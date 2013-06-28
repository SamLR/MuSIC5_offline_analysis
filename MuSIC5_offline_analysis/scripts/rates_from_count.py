#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Calculate simulated muon rates based on truth count of number of muons 
of each type.
"""

from ValueWithError import ValueWithError
from root_utilities import make_canvas
from ROOT import TGraphErrors
from array import array
from time import sleep


# g4bl = True
g4bl = False
n_protons_g4bl = 9e8
n_mu_pos_g4bl  = 86710
n_mu_neg_g4bl  = 9009
n_mu_pos_per_p_g4bl = n_mu_pos_g4bl/n_protons_g4bl

if g4bl:
  n_protons = n_protons_g4bl
else:
  n_protons = 5e5/n_mu_pos_per_p_g4bl

n_mu_neg_to_mu_pos = float(n_mu_neg_g4bl)/n_mu_pos_g4bl


class SimInfo(object):
  """docstring for SimInfo"""
  def __init__(self, deg_dz, n_cu, n_f, n_protons=n_protons):
    super(SimInfo, self).__init__()
    self.deg_dz  = deg_dz
    self.n_cu    = n_cu
    self.n_f     = n_f
    self.n_p     = n_protons
    
  def __str__(self):
    print_fmt = "Degrader: {}, cu: {}, free:{}"
    deg = self.degrader.replace("_", " ")
    return print_fmt.format(deg, self.n_cu, self.n_f)
    
  def __repr__(self):
    print_fmt = "{}: <cu:{} f:{}>"
    return print_fmt.format(self.degrader, self.n_cu, self.n_f)
    
  def get_rate(self, target):
    if target=="f":
      return self.n_f/self.n_p
    elif target=="cu":
      return self.n_cu/self.n_p
    

def get_counts(file_name, g4bl):
  """
  Read the count values from the txt output of analyse_simulation.py
  and return them
  """
  with open(file_name) as in_file:
    # throw away the first two lines of header
    in_file.readline()
    in_file.readline()
    res = {}
    for line in in_file:
      # format: Ai  |   5 |    881±30    |  11722±108   |    965±62    |  11613±220   |    758/1243 
      mat, dz, cu, f, junk, junk2, junk3 = map(str.strip, line.split("|"))
      f = f.split("+/-")
      cu = cu.split("+/-")
      key = float(dz) if mat == "Al" else 0.0
      
      if key not in res: res[key] = {'n_cu':0.0, 'n_f':0.0}
      
      if cu[0] == "na":
        # it's a mu+ measurement
        res[key]["n_cu"] += 0.0
        res[key]["n_f"]  += ValueWithError(*f)
      elif g4bl:
        res[key]["n_cu"] += ValueWithError(*cu)
        res[key]["n_f"]  += ValueWithError(*f) 
      else:
        # it's a mu- measurement so scale it
        res[key]["n_cu"] += ValueWithError(*cu) * n_mu_neg_to_mu_pos
        res[key]["n_f"]  += ValueWithError(*f)  * n_mu_neg_to_mu_pos
        
  for key, counts in res.items():
    res[key] = SimInfo(deg_dz=key, **counts)
  
  return res

def set_graph_values(graph, title, x_title, y_title):
  graph.SetTitle(title)
  graph.GetXaxis().SetTitle(x_title)
  graph.GetXaxis().SetRangeUser(-1.0, 6)
  graph.GetYaxis().SetTitle(y_title)
  
def make_plots(data, img_name):
  """
  make_plot(rates)
  """
  x_order = (0, 0.5, 1, 5)
  x     = array('f', x_order)
  x_er  = array('f', [k*0.01 for k in x_order]) # assumed errors
  cu    = array('f', [data[k].get_rate("cu").value for k in x_order])
  cu_er = array('f', [data[k].get_rate("cu").error for k in x_order])
  f     = array('f', [data[k].get_rate("f").value  for k in x_order])
  f_er  = array('f', [data[k].get_rate("f").error  for k in x_order])
  
  cu_graph = TGraphErrors(len(x), x, cu, x_er, cu_er)
  set_graph_values(cu_graph, "Simulated copper muon rates", "degrader thickness (mm)", "Muons per proton")
  f_graph  = TGraphErrors(len(x), x, f,  x_er, f_er)
  set_graph_values(f_graph, "Simulated free muon rates", "degrader thickness (mm)", "Muons per proton")
  
  canvas = make_canvas("Simulated muon rates (from direct counts)", n_x=2, n_y=1, resize=True)
  canvas.cd(1)
  cu_graph.Draw("ALP")
  canvas.cd(2)
  f_graph.Draw("ALP")
  canvas.Update()
  canvas.SaveAs(img_name+".svg")
  canvas.SaveAs(img_name+".png")
  sleep (5)
  

def run(file_name, g4bl):
  counts = get_counts(file_name, g4bl)
  print "dz  | {:^20s} | {:^20s}".format("cu", "f")
  for key in (0.0, 0.5, 1.0, 5.0):
    print "{} | {} | {}".format(key, counts[key].n_cu,counts[key].n_f)
    
  if g4bl:
    img_name = "images/g4bl_simulated_muon_rates_from_counts"
  else:
    img_name = "images/simulated_muon_rates_from_counts"
  make_plots(counts, img_name) 
  

def main(): 
  if g4bl:
    file_name = "output_txt/g4bl_simulation_counts_and_integrals_loose_f_16ns_bins.txt"
  else:
    file_name = "output_txt/simulation_counts_and_integrals_loose_f_16ns_bins.txt"
  run(file_name, g4bl)

if __name__=="__main__":
  main()