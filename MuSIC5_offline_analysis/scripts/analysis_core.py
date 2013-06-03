
from ROOT import TFile, TCanvas, TF1
from ValueWithError import ValueWithError

def fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options="MER"):
  func = get_func_with_named_initialised_param(func_name, hist, func_fmt, initial_settings)
  hist.Fit(func, fit_options)
  hist.func = func
  hist.fit_param = get_fit_parameters(func)

def get_func_with_named_initialised_param(name, hist, func_fmt, initial_settings,l_bound=50,u_bound=20000):
  func = TF1(name, func_fmt, l_bound, u_bound)
                       
  for parN, (name, initial, lower_limit, upper_limit) in enumerate(initial_settings):
    func.SetParName(parN, name)
    func.SetParameter(parN, float(initial(hist)))
    func.SetParLimits(parN, float(lower_limit(hist)), float(upper_limit(hist)))
    
  return func

def clean_par_name(string, char_to_del="{}#"):
  for char in char_to_del:
    string = string.replace(char, "")
  return string

def get_fit_parameters(func):
  res = {}
  for par_id in range(func.GetNpar()):
    par_name = clean_par_name( func.GetParName(par_id) )
    res[par_name] = ValueWithError( func.GetParameter(par_id), func.GetParError(par_id) )
  res['chi2'] = func.GetChisquare()
  res['ndf'] = func.GetNDF()
  return res
    
def get_file_root(filename):
  filename = filename.split("/")[-1]
  return filename.replace(".root","")

def get_hits_with(entry, filter_funcs, record_param):
  """
  Iterates over the hits in the entry and returns a list
  containing the results of calling the filter function, 
  which is expected to take the entry and a hit index as 
  arguments.
  """
  res = []
  for hit in range(entry.nhit):
    pass_filter = [func(entry, hit) for func in filter_funcs]
    if all(pass_filter):
      val = [getattr(entry, param)[hit] for param in record_param]
      res.append(val)
  return res

def get_pid_counter_filter(pid, counter):
  p_t_pairs = (("pdgid", pid), ("counter", counter), ("first_step", True))
  return [get_filter_function(p,t) for p,t in p_t_pairs]

def get_filter_function(param, test=None):
  return lambda entry, hit: ((getattr(entry, param)[hit])==test)
  
def get_decay_type(mu_type, decay_vertex):
  if mu_type=="mu-" and decay_vertex==2:
    return "cu"
  else:
    return "f"
    
def fill_hist_with_mu_e_times(hist,entry, mu_type):
  """
  Returns the first hits by muon and an electron 
  in the up and downstream counters respectively
  """
  # Get all the upstream muons and downstream electrons
  
  if "-" in mu_type:
    assert "+" not in mu_type
    mu_pid, e_pid = (13, 11) 
  elif "+" in mu_type:    
    assert "-" not in mu_type
    mu_pid, e_pid = (-13, -11)
    
  muons     = get_hits_with(entry, get_pid_counter_filter(mu_pid, 1),\
                            ("trkid", "tof"))
  electrons = get_hits_with(entry, get_pid_counter_filter(e_pid,  3),\
                            ("parentid", "tof"))
  res = []
  for e_parent, e_time in electrons:
    parent_muon = filter(lambda mu: mu[0]==e_parent, muons)
    if parent_muon and (e_time - parent_muon[0][1] > 50):  
      hist.Fill(e_time - parent_muon[0][1])
      muons.remove(parent_muon[0])