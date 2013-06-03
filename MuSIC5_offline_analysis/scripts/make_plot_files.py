"""
make_plot_files.py
scripts

Generates two sets of files. Each file contains one histogram 
per channel of ToF information.

Data files are on a per run basis whilst simulation files are
the combination of a mu+ and a mu- file scaled appropriately 
(currently 86710:9009).

Created by Sam Cook on 2013-06-02.
"""

from data_analysis_core import assign_leaves
from analysis_core import fill_hist_with_mu_e_times
from root_utilities import get_tree_from_file, make_hist, make_canvas
from ROOT import TFile
from time import sleep

# fast = True
fast = False
break_entry=20000

bin_width = 1 # use 1ns bins. Hists can be rebinned as required
l_bound, u_bound = -20000.0, 20000.0
neg_pos_ratio = 9009.0/86710.0

in_data_file_fmt="../../../converted_Cu_data/run00{run_id}_converted.root"
in_sim_file_fmt="../../../../simulation/MuSIC_5_detector_sim/MuSIC5/output/500k_mu/"+\
                "mu{charge}_{degrader}_500000.root"
                
out_data_file_fmt="hist_files/run{run_id}_hists.root"
out_sim_file_fmt="hist_files/degrader_{degrader}_hists.root"

channels = ("D1", "D2", "D3", "D4", "D5") if not fast else ("D5",)

data_run_ids = ("448", "451", "452","455", "458", "459") if not fast else ("451",)
simulated_degraders = ("0.5mm_Aluminium",
                       "1mm_Aluminium",
                       "5mm_Air",
                       "5mm_Aluminium",) if not fast else ("5mm_Air",)

hist_settings = {'mins':l_bound, 'maxs':u_bound, 'titles':("TDC-TDC0 (ns)", "Count")}
hist_settings['bins'] = int((u_bound - l_bound)/bin_width)

def generate_data_histograms(run_id):
  # Open the input file & init the tree
  print "Starting run", run_id
  in_file_name = in_data_file_fmt.format(run_id=run_id)
  tree = get_tree_from_file("Trigger", in_file_name)
  assign_leaves(tree, channels)
  
  # Create the file to write to
  out_file_name = out_data_file_fmt.format(run_id=run_id)
  out_file = TFile(out_file_name, "RECREATE")
  
  # Make the histograms & fill them
  hists = {ch:make_hist(ch, **hist_settings) for ch in channels}
  fill_data_hists (tree, hists)
  save_file(out_file)

def save_file(file_to_save):
  #Save everything
  file_to_save.Print()
  file_to_save.Write()
  file_to_save.Close()

def is_break_time(entry_id, log_xth):
  if entry_id>break_entry and fast:
    print "Quick exit"
    return True
  elif int(entry_id%int(log_xth)) == 0:
    print entry_id
  return False

def fill_data_hists (tree, hists):
  tenth = int(tree.GetEntries()/10)
  for entry_id, entry in enumerate(tree):
    if is_break_time(entry_id, tenth): 
      break
    for ch in channels:
      n_hits = int(tree.nHIT[ch]())
      for hit in range(n_hits):
        tdc = tree.TDC[ch](hit)
        hists[ch].Fill(tdc)
  
def generate_sim_histograms(degrader):
  print "Starting simulation of", degrader
  
  charges = {"+":"pos_"+degrader,"-":"neg_"+degrader}
  
  out_file_name = out_sim_file_fmt.format(degrader=degrader)
  out_file = TFile(out_file_name, "RECREATE")
  
  hists = {c:make_hist(charges[c], **hist_settings) for c in charges}
  hists['combined'] = make_hist("combined_"+degrader,**hist_settings)
  for c in charges:
    in_file_name = in_sim_file_fmt.format(charge=c, degrader=degrader)
    tree = get_tree_from_file("truth",in_file_name)
    fill_sim_hists (tree, hists[c], c)
    
  # combined = 1.0*h_mu_pos + 9009/86710*h_mu_neg
  hists['combined'].Add(hists['+'], hists['-'], 1.0, neg_pos_ratio)
  save_file(out_file)

def fill_sim_hists (tree, hist, charge):
  tenth = int(tree.GetEntries()/10)
  for entry_id, entry in enumerate(tree):
    if is_break_time(entry_id, tenth): break
    fill_hist_with_mu_e_times(hist, entry, charge)

def generate_histograms(run_ids, degraders):
  
  for r in run_ids:
    generate_data_histograms(r)
  
  for d in degraders:
    generate_sim_histograms(d)

def main():
  generate_histograms(run_ids=data_run_ids, degraders=simulated_degraders)
  

if __name__=="__main__":
  main()