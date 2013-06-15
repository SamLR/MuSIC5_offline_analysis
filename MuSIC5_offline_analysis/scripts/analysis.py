"""
analysis.py
scripts

Runs the full MuSIC5 analysis.

Created by Sam Cook on 2013-06-03.
"""


from time import time as current_time
from math import pi, exp
from os import makedirs
from os.path import getmtime as path_last_mod_time, exists as path_exists 
from ROOT import TFile, TGraph, gStyle
from make_plot_files import generate_data_histograms, generate_sim_histograms
from dead_time_estimation import get_dead_times_for_run_ids
from analysis_core import fit_histogram
from root_utilities import make_canvas, make_hist
from ValueWithError import ValueWithError, set_hist_bin_contents_and_er

# TODO Create some sort of analysis configuration object that holds g4bl etc

coloumb_in_e = 1.0/(1.602176565e-19)

class DataFile(object):
  def __init__(self, file_name, hist_names, bin_width=None, **kwargs):
    super(DataFile, self).__init__()
    self.file = TFile(file_name, "READ")
    self.file_name = file_name
    
    self.hist_names = hist_names
    self.hists = {h:self.file.Get(h) for h in hist_names}
    
    if bin_width:
      self.bin_width = bin_width
      map(lambda x:x.Rebin(bin_width), self.hists.values())
    else:
      self.bin_width = 1 # What it should get set to initially  
    
    # make sure that we don't reset any values
    ignore = ("file", "file_name", "hist_names", "hists", "bin_width")
    for k,v in kwargs.items():
      if k in ignore:
        continue
      else:
        setattr(self,k,v)
  
  def __str__(self):
    fmt = "File name:{}\n\tMeta-data:{}\n\tSummed integrals:{}\n\tSummed Rates:{}\n"
    ignore = ("hist_names", "file_name", "hists", "file", "muon_rates", "sum_integrals")
    meta_data = ["\n\t\t{}:{}".format(i,getattr(self, i)) for i in self.__dict__ if i[:2] != "__" and i not in ignore]
    meta_data = "".join(meta_data)
    integrals = ["\n\t\t{}:{}".format(i,self.sum_integrals[i]) for i in self.sum_integrals]
    rates = ["\n\t\t{}:{}".format(i,self.muon_rates[i]) for i in self.muon_rates]
    return fmt.format(self.file_name, meta_data, integrals, rates)
  
  def __repr__(self):
    fmt = "<File:{} Meta-data:{} Histograms:{}>"
    ignore = ("hist_names", "file_name", "hists", "file")
    meta_data = ["{}:{} ".format(i,getattr(self, i)) for i in self.__dict__ if i[:2] != "__" and i not in ignore]
    meta_data = "".join(meta_data)
    return fmt.format(self.file_name, meta_data, self.hist_names)
  
  def __getitem__(self, item):
    return self.hists[item]
  
  def __getattr__(self,attr):
    return self.file.__getattribute__(attr)





def run(run_dict, sim_dict, g4bl, fast, inc_phase, bin_width, fit_type):

  # Output file info
  img_dir, txt_dir = get_img_and_txt_dirs(g4bl, inc_phase, fit_type)
  integral_data_file = txt_dir+"rates_and_integrals.txt"
  detailed_data_file = txt_dir+"all_info.txt"
  
  # Get the file & histogram names and add them to the dicts
  init_data_dicts(run_dict, sim_dict, g4bl, fast)
  recreate_old_hist_files(run_dict, sim_dict, g4bl)
  
  run_data = process_files(run_dict, "run", bin_width, fit_type, inc_phase, g4bl, img_dir)
  sim_data = process_files(sim_dict, "sim", bin_width, fit_type, inc_phase, g4bl, img_dir)
  
  all_data = dict(run_data, **sim_data)
  with open(integral_data_file, "w") as out_file:
    out_file.write(get_rates_table(all_data))
    out_file.write("*"*80+"\n")
    out_file.write(get_integrals_table(all_data))
  
  with open(detailed_data_file, "w") as out_file:
    out_file.write(get_detailed_table(all_data))
  
  for target in ("cu", "f"):
    make_and_save_rate_hist(target, run_data, "run", img_dir)
    make_and_save_rate_hist(target, sim_data, "sim", img_dir)


