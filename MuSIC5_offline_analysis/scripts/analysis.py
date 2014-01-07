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
from sys import exit

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





def run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5, l_bound=50, u_bound=20000):
  if inc_phase and not inc_sin:
    print 'Cannot have phase & no sin!'
    return
  # Output file info
  img_dir, txt_dir = get_img_and_txt_dirs(g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5, l_bound, bin_width)
  integral_data_file = txt_dir+"rates_and_integrals.txt"
  detailed_data_file = txt_dir+"all_info.txt"
  tau_file = txt_dir+"tau_values.txt"
  latex_file = txt_dir+"latex_table.txt"
    
  # Get the file & histogram names and add them to the dicts
  init_data_dicts(run_dict, sim_dict, g4bl, fast, exec_d4_d5)
  recreate_old_hist_files(run_dict, sim_dict, g4bl, exec_d4_d5)
  out_root_file = TFile(img_dir+"/out.root", "RECREATE")
  run_data = process_files(out_root_file, run_dict, "run", bin_width, fit_type, inc_phase, inc_sin, g4bl, img_dir, l_bound, u_bound)
  sim_data = process_files(out_root_file, sim_dict, "sim", bin_width, fit_type, inc_phase, inc_sin, g4bl, img_dir, l_bound, u_bound)
  
  all_data = dict(run_data, **sim_data)
  with open(integral_data_file, "w") as out_file:
    out_file.write(get_rates_table(all_data))
    out_file.write("*"*80+"\n")
    out_file.write(get_integrals_table(all_data))
  
  with open(detailed_data_file, "w") as out_file:
    out_file.write(get_detailed_table(all_data))
  
  with open(tau_file, "w") as out_file:
    out_file.write(get_tau_table(all_data))
  
  with open(latex_file, "w") as out_file:
    out_file.write(get_latex_table(all_data))
  
  for target in ("cu", "f"):
      out_root_file.cd()
      out_root_file.Add(make_and_save_rate_hist(target, run_data, "run", img_dir, out_root_file))
      out_root_file.Add(make_and_save_rate_hist(target, sim_data, "sim", img_dir, out_root_file))
      out_root_file.Add(make_and_save_count_hist(target, run_data, "run", img_dir, out_root_file))
      out_root_file.Add(make_and_save_count_hist(target, sim_data, "sim", img_dir, out_root_file))
  out_root_file.Write()
  # out_root_file.Close()
  return out_root_file

def get_img_and_txt_dirs(g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5, l_bound, bin_width):
  """
  Generate the appropriate directory name and if neccessary make it.
  """
  out_dir_root = "analysis_"
  
  if g4bl:       out_dir_root += "g4bl_"
  if inc_sin:    out_dir_root += "sin_"
  if inc_phase:  out_dir_root += "phase_"
  if exec_d4_d5: out_dir_root += "exec_d4_d5_"
  
  out_dir_root += "l_bound"+str(l_bound)
  out_dir_root += "bin_"+str(bin_width)
    
  out_dir_root += fit_type
  
  img_dir, txt_dir = "images/"+out_dir_root+"/", "output_txt/"+out_dir_root+"/"
  
  # Make all of the image directories
  for sub_dir in filter(lambda x: not path_exists(img_dir+x), ("fits", "rates", "counts", "zoom")):
      makedirs(img_dir+sub_dir) # works recurisvely
  
  if not path_exists(txt_dir):
    makedirs(txt_dir)
  
  return img_dir, txt_dir

def init_data_dicts(run_dict, sim_dict, g4bl, fast, exec_d4_d5):
  # Histogram names
  # run_hist_names = ("D5","D4","D3","D2","D1") if not fast else ("D2",)
  if exec_d4_d5:
      hist_d = "hist_files_offset_exec_d4_d5/"
      run_hist_names = ("D3","D2","D1") 
  elif fast:
    hist_d = "hist_files_offset/"
    run_hist_names = ("D2")
  else:
    hist_d = "hist_files_offset/"
    run_hist_names = ("D5","D4","D3","D2","D1") 

  sim_hist_name_fmt = "combined_{degrader}"
  # Formats of the file names
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

def recreate_old_hist_files(run_dict, sim_dict, g4bl, exec_d4_d5, script_name="make_plot_files.py", force=False):
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
    # generate_data_histograms(run_id)
    
  for sim_id, path in sim_files_to_regen:
    print "Regenerating sim file:", sim_id, "path", path
    # generate_sim_histograms(sim_id, g4bl, exec_d4_d5)
 

