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

def create_histograms_from_tree(name, tree, bin_width):
  lb, ub = -20000, 20000
  nbins = (ub - lb)/bin_width
  hist_args = {"mins":lb, "maxs":ub, "titles":["Time (ns)", "Count"], "bins":nbins}
  hists = {k:make_hist(name+"_"+k, **hist_args) for k in ("f", "cu")}
  
  for entry in tree:
    dts = get_mu_e_dt_for_entry(entry)
    for vertex, times in dts.items():
      for t in times:
        hists[vertex].Fill(t)
  return hists

def get_mu_e_dt_for_entry(entry):
  """
  Returns the first hits by muon and an electron 
  in the up and downstream counters respectively
  """
  # Get all the upstream muons and downstream electrons
  
  mu_pid, e_pid = (13, 11)
  res = {"f":[], "cu":[]}
    
  muons     = get_hits_with(entry, get_pid_counter_filter(mu_pid, 1),\
                            ("trkid", "tof"))
  electrons = get_hits_with(entry, get_pid_counter_filter(e_pid,  3),\
                            ("parentid", "vertex_vol", "tof"))
                            
  for e_parent, e_mu_vertex, e_time in electrons:
    parent_muon = filter(lambda mu: mu[0]==e_parent, muons)
    if parent_muon and (e_time - parent_muon[0][1] > 50):  
    # if parent_muon:  
      key = "cu" if e_mu_vertex==2 else "f"
      res[key].append(e_time - parent_muon[0][1])
      muons.remove(parent_muon[0])
  return res


def fit_histogram(hist, func_fmt, initial_settings, func_name, fit_options="MER"):
  func = get_func_with_named_initialised_param(func_name, hist, func_fmt, initial_settings)
  hist.Fit(func, fit_options)
  hist.func = func
  hist.fit_param = get_fit_parameters(func)

def save_hist_with_fit(hist, name, save_image):
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
  canvas = make_canvas(name)
  hist.Draw()
  hist.func.Draw("SAMES")
  canvas.Update()
  canvas.SaveAs(save_image+".png")
  canvas.SaveAs(save_image+".svg")
  sleep(2)

def get_integrals_from_histogram(hist, key, l_bound=50, u_bound=20000):
  tau, scale = hist.fit_param["tau_"+key], hist.fit_param["N_"+key]
  l_exp, u_exp = [exp(-float(i)/float(tau)) for i in (l_bound, u_bound)] 
  return tau*scale*(l_exp - u_exp) / hist.GetBinWidth(1)

def get_fit_func_and_settings_for_muon_type(fit_type):
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
                  "loose":( 163.5   ,    0.0,    20000.0)}}
                  # "loose":( 163.5   ,    0.0,    1000.0)}}
    return vals[param][fit_type]


  f_vals  = get_setting_vals_for("f",  "loose" if "f"  in fit_type else "tight")
  cu_vals = get_setting_vals_for("cu", "loose" if "cu" in fit_type else "tight")
  
  n_f    = ("N_{f}"    , lambda x: x.GetMaximum()/2, lambda x: 1.0       , lambda x: x.GetMaximum()**2)   
  tau_f  = ("#tau_{f}" , lambda x: f_vals[0]       , lambda x: f_vals[1] , lambda x: f_vals[2])
  n_cu   = ("N_{cu}"   , lambda x: x.GetMaximum()  , lambda x: 1.0       , lambda x: x.GetMaximum()**2)
  tau_cu = ("#tau_{cu}", lambda x: cu_vals[0]      , lambda x: cu_vals[1], lambda x: cu_vals[2])
  return "[0]*exp(-x/[1])", {"cu":(n_cu, tau_cu), "f":(n_f, tau_f)}

def run_vertex_specific_fit(filename, fit_type="tight", save_image="", bin_width=5):
  """
  Gets the tree from file, opens it, creates a histogram of dts
  then fits it and if required, draws it. Returns the integrals
  """
  hist_name = get_file_root(filename) # strip the path and the file type
  print "Starting", hist_name
   
  func_fmt, initial_settings = get_fit_func_and_settings_for_muon_type(fit_type)
  
  tree = get_tree_from_file("truth", filename)
  hists = create_histograms_from_tree(hist_name, tree, bin_width)
    
  fit_options = "MER" if save_image else "MERN"
  res = {"f":0, "cu":0}
  for k, h in hists.items():
    fit_histogram(h, func_fmt, initial_settings[k], fit_options, hist_name+"_"+k)
    res[k] = get_integrals_from_histogram(h, k)
    if save_image: 
      save_hist_with_fit(h, hist_name+"_"+k, save_image+"_"+k)

  return res
  
def main():
  treename="truth"
  mu_type="mu-"
  filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/100k_mu/%s_5mm_Air_500000.root"%mu_type
  # filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/al_target_100000k.root"
  # filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/5mm_Cu_target_100k_mu-.root"
  # filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/MuSIC5_detector/test.root"
  # filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/1M_mu/%s_5mm_Air_1000000.root"%mu_type
  # fit_type="tight"
  fit_type="loose cu f"
  res = run_vertex_specific_fit(filename, fit_type, save_image="modded_g4_"+mu_type+fit_type.replace(" ","_"))
  # res = run_vertex_specific_fit(filename, fit_type, save_image=mu_type+fit_type.replace(" ","_"))
  for i,k in res.items():
    print i, k
  
if __name__=="__main__":
  main()