def get_img_and_txt_dirs(g4bl, inc_phase, fit_type):
  """
  Generate the appropriate directory name and if neccessary make it.
  """
  if g4bl and inc_phase:
    out_dir_root = "analysis_g4bl_phase_"
  elif g4bl:
    out_dir_root = "analysis_g4bl_"
  elif inc_phase:
    out_dir_root = "analysis_phase_"
  else:
    out_dir_root = "analysis_"
  out_dir_root += fit_type
  
  res = ("images/"+out_dir_root+"/", "output_txt/"+out_dir_root+"/")
  
  for path in res:
    if not path_exists(path):
      makedirs(path)
  
  return res

def init_data_dicts(run_dict, sim_dict, g4bl, fast):
  # Histogram names
  run_hist_names = ("D5","D4","D3","D2","D1") if not fast else ("D2",)
  sim_hist_name_fmt = "combined_{degrader}"
  # Formats of the file names
  hist_d = "hist_files_offset/"
  in_data_file_fmt  = hist_d+"run{run_id}_hists.root"
  if g4bl:
    in_sim_file_fmt = hist_d+"degrader_{degrader}_g4bl_hists.root" 
  else:
    in_sim_file_fmt = hist_d+"degrader_{degrader}_hists.root"
  
  # Calculate the dead times and add them to the metadata dictionaries
  dead_times = get_dead_times_for_run_ids(run_dict.keys())
  for run, run_info in run_dict.items():
    run_info.update(dead_times[run]) 
    run_info['file_name']  = in_data_file_fmt.format(run_id=run)
    run_info['hist_names'] = run_hist_names
    run_info['short_name'] = str(run)
    if fast: # only set up one file
      break
    
  for sim, sim_info in sim_dict.items():
    sim_info['file_name']  = in_sim_file_fmt.format(degrader=sim)
    sim_info['hist_names'] = (sim_hist_name_fmt.format(degrader=sim),)
    sim_info['short_name'] = sim
    if fast: # only set up one file
      break

def recreate_old_hist_files(run_dict, sim_dict, g4bl, script_name="make_plot_files.py", force=False):
  """
  Check if any of the files are older than their generating script, or
  don't exist. If this is true for any re-run the script.
  """
  # Get lists of file names to check if any need regenerating
  run_files = [(r, run_dict[r]['file_name']) for r in run_dict if 'file_name' in run_dict[r]]
  sim_files = [(s, sim_dict[s]['file_name']) for s in sim_dict if 'file_name' in sim_dict[s]]
  
  get_age = lambda path: current_time() - path_last_mod_time(path)
  script_age = get_age(script_name)
  
  needs_regen = lambda entry: not path_exists(entry[1]) or script_age < get_age(entry[1])
  
  # regen will be a list of bools showing whether the file exists or is too old
  sim_files_to_regen=filter(needs_regen, sim_files)
  run_files_to_regen=filter(needs_regen, run_files)
  
  for run_id, path in run_files_to_regen:
    print "Regenerating run file:", run_id, "path", path
    generate_data_histograms(run_id)
    
  for sim_id, path in sim_files_to_regen:
    print "Regenerating sim file:", sim_id, "path", path
    generate_sim_histograms(sim_id, g4bl)
 

def process_files(run_ids, data_type, bin_width, fit_type, inc_phase, g4bl, img_dir):
  res = {}
  for file_id, meta_data in run_ids.items():
    if 'file_name' not in meta_data:  # if we're running fast
      continue
    # filename etc should all be in the meta data
    data_file = DataFile(bin_width=bin_width, **meta_data)
    if img_dir: save_hist_around_zero_region(data_file, img_dir)
    fit_data(data_file, fit_type, data_type, inc_phase, img_dir)
    res[file_id] = data_file
    get_muon_rate(res[file_id], data_type, g4bl)
  return res