def process_files(out_root_file, run_ids, data_type, bin_width, fit_type, inc_phase, inc_sin, g4bl, img_dir, l_bound, u_bound):
  res = {}
  for file_id, meta_data in run_ids.items():
    if 'file_name' not in meta_data:  # if we're running fast
      continue
    # filename etc should all be in the meta data
    data_file = DataFile(bin_width=bin_width, **meta_data)
    out_root_file.cd()
    for h in data_file.hists.values():
      name = str(file_id) + "_" + h.GetTitle() 
      print name
      h.SetTitle(name)
      h.SetName(name)
      out_root_file.Add(h)
    if img_dir: save_hist_around_zero_region(data_file, img_dir)
    fit_data(data_file, fit_type, data_type, inc_phase, inc_sin, l_bound, u_bound, img_dir=img_dir)
    res[file_id] = data_file
    get_muons_per_namp(res[file_id], data_type, g4bl)
  return res

def save_hist_around_zero_region(data_file, img_dir, l_bound=-200, u_bound=200):
  for hist_key, hist in data_file.hists.items():
    img_name = img_dir+"zoom/{}_{}".format(data_file.short_name, hist.GetName())
    can = make_canvas(img_name)
    hist.GetXaxis().SetRangeUser(l_bound, u_bound)
    hist.Draw()
    can.Update()
    can.SaveAs(img_name+".eps")
    can.SaveAs(img_name+".svg")
    hist.GetXaxis().UnZoom() # reset the ranges to full
    
  

def fit_data(data_file, fit_type, data_type, inc_phase, inc_sin, l_bound, u_bound, img_dir="", fit_options="ILMER"):
  data_file.sum_integrals = {'f':0.0, 'cu':0.0}
  short_name = data_file.short_name
  bin_width = data_file.bin_width
  for hist_key, hist in data_file.hists.items():
    func_fmt, initial_settings = get_fit_func_and_settings(data_type, hist, fit_type, inc_phase, inc_sin)
    func_name = "{}_{}".format(short_name, hist.GetName())
    if img_dir:
      can = make_canvas(func_name, resize=True)
      hist.Draw()
      fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options, l_bound, u_bound)
      can.Update()
      img_name = img_dir+"fits/"+func_name
      can.SaveAs(img_name+".eps")
      can.SaveAs(img_name+".svg")
    else:
      fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options+"N")
    calculate_exp_integrals(hist, l_bound, u_bound)
    for k in data_file.sum_integrals:
      data_file.sum_integrals[k] += hist.integrals[k]


def get_fit_func_and_settings(data_type, hist, fit_type, inc_phase, inc_sin):
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
    elif not inc_sin:
      bkgnd             = [n_b]
      run_data_func_fmt = "[0]*exp(-x/[1]) + [2]*exp(-x/[3]) + [4]"
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
    # In g4bl we set the number of protons to be 9e8
    return 9e8
  else:
    # Only use the number of mu+ in g4bl as n_mu_sim is the number of mu+ simulated (mu- are scaled to this)
    g4bl_mu_per_p = 86710/9e8
    return n_mu_sim/g4bl_mu_per_p

def get_muons_per_namp(data, data_type, g4bl):
  """
  Calculate the rate of muons per proton
  """
  if data_type == "sim":
    n_proton = get_n_protons(g4bl, n_mu_sim=5e5)
    norm = n_proton/(1e-9*coloumb_in_e) # Want it in nA
  else:
    # norm = data.dead_time*data.run_time*data.proton_current*coloumb_in_e
    #  Make sure it's in nA
    norm = data.dead_time*data.run_time*data.proton_current/(1e-9)
  assert norm != 0.0
  
  data.muon_rates = {}
  for k in data.sum_integrals:
    data.muon_rates[k] = data.sum_integrals[k]/norm if data.sum_integrals[k] else data.sum_integrals[k]
  data.per_ch_rates = {}
  for ch in data.hist_names:
    data[ch].rate = {}
    for k in data[ch].integrals:
      # Because the integral is a ValueWithError if it's 0 then it will
      # cause divBy0 in carrying out the error propogation
      data[ch].rate[k] = data[ch].integrals[k]/norm if data[ch].integrals[k] else data[ch].integrals[k]

def get_integrals_table(data_dict):
  res = "{:^3s} | {:^3s} | {:^2s} | {:^21s} | {:^21s} | {:^13s}\n".format("id","dz","ch","cu","f","Chi^2/NDF") 
  fmt = "{f_id:^3s} | {dz:^3s} | {ch:^2s} | {i_c.value:7.2f}+/-{i_c.error:7.2f} |  {i_f.value:7.2f}+/-{i_f.error:7.2f}  | {chi:>5.0f} / {ndf:<5.0f}\n"
  for file_key, file in data_dict.items():
    res += fmt.format(f_id=str(file_key)[:3], dz=str(file.deg_dz), ch="--", i_c=file.sum_integrals["cu"], i_f=file.sum_integrals["f"], chi=-1, ndf=-1, )
    for ch in file.hist_names:
      res += fmt.format(f_id="--", dz="--", ch=ch[:2], chi=file[ch].fit_param["chi2"], ndf=file[ch].fit_param["ndf"],
              i_c=file[ch].integrals["cu"], i_f=file[ch].integrals["f"])
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

