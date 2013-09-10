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
break_entry=2000
# neg_pos_ratio = 9009.0/86710.02

# exec_d4_d5 = False
exec_d4_d5 = True

in_data_file_fmt="../../../converted_Cu_data/run00{run_id}_converted.root"
in_sim_dir="../../../../simulation/MuSIC_5_detector_sim/MuSIC5/output/"   
in_sim_g4bl_file_fmt=in_sim_dir+"final/final_st_Copper_0.5mm_deg_{degrader}.root"
in_sim_file_fmt=in_sim_dir+"500k_mu/mu{charge}_{degrader}_500000.root"

if exec_d4_d5:             
  out_data_file_fmt="hist_files_offset_exec_d4_d5/run{run_id}_hists.root"
  out_sim_file_fmt="hist_files_offset_exec_d4_d5/degrader_{degrader}_hists.root"
  out_sim_g4bl_file_fmt="hist_files_offset_exec_d4_d5/degrader_{degrader}_g4bl_hists.root"
else:
  out_data_file_fmt="hist_files_offset/run{run_id}_hists.root"
  out_sim_file_fmt="hist_files_offset/degrader_{degrader}_hists.root"
  out_sim_g4bl_file_fmt="hist_files_offset/degrader_{degrader}_g4bl_hists.root"
  
channels = (("D1", 74), ("D2", 86), ("D3", 87), ("D4", 117), ("D5", 127)) if not fast else (("D5", 127),)

data_run_ids = ("448", "451", "452","455", "458", "459") if not fast else ("451",)
degraders = ("0.5mm_Aluminium", "1mm_Aluminium", "5mm_Air", "5mm_Aluminium",) if not fast else ("5mm_Air",)
                       

l_bound, u_bound = -20000.0, 20000.0
bin_width = 1 # use 1ns bins. Hists can be rebinned as required
hist_settings = {'mins':l_bound, 'maxs':u_bound, 'titles':("TDC-TDC0 (ns)", "Count")}
hist_settings['bins'] = int((u_bound - l_bound)/bin_width)

def generate_data_histograms(run_id):
  # Open the input file & init the tree
  print "Starting run", run_id
  in_file_name = in_data_file_fmt.format(run_id=run_id)
  tree = get_tree_from_file("Trigger", in_file_name)
  assign_leaves(tree, [c[0] for c in channels]) # use comprehension to make a list of just the channels
  
  # Create the file to write to
  out_file_name = out_data_file_fmt.format(run_id=run_id)
  out_file = TFile(out_file_name, "RECREATE")
  
  # Make the histograms & fill them
  hists = {ch[0]:make_hist(ch[0], **hist_settings) for ch in channels}
  fill_data_hists (tree, hists)
  save_file(out_file)

def save_file(file_to_save):
  #Save everything
  file_to_save.Print()
  file_to_save.Write()
  file_to_save.Close()

def is_break_time(entry_id, log_xth):
  if fast and entry_id>break_entry:
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
    for ch, offset in channels:
      n_hits = int(tree.nHIT[ch]())
      for hit in range(n_hits):
        tdc = tree.TDC[ch](hit)
        hists[ch].Fill(tdc+offset)
  
def generate_sim_histograms(degrader, g4bl, exec_d4_d5):
  print "Starting simulation of", degrader, "g4bl:", g4bl
  if g4bl:
    out_file_name = out_sim_g4bl_file_fmt.format(degrader=degrader)
  else:
    out_file_name = out_sim_file_fmt.format(degrader=degrader)
  
  out_file = TFile(out_file_name, "RECREATE")
  
  charges = {"+":"pos_"+degrader,"-":"neg_"+degrader}
  hists = {c:make_hist(charges[c], **hist_settings) for c in charges}
  hists['combined'] = make_hist("combined_"+degrader,**hist_settings)
  
  if g4bl:
    in_file_name = in_sim_g4bl_file_fmt.format(degrader=degrader)
    tree = get_tree_from_file("truth",in_file_name)
    fill_g4bl_hists (tree, hists["+"], hists["-"], exec_d4_d5)
    hists['combined'].Add(hists['+'], hists['-'])
  else:
    neg_pos_ratio = get_g4bl_decay_ratio(degrader)
    for c in charges:
      in_file_name = in_sim_file_fmt.format(charge=c, degrader=degrader)
      tree = get_tree_from_file("truth",in_file_name)
      fill_sim_hist (tree, hists[c], c, exec_d4_d5)
    hists['combined'].Add(hists['+'], hists['-'], 1.0, neg_pos_ratio)
    # hists['combined'].Add(hists['+'], hists['-'], 1.0, neg_pos_ratio)
    
  save_file(out_file)

def fill_g4bl_hists (tree, pos_hist, neg_hist, exec_d4_d5):
  tenth  = int(tree.GetEntries()/10)
  for entry_id, entry in enumerate(tree):
    if is_break_time(entry_id, tenth): break
    fill_hist_with_mu_e_times(pos_hist, entry, "+", exec_d4_d5)
    fill_hist_with_mu_e_times(neg_hist, entry, "-", exec_d4_d5)
  

def fill_sim_hist (tree, hist, charge, exec_d4_d5):
  tenth = int(tree.GetEntries()/10)
  for entry_id, entry in enumerate(tree):
    if is_break_time(entry_id, tenth): break
    fill_hist_with_mu_e_times(hist, entry, charge, exec_d4_d5)

def get_g4bl_decay_ratio(degrader):
  """
  Returns the ratio of negative to positive decayse in the 
  equivalent g4bl simulation.
  """
  file_name = out_sim_g4bl_file_fmt.format(degrader=degrader)
  file = TFile(file_name, "READ")
  if not file.IsOpen():
    msg = "File {} not found, it may need recreating".format(file_name)
    raise Exception(msg)
  pos_hist = file.Get("pos_"+degrader)
  neg_hist = file.Get("neg_"+degrader)
  n_pos = pos_hist.GetEntries()
  n_neg = neg_hist.GetEntries()
  file.Close()
  return float(n_neg)/n_pos

def main():
  # for r in data_run_ids:
  #   generate_data_histograms(r)
  generate_data_histograms( "448" )
  # generate_sim_histograms("5mm_Air", True, exec_d4_d5)
  # for d in degraders:
  #   generate_sim_histograms(d, True, exec_d4_d5)
  #   generate_sim_histograms(d, False, exec_d4_d5)
  

if __name__=="__main__":
  main()