def save_hist_around_zero_region(data_file, img_dir, l_bound=-200, u_bound=200):
  for hist_key, hist in data_file.hists.items():
    img_name = img_dir+"zoom/{}_{}".format(data_file.short_name, hist.GetName())
    can = make_canvas(img_name)
    hist.GetXaxis().SetRangeUser(l_bound, u_bound)
    hist.Draw()
    can.Update()
    can.SaveAs(img_name+".png")
    can.SaveAs(img_name+".svg")
    hist.GetXaxis().UnZoom() # reset the ranges to full
    
  

def fit_data(data_file, fit_type, data_type, inc_phase, img_dir="", fit_options="ILMER"):
  data_file.sum_integrals = {'f':0.0, 'cu':0.0}
  short_name = data_file.short_name
  bin_width = data_file.bin_width
  for hist_key, hist in data_file.hists.items():
    func_fmt, initial_settings = get_fit_func_and_settings(data_type, hist, fit_type, inc_phase)
    func_name = "{}_{}".format(short_name, hist.GetName())
    if img_dir:
      can = make_canvas(func_name, resize=True)
      hist.Draw()
      fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options)
      can.Update()
      img_name = img_dir+"fits/"+func_name
      can.SaveAs(img_name+".png")
      can.SaveAs(img_name+".svg")
    else:
      fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options+"N")
    calculate_exp_integrals(hist, l_bound=00, u_bound=20000)
    # calculate_exp_integrals(hist, l_bound=50, u_bound=20000)
    for k in data_file.sum_integrals:
      data_file.sum_integrals[k] += hist.integrals[k]


def get_fit_func_and_settings(data_type, hist, fit_type, inc_phase):
  """
  Returns the correct fit settings for simulation depending on 
  whether mu+ or mu-. Fit type specifies how tightly the tau
  parameters should be constrained: 'loose' specifes that 
  it should be constrained to within the nearest sensible 1k
  division (e.g. 0 < tau_cu < 1k or 1k< tau_f<20k). 'Tight'
  constrains the value to within the PDG limits.
  
  tau_cu = 163.5     +/- 1ns
  tau_f  = 2196.9811 +/- 0.0022ns
  """
  f_vals  = (2196.9811, 1000.0, 20000.0) if "f"  in fit_type else (2196.9811, 2196.9789, 2196.9833)
  cu_vals = ( 163.5   ,    0.0, 20000.0) if "cu" in fit_type else ( 163.5   ,  162.5   ,  164.5   )
  
  h_max = hist.GetMaximum()
  #              par name    initial     minimum     maximum
  n_f     = ("N_{f}"    ,    h_max/2,        0.0,    2*h_max) # Scale of free component
  n_cu    = ("N_{cu}"   ,      h_max,        0.0,    2*h_max) # Scale of copper component
  tau_f   = ("#tau_{f}" ,  f_vals[0],  f_vals[1],  f_vals[2]) # lifetime of free muon
  tau_cu  = ("#tau_{cu}", cu_vals[0], cu_vals[1], cu_vals[2]) # lifetime of muon in copper
  
  if data_type=="sim":
    simulation_func_fmt = "[0]*exp(-x/[1]) + [2]*exp(-x/[3])"
    return simulation_func_fmt, (n_cu, tau_cu, n_f, tau_f)
  elif data_type=="run":
    #       par name      initial  minimum  maximum
    n_b    = ("N_{b}"  , h_max/10,  0.0,   h_max) # Flat background
    n_sin  = ("N_{sin}", h_max/20,  0.0, h_max/3) # scale the noise
    phase  = ("#phi"   ,     30.0,  0.0,    65.0) # phase
    period = ("T"      ,     59.3, 55.0,    65.0) # period
    if inc_phase:
      bkgnd             = [n_sin, phase, period, n_b] 
      run_data_func_fmt = "[0]*exp(-x/[1]) + [2]*exp(-x/[3]) + [4]*sin(2*pi*(x-[5])/[6]) + [7]"
    else:
      bkgnd             = [n_sin, period, n_b]
      run_data_func_fmt = "[0]*exp(-x/[1]) + [2]*exp(-x/[3]) + [4]*sin(2*pi*x/[5]) + [6]"
    
    return run_data_func_fmt, tuple([n_cu, tau_cu, n_f, tau_f] + bkgnd) 
  