def get_tau_table(data_dict):
  res = ["{} | {:^3s}  |  {:^19s} | {:^19s} ".format("file","ch", "tau_f", "tau_cu")]
  fmt = "{f_k} | {ch:^3s} | {f.value:7.2f} +/- {f.error:7.2f} |  {cu.value:7.2f} +/- {cu.error:7.2f} "
  for file_key, file in data_dict.items():
    f_val_str = ["float f_{}    [{}] = {{".format(str(file_key)[:3], len(file.hists))]
    f_err_str = ["float f_er_{} [{}] = {{".format(str(file_key)[:3], len(file.hists))]
    c_val_str = ["float c_{}    [{}] = {{".format(str(file_key)[:3], len(file.hists))]
    c_err_str = ["float c_er_{} [{}] = {{".format(str(file_key)[:3], len(file.hists))]
    
    for ch, hist in file.hists.items():
      v = fmt.format(f_k=file_key, ch=ch[:3], f=hist.fit_param['tau_f'], cu=hist.fit_param['tau_cu'])
      f_val_str.append("{:7.2f}, ".format(hist.fit_param['tau_f'].value))
      f_err_str.append("{:7.2f}, ".format(hist.fit_param['tau_f'].error))
      c_val_str.append("{:7.2f}, ".format(hist.fit_param['tau_cu'].value))
      c_err_str.append("{:7.2f}, ".format(hist.fit_param['tau_cu'].error))
      res.append(v)
    f_val_str = "".join(f_val_str)
    f_err_str = "".join(f_err_str)
    c_val_str = "".join(c_val_str)
    c_err_str = "".join(c_err_str)
    res += [f_val_str, f_err_str, c_val_str, c_err_str]
  return "\n".join(res)

def get_latex_table(data_dict):
  res = "{:4s} & {:2s}&{:^19s}&{:^19s}&{:^18s}&{:^17s}&{:^17s}&{:^16s}&{:^18s}&{:^20s}&{:^20s}&{:^12s}&{:^9s} \\\\"
  res = [res.format("file", "ch", "N_b", "N_sin", "phi", "N_cu", "N_f", "i_c", "i_f", "r_c(/nA)", "r_f(/nA)", "chi2", "ndf")]
  fmt = "  &  {ch:^2s}  &  {N_b.value:7.3f} & {N_b.error:5.3f}  &  "+\
        "{N_sin.value:7.3f} & {N_sin.error:5.3f}  &  {phi.value:6.3f} & {phi.error:5.3f}  &  "+\
        "{N_cu.value:6.1f} & {N_cu.error:4.1f}  &  {N_f.value:7.2f} & {N_f.error:4.2f}  &  "+\
        "{i_c.value:5.0f} & {i_c.error:3.0f}  &  {i_f.value:6.0f} & {i_f.error:3.0f}  &  "+\
        "{r_c.value:7.2f} & {r_c.error:6.2f}  &  {r_f.value:7.2f} & {r_f.error:6.2f}  &  "+\
        "{chi2:>6.0f} & {ndf:<5.0f} \\\\"
  
  for file_key in ("448", "451", "452", "455", "458", "459"):
    file = data_dict[int(file_key)]
    res.append("\hline\n\multirow{5}{*}{%s}"%file_key)
    # Only produce this for D1-5 in order, as we don't always use D4 & D5 filter for it
    for ch in filter(lambda x: x in file.hists.keys(), ("D1", "D2", "D3", "D4", "D5")):
      hist =  file.hists[ch]
      N_b   = ValueWithError(-1, -1) if 'N_b'   not in hist.fit_param else hist.fit_param['N_b']
      N_sin = ValueWithError(-1, -1) if 'N_sin' not in hist.fit_param else hist.fit_param['N_sin']
      phi   = ValueWithError(-1, -1) if 'phi'   not in hist.fit_param else hist.fit_param['phi']
        
      v = fmt.format(ch=str(ch)[:3], N_b=N_b, N_sin=N_sin, phi=phi,
                    N_cu=hist.fit_param['N_cu'],   N_f=hist.fit_param['N_f'],
                    i_c=file[ch].integrals['cu'],  i_f=file[ch].integrals['f'],
                    r_c=file[ch].rate['cu'],       r_f=file[ch].rate['f'],
                    chi2=hist.fit_param['chi2'],   ndf=hist.fit_param['ndf'])
      res.append(v)
  return '\n'.join(res)
    
  
  
