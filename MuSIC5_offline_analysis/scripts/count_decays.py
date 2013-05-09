"""
 count_decays.py
 Counts the number of decays in a simulated data file
 
 Created by Sam Cook on 2013-05-08.
 Copyright 2013 Sam Cook. All rights reserved.
"""

from analysis_core import get_hits_with, get_pid_counter_filter
from root_utilities import get_tree_from_file
from ValueWithError import ValueWithError

def get_mu_decay_count_from_tree(tree, mu_type):
  res = {"f":0, } if mu_type=="mu+" else {"f":0, "cu":0}
  for entry in tree:
    counts = find_n_decay_pairs_in_entry(entry, mu_type)
    for key in counts:
      res[key] += counts[key]
  return res
  
def get_decay_type(mu_type, decay_vertex):
  if mu_type=="mu-" and decay_vertex==2:
    return "cu"
  else:
    return "f"
    
def find_n_decay_pairs_in_entry(entry, mu_type):
  """
  Finds the number of muon/electron decay pairs with a 
  time difference of greater than 50 ns
  """
  # Get all the upstream muons and downstream electrons
  
  if mu_type=="mu-":
    res = {"f":0, "cu":0}
    mu_pid, e_pid = (13, 11) 
  elif mu_type=="mu+":
    res = {"f":0, }
    mu_pid, e_pid = (-13, -11)
    
  muons     = get_hits_with(entry, get_pid_counter_filter(mu_pid, 1),\
                            ("trkid", "tof"))
  electrons = get_hits_with(entry, get_pid_counter_filter(e_pid,  3),\
                            ("parentid", "vertex_vol", "tof"))

  for e_parent, e_mu_vertex, e_time in electrons:
    parent_muon = filter(lambda mu: mu[0]==e_parent, muons)
    if parent_muon and (e_time - parent_muon[0][1] > 50):  
      key = get_decay_type(mu_type, e_mu_vertex)
      res[key] += 1
      muons.remove(parent_muon[0])
  return res
  
def run_count_analysis(filename, mu_type):
  tree = get_tree_from_file("truth", filename)
  counts  = get_mu_decay_count_from_tree(tree, mu_type)
  res = {}
  for key, n_decays in counts.items():
    res[key] = ValueWithError(n_decays, n_decays**0.5, print_fmt="{: >6.0f} +/- {: <5.0f}")
  return res

def main():
  mu_type="mu-"
  # mu_type="mu+"
  filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/100k_mu/%s_5mm_Air_100000.root"%mu_type
  for key, val in run_count_analysis(filename, mu_type).items():
    print key, val
if __name__=="__main__":
  main()