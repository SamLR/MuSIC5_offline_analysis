


# Assume using 1uA of current (ie 1,000nA), have 100M protons ~16us of beam
# Acceptance is 1 as this is a 'perfect' simulation
sim_time = 0.000016
sim_current = 1000
sim_acceptance = 1
ch_used = 'na' # the simulation doesn't have any channels
sim_run_conditions = {'time':sim_time, 'current':sim_current, # common values
                          'acceptance':sim_acceptance, 'ch_used':(ch_used,)}


if __name__ == '__main__':
  print "### This is a config file ###"
  print "Simulated run conditions"
  for i in sim_run_conditions:
      print "\t% 12s : %s"%(i, str(sim_run_conditions[i])) 