def calculate_exp_integrals(hist, l_bound=50, u_bound=20000):
  res = {}
  for k in ("cu", "f"):
    tau, scale = hist.fit_param["tau_"+k], hist.fit_param["N_"+k]
    l_exp, u_exp = [exp(-float(i)/float(tau)) for i in (l_bound, u_bound)] 
    
    if l_exp == 0.0:
      print "\n\nWARNING, tau value too small, integral ~= 0.0"
      print tau, scale, hist.GetBinWidth(1), l_exp, u_exp
      res[k] = ValueWithError(0.0, 0.0)
      continue
    # The 0th bin is underflow
    integral = (l_exp - u_exp) / hist.GetBinWidth(1)
    integral *= tau*scale
    res[k] = integral
  hist.integrals = res


def get_n_protons(g4bl, n_mu_sim):
  if g4bl:
    # In g4bl we set the number of protons to be 9e6
    return 9e6 
  else:
    # Add an error to this as there's an error on the number of muons in g4bl
    g4bl_mu_per_p = ValueWithError(86710)/9e8
    return n_mu_sim/g4bl_mu_per_p

def get_muon_rate(data, data_type, g4bl):
  """
  Calculate the rate of muons per proton
  """
  if data_type == "sim":
    denom = get_n_protons(g4bl, n_mu_sim=5e5) 
  else:
    denom = data.dead_time*data.run_time*data.proton_current*coloumb_in_e
  assert denom != 0.0
  
  data.muon_rates = {}
  for k in data.sum_integrals:
    data.muon_rates[k] = data.sum_integrals[k]/denom if data.sum_integrals[k] else data.sum_integrals[k]
  data.per_ch_rates = {}
  for ch in data.hist_names:
    data[ch].rate = {}
    for k in data[ch].integrals:
      # Because the integral is a ValueWithError if it's 0 then it will
      # cause divBy0 in carrying out the error propogation
      data[ch].rate[k] = data[ch].integrals[k]/denom if data[ch].integrals[k] else data[ch].integrals[k]
    
def get_integrals_table(data_dict):
  res = "{:^3s} | {:^3s} | {:^2s} | {:^21s} | {:^21s} | {:^13s}\n".format("id","dz","ch","cu","f","Chi^2/NDF") 
  fmt = "{:^3s} | {:^3s} | {:^2s} | {} | {} | {:>5.0f} / {:<5.0f}\n"
  for file_key, file in data_dict.items():
    res += fmt.format(str(file_key)[:3], str(file.deg_dz), "--", file.sum_integrals["cu"], file.sum_integrals["f"], -1, -1 )
    for ch in file.hist_names:
      res += fmt.format("--", "--", ch[:2], file[ch].integrals["cu"], file[ch].integrals["f"], 
                        file[ch].fit_param["chi2"], file[ch].fit_param["ndf"])
  return res

def get_rates_table(data_dict):
  res = "{:^3s} | {:^3s} | {:^2s} | {:^20s} | {:^20s}\n".format("id","dz","ch","cu rate (muon per p)","f rate (muon per p)") 
  fmt = "{:^3s} | {:^3s} | {:^2s} | {} | {}\n"
  for file_key, file in data_dict.items():
    res += fmt.format(str(file_key)[:3], str(file.deg_dz), "--", file.muon_rates["cu"], file.muon_rates["f"])
    for ch in file.hist_names:
      res += fmt.format("--", "--", ch[:2], file[ch].rate['cu'], file[ch].rate["f"])
  return res

def get_detailed_table(data_dict):
  res = ""
  column_order = ("N_f", "tau_f", "N_cu", "tau_cu", "N_sin", "phi", "T", "N_b")
  for file_key, file in data_dict.items():
    res+=str(file)
    first = True
    for ch, hist in file.hists.items():
      if first:
        first = False
        res += "ch |  Chi^2/NDF "
        ch_fmt = "{ch} | {chi2:>5.0f} / {ndf:<5.0f}"
        for param in column_order:
          if param not in hist.fit_param: continue
          res = res + (' {:^20s} |'.format(param))
          ch_fmt += ' {%s} |'%(param)
        res, ch_fmt = res+"\n", ch_fmt+"\n"
      res += ch_fmt.format(ch=ch[:2],**hist.fit_param)
    res += "*"*80 + "\n\n"
  return res
    

