"""
analysis.py
scripts

Runs the full MuSIC5 analysis.

Created by Sam Cook on 2013-06-03.
"""


from time import time as current_time
from math import pi, exp
from os.path import getmtime as path_last_mod_time, exists as file_exists 
from ROOT import TFile, TGraph, gStyle
from make_plot_files import generate_histograms
from dead_time_estimation import get_dead_times_for_run_ids
from analysis_core import fit_histogram
from root_utilities import make_canvas, make_hist
from ValueWithError import set_hist_bin_contents_and_er

# fast = True
fast = False
hist_dir = "hist_files"
g4bl=True
# bin_width=50
bin_width=16
# The data files we actually want to run
# data hist names
run_channels = ("D5","D4","D3","D2","D1") if not fast else ("D5","D4")
# The data files we actually have
run_ids = {448:{'deg_dz':0,   'run_time':9221, 'proton_current':0.0153375e-9  },  #'acceptance':0.087,
           451:{'deg_dz':0.5, 'run_time':1001, 'proton_current':0.0154625e-9  },  #'acceptance':0.077,
           452:{'deg_dz':0.5, 'run_time':4944, 'proton_current':0.013132143e-9},  #'acceptance':0.077,
           455:{'deg_dz':1,   'run_time':6307, 'proton_current':0.013321429e-9},  #'acceptance':0.069,
           458:{'deg_dz':5,   'run_time':5144, 'proton_current':0.013625e-9   },  #'acceptance':0.045,
           459:{'deg_dz':5,   'run_time':2452, 'proton_current':0.012383929e-9},  #'acceptance':0.045,
           }\
           if not fast else \
           {451:{'deg_dz':0.5, 'run_time':1001, 'proton_current':0.0154625  },}

coloumb_in_e = 1.0/(1.602176565e-19)
n_protons_simulated = 900e6
simulated_degraders = {"5mm_Air":{'deg_dz':0},
                       "0.5mm_Aluminium":{'deg_dz':0.5},
                       "1mm_Aluminium":{'deg_dz':1},
                       "5mm_Aluminium":{'deg_dz':5},
                      }\
                      if not fast else \
                      {"5mm_Air":{'deg_dz':0},}
# Only treat the combined hist (for the moment)
sim_hist_name_fmt = "combined_{degrader}"

out_data_file_fmt=hist_dir+"/run{run_id}_hists.root"
out_sim_file_fmt =hist_dir+"/degrader_{degrader}_g4bl_hists.root"

# inc_phase = True
inc_phase = False

run_data_func_fmt   = "[0]*exp(-x/[1]) + [2]*exp(-x/[3]) + [4]*sin(2*pi*(x-[5])/[6]) + [7]"\
                      if inc_phase else \
                      "[0]*exp(-x/[1]) + [2]*exp(-x/[3]) + [4]*sin(2*pi*x/[5]) + [6]"
simulation_func_fmt = "[0]*exp(-x/[1]) + [2]*exp(-x/[3])"

img_dir = "images/analysis_phase/" if inc_phase else "images/analysis/"
txt_dir = "output_txt/analysis_phase/" if inc_phase else "output_txt/analysis/"
integral_data_file = txt_dir+"rates_and_integrals.txt" 
detailed_data_file = txt_dir+"all_info.txt" 

class DataFile(object):
  def __init__(self, file_name, hist_names, bin_width=None, **kwargs):
    super(DataFile, self).__init__()
    self.file_name = file_name
    self.file = TFile(self.file_name, "READ")
    
    self.hist_names = hist_names
    self.hists = {h:self.file.Get(h) for h in hist_names}
    
    if bin_width:
      self.bin_width = bin_width
      map(lambda x:x.Rebin(bin_width), self.hists.values())
    else:
      self.bin_width = 1 # What it should get set to initially  

    for k,v in kwargs.items():
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

def get_fit_func_and_settings(data_type, hist, fit_type):
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
  def get_setting_vals_for(param, fit_type):
    """
    Returns either a loose or a tight pair of bounds 
    and the value of tau.
    tau_f  = 2196.9811 +/- 0.0022
    tau_cu =  163.5    +/- 1
    """
    vals = {"f": {"tight":(2196.9811, 2196.9789, 2196.9833), 
                  "loose":(2196.9811, 1000.0,   20000.0)},
            "cu":{"tight":( 163.5   ,  162.5,     164.5),     
                  "loose":( 163.5   ,    0.0,   20000.0)}}
    return vals[param][fit_type]
  h_max = hist.GetMaximum()
  f_vals = get_setting_vals_for("f", "loose" if "f" in fit_type else "tight")
  n_f    = ("N_{f}"   , h_max/2,   1.0      , 2*h_max)   
  tau_f  = ("#tau_{f}", f_vals[0], f_vals[1], f_vals[2])

  cu_vals = get_setting_vals_for("cu", "loose" if "cu" in fit_type else "tight")
  n_cu    = ("N_{cu}",    h_max,      1.0       , 2*h_max)
  tau_cu  = ("#tau_{cu}", cu_vals[0], cu_vals[1], cu_vals[2])
  
  if data_type=="sim":
    return simulation_func_fmt, (n_cu, tau_cu, n_f, tau_f)
  elif data_type=="run":
    #       par name      initial  minimum  maximum
    n_sin  = ("N_{sin}",  h_max/20,    1.0, h_max/3) # scale the noise
    phase  = ("#phi",      30,          0.0,   65.0) # phase
    period = ("T",        59.3,       55.0,    65.0) # period
    n_b    = ("N_{b}",    h_max/10,    1.0, h_max  ) # Flat background
    bkgnd  = [n_sin, phase, period, n_b] if inc_phase else [n_sin, period, n_b]
    return run_data_func_fmt, tuple([n_cu, tau_cu, n_f, tau_f] + bkgnd)

