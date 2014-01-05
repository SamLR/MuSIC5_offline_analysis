"""

fit_noise.py
scripts

Created by Sam Cook on 2013-05-28.

"""

from time import sleep
from ROOT import gStyle, TFile
from root_utilities import get_tree_from_file, make_canvas
from general_utilities import EntryLogger
from data_analysis_core import assign_leaves, make_ch_hists
from analysis_core import get_func_with_named_initialised_param, get_fit_parameters


# Global values
fast=False
debug=False
# debug=True
# fast=True
EntryLogger.enabled=True
data_dir = "../../../converted_Cu_data"
file_fmt = "{dir}/run00{file_id}_converted.root"
out_file_name = "noise_fit_info2.txt"
img_dir = "images/noise_fits/"
img_fmt = img_dir+"{id}_{ch}_noise_fit"
#            filename  target info (mm)
run_info = ({"file_id":"448", "target_dz":5,   "target_mat":"Air"},
            {"file_id":"451", "target_dz":0.5, "target_mat":"Aluminium"},
            {"file_id":"452", "target_dz":0.5, "target_mat":"Aluminium"},
            {"file_id":"455", "target_dz":1,   "target_mat":"Aluminium"},
            {"file_id":"458", "target_dz":5,   "target_mat":"Aluminium"},
            {"file_id":"459", "target_dz":5,   "target_mat":"Aluminium"}) \
            if not debug else \
            ({"file_id":"448", "target_dz":5,   "target_mat":"Air"},)
            # ({"file_id":"455", "target_dz":1,  "target_mat":"Aluminium"},)
            
channels=("D5", "D4", "D3", "D2", "D1") if not debug else ("D1",)
l_bound=8000
u_bound=8600
# u_bound=20000
# func_fmt = "[0] + [1] * sin((2*pi/[2])*x) * sin((2*pi/[3])*x)"
# func_fmt = "[0] + [1] * sin((2*pi/[2])*(x-[3])) * sin((2*pi/[4])*(x-[5]))"
func_fmt = "[0] + [1] * sin((2*pi/[2])*(x-[3]))"

@EntryLogger
# 440000 TDC level number of bins
def init_tree_and_hists(run_info, bins=400):
  filename = file_fmt.format(dir=data_dir, file_id=run_info["file_id"])
  
  tree = get_tree_from_file("Trigger", filename)
  
  for attr, val in run_info.items(): setattr(tree, attr, val)
  
  assign_leaves(tree, channels)
  tree.hists = make_ch_hists(tree, channels, l_bound, u_bound, bins)
  return tree

@EntryLogger
def fill_hists(tree):
  for event_id, event in enumerate(tree):
    if (event_id>2000 and fast): 
      break
    if (event_id%1000000 == 0): 
      print event_id
    for ch in channels:
      for hit in range(int(tree.nHIT[ch]() )):
        tree.hists[ch].Fill( tree.TDC[ch](hit) )

def get_initial_settings(hist):
  h_max = float(hist.GetMaximum())
  print "h max",h_max
  #       par name        initial val          minimum value      maximum value
  res = (("N_{b}",    lambda x: h_max/10.0, lambda x:    1.0, lambda x:   h_max), # Scale factor
         ("N_{sin}",  lambda x: h_max/20.0, lambda x:    1.0, lambda x: h_max/3), # Scale factor
         # ("T_{f}",    lambda x:       59.3, lambda x:   55.0, lambda x:    65.0), # fast period
         ("T_{f}",    lambda x:       59.3, lambda x:    0.0, lambda x:   200.0), # fast period
         # ("T_{f}",    lambda x:       78.4, lambda x:    0.0, lambda x:   100.0), # fast period
         ("#phi_{f}", lambda x:       30.0, lambda x:    0.0, lambda x:    65.0)) # fast phase
         # ("T_{s}",    lambda x:     5130.0, lambda x: 5120.0, lambda x:  5140.0), # slow period
         # ("#phi_{s}", lambda x:     1700.0, lambda x:    0.0, lambda x:  5200.0)) # slow phase
  return res       

def fit_hist(hist, fit_options="LIMER"):
  def get_fit_goodness(func):
    return  (func.GetChisquare()/func.GetNDF())
  initial_settings = get_initial_settings(hist)
  fit_func = get_func_with_named_initialised_param("f_"+hist.GetTitle(), hist, 
                                                   func_fmt, initial_settings,
                                                   l_bound, u_bound)
  fit_func.SetNpx(100000)
  hist.Fit(fit_func, fit_options)
  hist.fit_func = fit_func
  hist.fit_param = get_fit_parameters(fit_func)

def save_fit_info(hist):
  table_fmt = "{run} | {ch} | "+\
             "{N_b.value:>5.0f}+/-{N_b.error:<3.1f} | "     +\
             "{N_sin.value:>4.0f}+/-{N_sin.error:<3.1f} | " +\
             "{T_f.value:>4.1f}+/-{T_f.error:<3.1f} | "     +\
             "{phi_f.value:>4.1f}+/-{phi_f.error:<3.1f} | " +\
             "{chi2:>5.0f} / {ndf:<4d}\n"
  with open(out_file_name, "a") as out_file:
    res = table_fmt.format(run=hist.file_id, ch=hist.ch, **hist.fit_param)
    out_file.write(res)

def save_header():
  # header = ("run",    "ch",    "N_b",  "N_sin",  "T_f",  "phi_f",   "T_s", "phi_s", "Chi^2", "NDF")   
  header = ("run",    "ch",    "N_b",  "N_sin",  "T_f",  "phi_f", "Chi^2", "NDF")   
  table_fmt = "{:3s} | {:2s} | {:^11s} | {:^10s} | {:^10s} | {:^11s} | {:^5s} / {:^4s}\n"
  with open(out_file_name, "w") as out_file:
    res = table_fmt.format(*header)
    out_file.write(res)

def main():
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
  
  save_header()
  root_file = TFile(img_dir + "out.root", "RECREATE");
  for run in run_info:
    tree = init_tree_and_hists(run)
    
    fill_hists(tree)
    
    for ch in channels:
      hist = tree.hists[ch]
      
      root_file.Add(hist);
      print hist.GetTitle(), hist.GetEntries()
      can = make_canvas(hist.GetTitle(),resize=True)
      hist.Draw("E")
      fit_hist(hist)
      # print "\nChi^2/NDF {:.1f} / {}\n\n".format(hist.fit_func.GetChisquare(), hist.fit_func.GetNDF()) 
      can.Update()
      img_name = img_fmt.format(id=hist.file_id, ch=hist.ch)
      can.SaveAs(img_name+".eps")
      can.SaveAs(img_name+".svg")
      if debug:
        sleep(2)
      save_fit_info(hist)
    root_file.Write();
  root_file.Close();

if __name__=="__main__":
  main()
  if debug: print "*"*80, "\n\nDebug mode enabled!\n\n", "*"*80