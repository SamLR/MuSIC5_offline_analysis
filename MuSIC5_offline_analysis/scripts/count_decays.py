"""
 count_decays.py
 Counts the number of decays in a simulated data file
 
 Created by Sam Cook on 2013-05-08.
 Copyright 2013 Sam Cook. All rights reserved.
"""

from analysis_core import first_upstream_step_of_a_mu_plus, \
                          first_downstream_step_of_an_e_plus
from root_utilities import get_tree_from_file

def get_mu_decay_count_from_tree(tree):
  count = 0
  for entry in tree:
    u_mu_ids = []
    d_e_ids_and_vertex = []
    for hit in range(entry.nhit):
      if first_upstream_step_of_a_mu_plus(entry, hit):
        u_mu_ids.append(entry.trkid[hit])
      elif first_downstream_step_of_an_e_plus(entry,hit):
        origin = (entry.parentid[hit], entry.vertex_vol[hit])
        d_e_ids_and_vertex.append(origin)
    
    for parent, vertex in d_e_ids_and_vertex:
      if parent in u_mu_ids:
        # currently ignoring vertex info
        count += 1
        u_mu_ids.remove(parent)
  return count
  
def main():
  treename="truth"
  filename="/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/100k_mu/mu+_5mm_Air_100000.root"
  tree = get_tree_from_file(treename, filename)
  n_decays = get_mu_decay_count_from_tree(tree)
  print n_decays, n_decays**0.5
  print "ADD 50ns exclusion"

if __name__=="__main__":
  main()