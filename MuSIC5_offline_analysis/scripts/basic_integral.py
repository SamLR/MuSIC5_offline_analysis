""" 
  A very simple and inclusive (hopefully) attempt at analysing the 
  simulated data for MuSIC 5
  simple_sim_analysis.py
  scripts
  
  Created by Sam Cook on 2013-05-07.
  Copyright 2013 Sam Cook. All rights reserved.
 
"""

from analysis_core import get_hits_with, get_func_with_named_initialised_param, \
                          get_fit_parameters, get_file_root, get_pid_counter_filter
from root_utilities import make_hist, make_canvas, get_tree_from_file
from ROOT import gStyle
from time import sleep
from math import exp

def create_histogram_from_tree(name, tree, bin_width, mu_type):
  lb, ub = -20000, 20000
  nbins = (ub - lb)/bin_width
  hist = make_hist(name, mins=lb,maxs=ub, titles=["Time (ns)", "Count"], bins=nbins)
  hist.bin_width = bin_width
  for entry in tree:
    time = get_mu_e_dt_for_entry(entry, mu_type)
    if time:
      hist.Fill(time)
  return hist

def get_mu_e_dt_for_entry(entry, mu_type):
  """
  Returns the first hits by muon and an electron 
  in the up and downstream counters respectively
  """
  if mu_type=="mu-":
    mu_pid, e_pid = (13, 11) 
  elif mu_type=="mu+":
     mu_pid, e_pid = (-13, -11)  
    
  muons     = get_hits_with(entry, get_pid_counter_filter(mu_pid, 1), ("trkid",    "tof"))
  electrons = get_hits_with(entry, get_pid_counter_filter(e_pid,  3), ("parentid", "tof"))
  
  muons, electrons = get_muon_electron_decay_times(muons, electrons)
  
  if len(electrons)>0 and len(muons)>0:
    # Finally: get the times
    start_time = min([m[1] for m in muons])
    stop_time  = min([e[1] for e in electrons])
    return stop_time - start_time  
  else: 
    return False

def get_muon_electron_decay_times(muons, electrons):
  # find the common track/parent ids
  track_ids  = set([m[0] for m in muons])
  parent_ids = set([e[0] for e in electrons])
  decay_pairs = track_ids.intersection(parent_ids)
  
  # Get the times
  muons     = filter(lambda track_id: track_id[0] in decay_pairs, muons)
  electrons = filter(lambda parent_id: parent_id[0] in decay_pairs, electrons)
  return muons, electrons

def fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options="MER"):
  func = get_func_with_named_initialised_param(func_name, hist, func_fmt, initial_settings)
  hist.Fit(func, fit_options)
  hist.func = func
  hist.fit_param = get_fit_parameters(func)

def save_hist_with_fit(hist, name, save_image):
  canvas = make_canvas(name)
  hist.Draw()
  canvas.Update()
  canvas.SaveAs(save_image)

def get_integrals_from_histogram_for_keys(hist, keys, l_bound=50, u_bound=20000):
  res = {}
  for k in keys:
    tau, scale = hist.fit_param["tau_"+k], hist.fit_param["N_"+k]
    l_exp, u_exp = [exp(-float(i)/float(tau)) for i in (l_bound, u_bound)] 
    integral = tau*scale*(l_exp - u_exp) / hist.bin_width
    res[k] = integral
  return res

def get_fit_func_and_settings_for_muon_type(mu_type):
  if mu_type == "mu+":
    func_fmt = "[0]*exp(-x/[1])"
    initial_settings =(("N_{f}",    lambda x: float(x.GetMaximum()), lambda x: 0.0      , lambda x: x.GetMaximum()**2 ),
                       ("#tau_{f}", lambda x: 2196.9811,             lambda x: 2196.9789, lambda x: 2196.9833         ),)    
  else:
    func_fmt = "[0]*exp(-x/[1]) + [2]*exp(-x/[3])"
    initial_settings =(("N_{f}"    , lambda x: float(x.GetMaximum()/2), lambda x: 0.0      , lambda x: x.GetMaximum()**2 ),
                       ("#tau_{f}" , lambda x: 2196.9811              , lambda x: 2196.9789, lambda x: 2196.9833         ),
                       ("N_{Cu}"   , lambda x: float(x.GetMaximum())  , lambda x: 0.0      , lambda x: x.GetMaximum()**2 ),
                       ("#tau_{Cu}", lambda x: 163.5                  , lambda x: 162.5    , lambda x: 164.5             ),)
  return func_fmt, initial_settings

def run_basic_sim_analysis(filename, mu_type, save_image="", bin_width=100):
  """
  Gets the tree from file, opens it, creates a histogram of dts
  then fits it and if required, draws it. Returns the integrals
  """
  hist_name = get_file_root(filename) # strip the path and the file type
  print "Starting", hist_name
   
  func_fmt, initial_settings = get_fit_func_and_settings_for_muon_type(mu_type)
  
  tree = get_tree_from_file("truth", filename)
  hist = create_histogram_from_tree(hist_name, tree, bin_width, mu_type)
  
  fit_options = "MER" if save_image else "MERN"
  fit_histogram(hist, func_fmt, initial_settings, fit_options, hist_name)
  
  if save_image: save_hist_with_fit(hist, hist_name, save_image)
  
  keys = ("f",) if mu_type == "mu+" else ("f", "Cu") 
  return get_integrals_from_histogram_for_keys(hist, keys=keys)
  
def main():
  treename="truth"
  mu_type = "mu+"
  # mu_type = "mu-"
  filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/100k_mu/%s_5mm_Air_100000.root"%mu_type

  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
  
  res = run_basic_sim_analysis(filename, mu_type)
  for i,k in res.items():
    print i, k
  
if __name__=="__main__":
  main()