def make_rate_hist(name, target, data_dict):
  titles=("Degrader", "Muon rate (nA^{-1})")
  res = make_hist(name, mins=0, maxs=len(data_dict), bins=len(data_dict), titles=titles)
  
  dz_ordered_keys = [(k,v.deg_dz) for k,v in data_dict.items()]
  # sort by degrader thickness
  dz_ordered_keys.sort(key=lambda x:x[1])
  for bin_id, (file_id, degrader) in enumerate(dz_ordered_keys, 1):
    rate = data_dict[file_id].muon_rates[target]
    set_hist_bin_contents_and_er(res, bin_id, rate, name=str(degrader))
  return res

def make_and_save_rate_hist(target, data, data_type, img_dir, out_root_file):
  name = "Rate " if data_type == "run" else "Simulated rate "
  name += "of muons decaying in "+target
  hist = make_rate_hist(name, target, data)
  # out_root_file.Add(hist)
  canvas = make_canvas(name, resize=True)
  hist.Draw()
  img_name = img_dir+"rates/"+data_type+"_muon_rate_in_"+target
  canvas.SaveAs(img_name+".svg")
  canvas.SaveAs(img_name+".eps")
  return hist

def make_count_hist(name, target, data_dict):
  titles=("Degrader", "Muon count")
  res = make_hist(name, mins=0, maxs=len(data_dict), bins=len(data_dict), titles=titles)
  
  dz_ordered_keys = [(k,v.deg_dz) for k,v in data_dict.items()]
  # sort by degrader thickness
  dz_ordered_keys.sort(key=lambda x:x[1])
  for bin_id, (file_id, degrader) in enumerate(dz_ordered_keys, 1):
    count = data_dict[file_id].sum_integrals[target]
    set_hist_bin_contents_and_er(res, bin_id, count, name=str(degrader))
  return res

def make_and_save_count_hist(target, data, data_type, img_dir, out_root_file):
  name = "Count " if data_type == "run" else "Simulated count "
  name += "of muons decaying in "+target
  hist = make_count_hist(name, target, data)
  canvas = make_canvas(name, resize=True)
  hist.Draw()
  img_name = img_dir+"counts/"+data_type+"_muon_count_in_"+target
  canvas.SaveAs(img_name+".svg")
  canvas.SaveAs(img_name+".eps") 
  return hist   

def main():
  
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)  
  
  fast = False
  # fast = True
  exec_d4_d5 = True
  
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
  files_to_kill = []

  # g4bl, sin inc phase inc D4 & 5 (i.e. best fit for all show how bad D4 & D5 are)
  # Want this for big tables o' data
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, True, True, "tight", False
  files_to_kill.append(run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5))
  print "*"*80,"\nTable run complete!\n","*"*80
  
  # g4bl, sin inc phase inc D4 & 5 (i.e. best fit for all show how bad D4 & D5 are)
  # Want this one for the final plots of rates etc.
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, True, True, "tight", True
  files_to_kill.append(run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5))
  print "*"*80,"\nAnalysis run complete!\n","*"*80
  
  # g4bl, sin inc phase inc D4 & 5 (i.e. best fit for all show how bad D4 & D5 are)
  # Want one with a higher start fit point for systematics
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, True, True, "tight", True
  files_to_kill.append(run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5, l_bound=75))
  print "*"*80,"\nl_bound systematic run complete!\n","*"*80
  
  # g4bl, sin inc phase inc D4 & 5 (i.e. best fit for all show how bad D4 & D5 are)
  # Now we want to test affect of bin size for systematics 
  bin_width = 8
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, True, True, "tight", True
  files_to_kill.append(run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5))
  print "*"*80,"\nBin width = 8 run complete!\n","*"*80
  
  bin_width = 32
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, True, True, "tight", True
  files_to_kill.append(run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5))
  print "*"*80,"\nBin width = 32 run complete!\n","*"*80
  for f in files_to_kill: f.Close()
  return 
  
  # g4bl, sin inc phase inc D4 & 5 (i.e. best fit for all show how bad D4 & D5 are)
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, True, True, "loose_f", False
  run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5)
  
  # g4bl, sin inc phase inc D4 & 5 (i.e. best fit for all show how bad D4 & D5 are)
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, True, True, "loose_cu", False
  run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5)
  
  return
  # ########
  # tight fit no sin
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, False, False, "tight", True
  run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5)
  
  
  # loose fit no sin
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, False, False, "loose_f_cu", True
  run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5)
  
  return
  # loose fit sin
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, False, True, "loose_f_cu", True
  run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5)
  
  # tight fit sin
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, False, True, "tight", True
  run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5)
  
  # loose fit sin + phase
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, True, True, "loose_f_cu", True
  run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5)
  
  # tight fit sin + phase
  g4bl, inc_phase, inc_sin, fit_type, exec_d4_d5 = True, True, True, "tight", True
  run(run_dict, sim_dict, g4bl, fast, inc_phase, inc_sin, bin_width, fit_type, exec_d4_d5)
  
  
  return
if __name__=="__main__":
  main()