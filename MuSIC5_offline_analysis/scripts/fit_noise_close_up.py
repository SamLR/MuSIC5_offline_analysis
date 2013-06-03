"""

fit_noise.py
scripts

Created by Sam Cook on 2013-05-28.

"""

from time import sleep
from ROOT import gStyle
from root_utilities import get_tree_from_file, make_canvas
from general_utilities import EntryLogger
from data_analysis_core import assign_leaves, make_ch_hists
from analysis_core import get_func_with_named_initialised_param, get_fit_parameters


# Global values
# debug=False
debug=True
# fast=True
fast=False
EntryLogger.enabled=True
data_dir = "../../../converted_Cu_data"
file_fmt = "{dir}/run00{file_id}_converted.root"
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
u_bound=9000
func_fmt = "[0] + [1] * sin((2*pi/[2])*x)"
# func_fmt = "[0] + [1] * sin((2*pi/[2])*(x-[3]))"
# func_fmt = "[0] + [1] * sin((2*pi/[2])*(x-[3])) * sin((2*pi/[4])*(x-[5]))"

@EntryLogger
# 440000 TDC level number of bins
def init_tree(run_info, bins=300):
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
  #       par name        initial val          minimum value      maximum value
  res = (("N_{b}",    lambda x: h_max/10.0, lambda x:    1.0, lambda x:   h_max), # Scale factor
         ("N_{sin}",  lambda x: h_max/20.0, lambda x:    1.0, lambda x:   h_max), # Scale factor
         ("T_{f}",    lambda x:       52.5, lambda x:    0.0, lambda x:  2000.0)) # period
         # ("#phi_{f}", lambda x:        0.0, lambda x:   -0.6, lambda x:     0.6)) # phase  
         # ("T_{f}",    lambda x:     2200.0, lambda x:    0.0, lambda x: 20000.0), # period
         # ("#phi_{f}", lambda x:        0.0, lambda x:   -0.6, lambda x:     0.6)) # phase
  return res       


# def fit_hist(hist, fit_options="ILEMR"):
def fit_hist(hist, fit_options="LR"):
  # I: fit using integral of func (not value @ centre, better for rapid function)
  # L: Loglikelihood (better @ low stats)
  # V: verbose mode
  # E: better errors
  # M: More, improve fit results (looks for alt local minima)
  # R: fit to function range
  def get_fit_goodness(func):
    return  (func.GetChisquare()/func.GetNDF())
  initial_settings = get_initial_settings(hist)
  fit_func = get_func_with_named_initialised_param("f_"+hist.GetTitle(), hist, 
                                                   func_fmt, initial_settings,
                                                   l_bound, u_bound)
  fit_func.SetNpx(10000) # number of points for drawing the function 
  hist.Fit(fit_func, fit_options)
  # best_t = t = initial_settings[2][1](hist)
  # d=0.05
  # min_goodness = goodness = get_fit_goodness(fit_func)
  # while (goodness)>3.0:
  #   t+=d
  #   fit_func.SetParameter(2,t)
  #   hist.Fit(fit_func, fit_options)
  #   goodness = get_fit_goodness(fit_func)
  #   if goodness < min_goodness: 
  #     min_goodness=goodness
  #     best_t = t
  #   if t > (initial_settings[2][1](hist)+ d*100):
  #     print "breaking fit loop, best fit {} for t={}".format(min_goodness, best_t)
  #     break 
      
  hist.fit_func = fit_func
  hist.fit_param = get_fit_parameters(fit_func)

def main():
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
  
  for run in run_info:
    tree = init_tree(run)
    
    fill_hists(tree)
    
    for hist in tree.hists.values():
      print hist.GetTitle(), hist.GetEntries()
      can = make_canvas(hist.GetTitle(),resize=True)
      hist.Draw()
      fit_hist(hist)
      print "\nChi^2/NDF {:.1f} / {}".format(hist.fit_func.GetChisquare(), hist.fit_func.GetNDF()) 
      can.Update()
      can.SaveAs("images/noise_fit_zoom.png")
      if debug:
        sleep(5)
    

if __name__=="__main__":
  main()
  if debug: print "*"*80, "\n\nDebug mode enabled!\n\n", "*"*80