def recreate_old_hist_files(run_ids, simulated_degraders, force=False):
  """
  Check if any of the files are older than their generating script, or
  don't exist. If this is true for any re-run the script.
  """
  # TODO Set up look for 'main' in the script and pass file names...
  files_to_check = [out_data_file_fmt.format(run_id=r) for r in run_ids] + \
                   [out_sim_file_fmt.format(degrader=s) for s in simulated_degraders]
  
  get_age = lambda path: current_time() - path_last_mod_time(path)
  script_age = get_age("make_plot_files.py")
  needs_regen = lambda path: not file_exists(path) or script_age < get_age(path)
  # regen will be a list of bools showing whether the file exists or is too old
  regen=map(needs_regen, files_to_check)
  if force or any(regen):
    print "Regenerating all files, please wait."
    generate_histograms(run_ids=run_ids, degraders=simulated_degraders, g4bl=g4bl)
  
  
def update_metadata(file_dictionaries):
  """
  Fills in the metadata for the various runs. 
  
  Most of this information is statically loaded from meta_data but 
  some (e.g. dead time & acceptance) is calculated
  """
  # area of U scint/area of beampipe
  acceptance_u_bound = 8*30*380.0/(pi*380.0**2)
  print "Maximum (naive, geometrical) acceptance:", acceptance_u_bound
  
  dead_times = get_dead_times_for_run_ids(file_dictionaries.keys())
  for run_id, dead_time_info in dead_times.items():
    file_dictionaries[run_id].update(dead_time_info)
  
def process_files(run_ids, data_type, fit_type="tight"):
  res = {}
  for file_id, meta_data in run_ids.items():
    file_name, hist_names = get_file_and_hist_names(file_id, data_type)
    res[file_id] = DataFile(file_name, hist_names, bin_width, **meta_data)
  fit_data(res, fit_type, data_type)
  get_muon_rate(res, data_type)
  return res
  
def get_file_and_hist_names(file_id, data_type):
  if data_type =="sim":
    return out_sim_file_fmt.format(degrader=file_id), [sim_hist_name_fmt.format(degrader=file_id),]
  elif data_type=="run":
    return out_data_file_fmt.format(run_id=file_id), run_channels

def calculate_exp_integrals(hist, l_bound=50, u_bound=20000):
  res = {}
  for k in ("cu", "f"):
    tau, scale = hist.fit_param["tau_"+k], hist.fit_param["N_"+k]
    l_exp, u_exp = [exp(-float(i)/float(tau)) for i in (l_bound, u_bound)] 
    # The 0th bin is underflow
    integral = tau*scale*(l_exp - u_exp) / hist.GetBinWidth(1)
    res[k] = integral
  hist.integrals = res

def fit_data(run_data_dict, fit_type, data_type, fit_options="ILMER"):
  for file_key, file in run_data_dict.items():
    file.sum_integrals = {'f':0.0, 'cu':0.0}
    for hist_key, hist in file.hists.items():
      func_fmt, initial_settings = get_fit_func_and_settings(data_type, hist, fit_type)
      func_name = "{}_{}".format(file_key, hist_key)
      if img_dir:
        can = make_canvas(func_name)
        hist.Draw()
        fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options)
        can.Update()
        img_name = img_dir+func_name
        can.SaveAs(img_name+".png")
        can.SaveAs(img_name+".svg")
      else:
        fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options+"N")
      calculate_exp_integrals(hist, l_bound=50, u_bound=20000)
      for k in ('f','cu'):
        file.sum_integrals[k] += hist.integrals[k]
      
def get_muon_rate(run_data_dict, data_type):
  """
  Calculate the rate of muons per proton
  """
  for run_id, data in run_data_dict.items():
    denom = n_protons_simulated if data_type == "sim" else (data.dead_time*data.run_time*data.proton_current*coloumb_in_e)
    data.muon_rates = {k:data.sum_integrals[k]/denom for k in data.sum_integrals}
    data.per_ch_rates = {}
    for ch in data.hist_names:
      data[ch].rate = {k:data[ch].integrals[k]/denom for k in data[ch].integrals}
    
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

def make_and_save_rate_hist(target, data, data_type):
  name = "Rate " if data_type == "run" else "Simulated rate "
  name += "of muons decaying in "+target
  hist = make_rate_hist(name, target, data)
  canvas = make_canvas(name, resize=True)
  hist.Draw()
  img_name = img_dir+data_type+"_muon_rate_in_"+target
  canvas.SaveAs(img_name+".svg")
  canvas.SaveAs(img_name+".png")
    
def main():
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)  
  
  recreate_old_hist_files(run_ids, simulated_degraders)
  update_metadata(run_ids)
  
  run_data = process_files(run_ids, "run")
  sim_data = process_files(simulated_degraders, "sim")
  
  all_data = dict(run_data, **sim_data)
  with open(integral_data_file, "w") as out_file:
    out_file.write(get_rates_table(all_data))
    out_file.write("*"*80+"\n")
    out_file.write(get_integrals_table(all_data))
  
  with open(detailed_data_file, "w") as out_file:
    out_file.write(get_detailed_table(all_data))
  
  for target in ("cu", "f"):
    make_and_save_rate_hist(target, run_data, "run")
    make_and_save_rate_hist(target, sim_data, "sim")
  

if __name__=="__main__":
  main()