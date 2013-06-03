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

def create_histogram_from_tree(name, tree, bin_width, mu_type, fast=False):
  lb, ub = -20000, 20000
  nbins = (ub - lb)/bin_width
  hist = make_hist(name, mins=lb,maxs=ub, titles=["Time (ns)", "Count"], bins=nbins)
  hist.bin_width = bin_width
  for entry_id, entry in enumerate(tree):
    if fast and entry_id> 2000:
      break
    time = get_mu_e_dt_for_entry(entry, mu_type)
    for t in time:
      hist.Fill(t)
    # if time:
    #   hist.Fill(time)
  return hist

def get_mu_e_dt_for_entry(entry, mu_type):
  """
  Returns the first hits by muon and an electron 
  in the up and downstream counters respectively
  """
  # Get all the upstream muons and downstream electrons
  
  if mu_type=="mu-":
    mu_pid, e_pid = (13, 11) 
  elif mu_type=="mu+":
    mu_pid, e_pid = (-13, -11)
    
  muons     = get_hits_with(entry, get_pid_counter_filter(mu_pid, 1),\
                            ("trkid", "tof"))
  electrons = get_hits_with(entry, get_pid_counter_filter(e_pid,  3),\
                            ("parentid", "tof"))
  res = []
  for e_parent, e_time in electrons:
    parent_muon = filter(lambda mu: mu[0]==e_parent, muons)
    if parent_muon and (e_time - parent_muon[0][1] > 50):  
      res.append(e_time - parent_muon[0][1])
      muons.remove(parent_muon[0])
  return res

def fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options="MER",img_name=""):
  func = get_func_with_named_initialised_param(func_name, hist, func_fmt, initial_settings)
  
  if img_name:
    canvas = make_canvas(img_name, resize=True)
    hist.Draw()
    hist.Fit(func, fit_options)
    canvas.Update()
    canvas.SaveAs(img_name+".png")
    canvas.SaveAs(img_name+".svg")
  else:
    hist.Fit(func, fit_options+"N")

  hist.func = func
  hist.fit_param = get_fit_parameters(func)

def get_integrals_from_histogram_for_keys(hist, keys, l_bound=50, u_bound=20000):
  res = {}
  for k in keys:
    tau, scale = hist.fit_param["tau_"+k], hist.fit_param["N_"+k]
    l_exp, u_exp = [exp(-float(i)/float(tau)) for i in (l_bound, u_bound)] 
    integral = tau*scale*(l_exp - u_exp) / hist.bin_width
    res[k] = integral
  return res

def get_fit_func_and_settings_for_muon_type(mu_type, fit_type):
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
                  # "loose":( 163.5   ,    0.0,    1000.0)}}
    return vals[param][fit_type]

  f_vals = get_setting_vals_for("f", "loose" if "f" in fit_type else "tight")
  n_f    = ("N_{f}"   , lambda x: x.GetMaximum()/2, lambda x: 1.0      , lambda x: x.GetMaximum()**2)   
  tau_f  = ("#tau_{f}", lambda x: f_vals[0]       , lambda x: f_vals[1], lambda x: f_vals[2])
  
  if mu_type == "mu+":
    return "[0]*exp(-x/[1])", (n_f, tau_f)
  elif mu_type =="mu-":
    cu_vals = get_setting_vals_for("cu", "loose" if "cu" in fit_type else "tight")
    n_cu    = ("N_{cu}",    lambda x: x.GetMaximum(), lambda x: 1.0       , lambda x: x.GetMaximum()**2)
    tau_cu  = ("#tau_{cu}", lambda x: cu_vals[0]    , lambda x: cu_vals[1], lambda x: cu_vals[2])
    return "[0]*exp(-x/[1]) + [2]*exp(-x/[3])", (n_cu, tau_cu, n_f, tau_f)

def run_basic_sim_analysis(filename, mu_type, fit_type, bin_width, save_image="", fast=False):
  """
  Gets the tree from file, opens it, creates a histogram of dts
  then fits it and if required, draws it. Returns the integrals
  """
  hist_name = get_file_root(filename) # strip the path and the file type
  print "running", hist_name
  func_fmt, initial_settings = get_fit_func_and_settings_for_muon_type(mu_type,fit_type)
  
  tree = get_tree_from_file("truth", filename)
  hist = create_histogram_from_tree(hist_name, tree, bin_width, mu_type, fast)
  
  fit_options = "LIMER"
  fit_histogram(hist, func_fmt, initial_settings, func_name=hist_name, fit_options=fit_options, img_name=save_image)
  
  sleep(10)
  
  keys = ("f",) if mu_type == "mu+" else ("f", "cu") 
  return get_integrals_from_histogram_for_keys(hist, keys=keys), hist.fit_param
  
def main():
  treename="truth"
  # mu_type = "mu+"
  mu_type = "mu-"
  filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/100k_mu/%s_5mm_Air_100000.root"%mu_type
  # filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/1M_mu/%s_5mm_Air_1000000.root"%mu_type
  fit_type="loose cu f"
  res = run_basic_sim_analysis(filename, mu_type, fit_type, save_image=mu_type+"_"+fit_type.replace(" ", "_"))
  for i,k in res.items():
    print i, k
  
if __name__=="__main__":
  main()