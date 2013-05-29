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

def main():

  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
  filename_fmt = "/Users/scook/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/output/500k_mu/"\
                +"{mu_type}_{degrader}_500000.root"
  degraders = ("5mm_Air", "0.5mm_Aluminium", "1mm_Aluminium", "5mm_Aluminium")
  mu_types  = {"mu+":("f", ), "mu-":("f", "cu")}
  ratio_neg_to_pos_mu = 9009.0/86710.0
  
  # fit_type = "tight"
  fit_type = "loose_f"
  
  counts, integrals = {}, {} 
  res_string = fit_type+"\n"
  for deg in degraders:
    res_string += deg + "\n"
    counts[deg], integrals[deg] = {}, {}
    for mu, keys in mu_types.items():
      filename      = filename_fmt.format(degrader=deg, mu_type=mu)
      print "Count muons in ", filename
      counts[mu]    = run_count_analysis(filename, mu)
      image_name    = "images/sim_{}_{}_{}_500k".format(mu, deg, fit_type)
      print "Fit & integrate"
      integrals[mu] = run_basic_sim_analysis(filename, mu, save_image=image_name)
      
      res_string += "\t" + mu + "\n"
      for k in keys:
        res_string += "\t\t{: >2s} {} {} \n".format(k, counts[mu][k], integrals[mu][k])
  
  print res_string
      
if __name__=="__main__":
  main()