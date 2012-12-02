# Assume using 1uA of current (ie 1,000nA), have 900M protons
# Acceptance is a simple fraction of the total muons
from constants import *
n_initial_protons = 9e8 #1e8
sim_current = 1000 # max current (1uA) in nA
sim_time = float(n_initial_protons*e_charge)/(sim_current*nA)
n_initial_muons = 95719#14321
sim_acceptance = lambda x:float(x)/n_initial_muons
ch_used = 'na' # the simulation doesn't have any channels
sim_run_conditions = {'time':sim_time, 'current':sim_current, # common values
                          'acceptance':sim_acceptance, 'ch_used':(ch_used,)}

print "\n\nSimulated data assumes %i initial protons & %i initial muons\n\n"%(n_initial_protons, n_initial_muons)

if __name__ == '__main__':
  print "### This is a config file ###"
  print "Simulated run conditions"
  for i in sim_run_conditions:
      print "\t% 12s : %s"%(i, str(sim_run_conditions[i])) 