def make_rate_hist(name, target, data_dict):
  titles=("Degrader", "Muons per proton")
  res = make_hist(name, mins=0, maxs=len(data_dict),bins=len(data_dict), titles=titles)
  
  dz_ordered_keys = [(k,v.deg_dz) for k,v in data_dict.items()]
  # sort by degrader thickness
  dz_ordered_keys.sort(key=lambda x:x[1])
  for bin_id, (file_id, degrader) in enumerate(dz_ordered_keys, 1):
    rate = data_dict[file_id].muon_rates[target]
    set_hist_bin_contents_and_er(res, bin_id, rate, name=str(degrader))
  return res

def make_and_save_rate_hist(target, data, data_type, img_dir):
  name = "Rate " if data_type == "run" else "Simulated rate "
  name += "of muons decaying in "+target
  hist = make_rate_hist(name, target, data)
  canvas = make_canvas(name, resize=True)
  hist.Draw()
  img_name = img_dir+"rates/"+data_type+"_muon_rate_in_"+target
  canvas.SaveAs(img_name+".svg")
  canvas.SaveAs(img_name+".png")
    

def main():
  
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)  
  
  fast = False
  # fast = True

  # The data files we actually have
  run_dict = {
              448:{'deg_dz':0,   'run_time':9221, 'proton_current':0.0153375e-9  },  #'acceptance':0.087,
             } if fast else {
              448:{'deg_dz':0,   'run_time':9221, 'proton_current':0.0153375e-9  },  #'acceptance':0.087,
              451:{'deg_dz':0.5, 'run_time':1001, 'proton_current':0.0154625e-9  },  #'acceptance':0.077,
              452:{'deg_dz':0.5, 'run_time':4944, 'proton_current':0.013132143e-9},  #'acceptance':0.077,
              455:{'deg_dz':1,   'run_time':6307, 'proton_current':0.013321429e-9},  #'acceptance':0.069,
              458:{'deg_dz':5,   'run_time':5144, 'proton_current':0.013625e-9   },  #'acceptance':0.045,
              459:{'deg_dz':5,   'run_time':2452, 'proton_current':0.012383929e-9},  #'acceptance':0.045,
             }
            
  sim_dict = {
              "5mm_Air"        :{'deg_dz':0},
             } if fast else {
              "5mm_Air"        :{'deg_dz':0},
              "0.5mm_Aluminium":{'deg_dz':0.5},
              "1mm_Aluminium"  :{'deg_dz':1},
              "5mm_Aluminium"  :{'deg_dz':5},
             }

  bin_width=16
  g4bl, inc_phase, fit_type = True, True, "tight"
  run(run_dict, sim_dict, g4bl, fast, inc_phase, bin_width, fit_type)
  
  g4bl, inc_phase, fit_type = False, True, "tight"
  run(run_dict, sim_dict, g4bl, fast, inc_phase, bin_width, fit_type)
  return
  g4bl, inc_phase, fit_type = True, False, "tight"
  run(run_dict, sim_dict, g4bl, fast, inc_phase, bin_width, fit_type)
  
  g4bl, inc_phase, fit_type = False, False, "tight"
  run(run_dict, sim_dict, g4bl, fast, inc_phase, bin_width, fit_type)
  
  g4bl, inc_phase, fit_type = True, True, "loose_f"
  run(run_dict, sim_dict, g4bl, fast, inc_phase, bin_width, fit_type)
  
  g4bl, inc_phase, fit_type = False, True, "loose_f"
  run(run_dict, sim_dict, g4bl, fast, inc_phase, bin_width, fit_type)
  
  g4bl, inc_phase, fit_type = True, False, "loose_f"
  run(run_dict, sim_dict, g4bl, fast, inc_phase, bin_width, fit_type)
  
  g4bl, inc_phase, fit_type = False, False, "loose_f"
  run(run_dict, sim_dict, g4bl, fast, inc_phase, bin_width, fit_type)

if __name__=="__main__":
  main()