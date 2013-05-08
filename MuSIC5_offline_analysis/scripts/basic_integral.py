""" 
  A very simple and inclusive (hopefully) attempt at analysing the 
  simulated data for MuSIC 5
  simple_sim_analysis.py
  scripts
  
  Created by Sam Cook on 2013-05-07.
  Copyright 2013 Sam Cook. All rights reserved.
 
"""

from analysis_core import first_upstream_step_of_a_mu_plus, \
                          first_downstream_step_of_an_e_plus, \
                          get_hits_with, get_func_with_named_initialised_param, \
                          get_fit_parameters
from root_utilities import make_hist, make_canvas, get_tree_from_file
from ROOT import gStyle
from time import sleep
from math import exp

def create_histogram_from_tree(name, tree, bin_width):
  lb, ub = -20000, 20000
  nbins = (ub - lb)/bin_width
  hist = make_hist(name, mins=lb,maxs=ub, titles=["Time (ns)", "Count"], bins=nbins)
  hist.bin_width = bin_width
  for entry in tree:
    time = get_mu_e_dt(entry)
    if time:
      hist.Fill(time)
  return hist

def get_mu_e_dt(entry):
  """
  Returns the first hits by muon and an electron 
  in the up and downstream counters respectively
  """
  # Get all the upstream muons and downstream electrons
  muons     = get_hits_with(entry, mu_track_and_time)
  electrons = get_hits_with(entry, e_parent_and_time)
  
  muons, electrons = get_muon_electron_decay_times(muons, electrons)
  
  if len(electrons)>0 and len(muons)>0:
    # Finally get the times
    start_time = min([m[1] for m in muons])
    stop_time  = min([e[1] for e in electrons])
    return stop_time - start_time  
  else: 
    return False

# functions to get us muons and electrons
def mu_track_and_time(entry, hit):
  if first_upstream_step_of_a_mu_plus(entry, hit):
    return entry.trkid[hit], entry.tof[hit]
  else:
    return False
    
def e_parent_and_time(entry, hit):
  if first_downstream_step_of_an_e_plus(entry, hit):
    return entry.parentid[hit], entry.tof[hit]
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

def fit_histogram(hist, func_fmt, initial_settings, fit_options="MER"):
  # FIXME change name to be more descriptive
  func = get_func_with_named_initialised_param("func", hist, func_fmt, initial_settings)
  hist.Fit(func, fit_options)
  hist.func = func
  hist.fit_param = get_fit_parameters(func)

def draw_hist_with_fit(hist, name):
  canvas = make_canvas(name)
  hist.Draw()
  canvas.Update()
  return canvas

def get_integrals_from_histogram(hist, l_bound=50, u_bound=20000):
  # tau and scale have type ValuesWithError
  tau, scale = hist.fit_param["tau_f"], hist.fit_param["N_f"]
  exp_bit = exp(-float(l_bound)/tau.value) - exp(-float(u_bound)/tau.value)
  return tau*scale*exp_bit/hist.bin_width

def main():
  treename="truth"
  filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/100k_mu/mu+_5mm_Air_100000.root"
  func_fmt = "[0]*exp(-x/[1])"
  initial_settings =(("N_{f}",    lambda x: float(x.GetMaximum()), lambda x: 0.0      , lambda x: x.GetMaximum()**2 ),
                     ("#tau_{f}", lambda x: 2196.9811,             lambda x: 2196.9789, lambda x: 2196.9833         ),)
  bin_width = 100 # ns
  draw_mode = False
  if draw_mode:
    gStyle.SetOptStat(10)
    gStyle.SetOptFit(111)
                     
  tree = get_tree_from_file(treename, filename)
  
  hist = create_histogram_from_tree("test",tree, bin_width)

  fit_options = "MER" if draw_mode else "MERN"
  fit_histogram(hist, func_fmt, initial_settings)
  
  if draw_mode:
    canvas = draw_hist_with_fit(hist, "c")
    canvas.SaveAs("images/test.png")
  print get_integrals_from_histogram(hist)
  

if __name__=="__main__":
  main()