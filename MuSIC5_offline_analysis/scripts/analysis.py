"""
analysis.py
scripts

Runs the full MuSIC5 analysis.

Created by Sam Cook on 2013-06-03.
"""


from time import time as current_time
from math import pi
from os.path import getmtime as path_last_mod_time, exists as file_exists 
from make_plot_files import generate_histograms

fast = True
hist_dir = "hist_files"

run_ids = {"451":[]}
simulated_degraders = {"5mm_Air":[]}

out_data_file_fmt=hist_dir+"/run{run_id}_hists.root"
out_sim_file_fmt =hist_dir+"/degrader_{degrader}_hists.root"

def recreate_old_hist_files(files_to_check, force=False):
  """
  Check if any of the files are older than their generating script, or
  don't exist. If this is true for any re-run the script
  """
  # TODO Set up look for 'main' in the script and pass file names...
  get_age = lambda path: current_time() - path_last_mod_time(path)
  script_age = get_age("make_plot_files.py")
  needs_regen = lambda path: not file_exists(path) or script_age < get_age(path)
  # regen will be a list of bools showing whether the file exists or is too old
  regen=map(needs_regen, files_to_check)
  if force or any(regen):
    print "Regenerating all files, please wait."
    generate_histograms(run_ids=run_ids, degraders=simulated_degraders)
  
def calculate_missing_metadata():
  # area of U scint/area of beampipe
  acceptance_u_bound = 8*30*380.0/(pi*380.0**2)
  print "Maximum (naive, geometrical) acceptance:", acceptance_u_bound
  
  
  
def fit_run_data():
  pass
def fit_simulation_data():
  pass


def main():
  hist_files = [out_data_file_fmt.format(run_id=r) for r in run_ids] + \
               [out_sim_file_fmt.format(degrader=s) for s in simulated_degraders]
                   
  recreate_old_hist_files(hist_files)
  calculate_missing_metadata()
  fit_run_data()
  fit_simulation_data()

if __name__=="__main__":
  main()