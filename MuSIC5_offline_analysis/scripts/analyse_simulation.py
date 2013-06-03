"""
analyse_simulation.py
scripts

Runs the count & integral scripts on all simulations

Created by Sam Cook on 2013-05-10.
Copyright 2013 Sam Cook. All rights reserved.

"""

from ROOT import gStyle
from count_decays import run_count_analysis
from basic_integral import run_basic_sim_analysis


fast=False
# fast=True
# bin_width=10
bin_width=100
degraders = ("5mm_Air", "0.5mm_Aluminium", "1mm_Aluminium", "5mm_Aluminium")
mu_types  = {"mu+":("f", ), "mu-":("f", "cu")}
ratio_neg_to_pos_mu = 9009.0/86710.0

# fit_type = "tight"
fit_type = "loose_f"
# fit_type = "loose_cu"
# fit_type = "loose_cu_f"
img_file_fmt = "images/sim_{mu_type}_{degrader}_{fit_type}_{bin_width}ns_bins_500k"
filename_fmt = "/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/500k_mu/{mu_type}_{degrader}_500000.root"
out_file_fmt = "simulation_counts_and_integrals_{fit_type}_{bin_width}ns_bins.txt"

def save_count_integral(filename, material, dz, count, integral, chi2, ndf, *args, **kwargs):
  table_fmt = "{mat:3s} | {dz:>3s} | "+\
              "{count[0]} | {count[1]} | {integral[0]} | {integral[1]} | " +\
              "{chi2:>6.0f}/{ndf:<5.0f}\n"
  val_fmt = "{:>6.0f}\xb1{:<5.0f}"
  na = "{:12s}".format("na")
  if "cu" in count:
    count    = [count['cu'], count['f']]
    integral = [integral['cu'], integral['f']]
    for c,i in zip(count, integral):
      c.print_fmt = val_fmt
      i.print_fmt = val_fmt
  else:
    count = [na,count['f']]
    count[1].print_fmt = val_fmt
    integral = [na, integral['f']]
    integral[1].print_fmt = val_fmt
  
  with open(filename, "a") as out_file:
    res = table_fmt.format(mat=material, dz=dz, count=count, integral=integral, chi2=chi2, ndf=ndf)
    out_file.write(res)

def save_header(filename):
  table_1 = "{:^3s} | {:^3s} | {:^27s} | {:^27s} | {:>6s}/{:<5s}\n"
  table_2 = "    |     | {:^12s} | {:^12s} | {:^12s} | {:^12s} | {:12s}\n"
  entries_1 = ("mat", "dz", "count", "integral", "Chi^2", "NDF")
  entries_2 = ("cu", "f", "cu", "f", "")
  with open(filename, "w") as out_file:
    out_file.write(table_1.format(*entries_1))
    out_file.write(table_2.format(*entries_2))
    
def get_mat_and_dz(degrader):
  dz, mat = degrader.split("_")
  return dz[:-2], mat[:2]

def get_file_and_image_name(degrader, mu_type):
  file_name   = filename_fmt.format(degrader=degrader, mu_type=mu_type)
  image_name = img_file_fmt.format(mu_type=mu_type, degrader=degrader, fit_type=fit_type, bin_width=bin_width)
  return file_name, image_name
  
def main():
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
                
  out_file_name = out_file_fmt.format(fit_type=fit_type, bin_width=bin_width)
  save_header(out_file_name)
  
  for deg in degraders:
    for mu_charge, keys in mu_types.items():
      file_name, image_name  = get_file_and_image_name(deg, mu_charge)
      print "Started:", file_name.split("/")[-1]
      count = run_count_analysis(file_name, mu_charge)
      integral, fit_param = run_basic_sim_analysis(file_name, mu_charge, \
                                                          fit_type=fit_type, bin_width=bin_width, \
                                                          save_image=image_name, fast=fast)
      dz, mat = get_mat_and_dz(deg)
      save_count_integral(out_file_name, mat, dz, count, integral, **fit_param)
      
      
if __name__=="__main__":
  main()