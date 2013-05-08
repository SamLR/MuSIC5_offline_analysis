
from ROOT import TFile, TCanvas, TF1
from ValueWithError import ValueWithError

def first_upstream_step_of_a_mu_plus(entry, hit):
  return check_pdgid_location_and_first_step(entry, hit, pdgid=-13, counter=1)

def first_downstream_step_of_an_e_plus(entry, hit):
  return check_pdgid_location_and_first_step(entry, hit, pdgid=-11, counter=3)

def check_pdgid_location_and_first_step(entry, hit, pdgid, counter):
  pdgid = (entry.pdgid[hit] == pdgid)
  counter = (entry.counter[hit] == counter)
  first_step = (entry.first_step[hit])
  return pdgid and counter and first_step
  
def get_hits_with(entry, filter_func):
  """
  Iterates over the hits in the entry and returns a list
  containing the results of calling the filter function, 
  which is expected to take the entry and a hit index as 
  arguments.
  """
  res = []
  for hit in range(entry.nhit):
    val = filter_func(entry, hit)
    if val: res.append(val)
  return res
  
def get_func_with_named_initialised_param(name, hist, func_fmt, initial_settings):
  func = TF1(name, func_fmt, 50, 20000)
                       
  for parN, (name, initial, lower_limit, upper_limit) in enumerate(initial_settings):
    func.SetParName(parN, name)
    func.SetParameter(parN, initial(hist))
    func.SetParLimits(parN, lower_limit(hist), upper_limit(hist))
    
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
  return res