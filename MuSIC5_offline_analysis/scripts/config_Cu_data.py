u_channels = tuple(["U%i"%i for i in range(1,9)]) # range(x,y) returns x:(y-1)
d_channels = tuple(["D%i"%i for i in range(1,6)])
all_channels = u_channels + d_channels

files_info = {448:{ 'run_conditions': 
                    {'deg_dz':0,  'time':9221, 'current':0.0153375  , 'acceptance':0.087, 'ch_used':d_channels},
                  },
              451:{ 'run_conditions':
                    {'deg_dz':0.5,'time':1001, 'current':0.0154625  , 'acceptance':0.077, 'ch_used':d_channels},
                  },
              452:{ 'run_conditions':
                    {'deg_dz':0.5,'time':4944, 'current':0.013132143, 'acceptance':0.077, 'ch_used':d_channels},
                  },
              455:{ 'run_conditions':
                    {'deg_dz':1,  'time':6307, 'current':0.013321429, 'acceptance':0.069, 'ch_used':d_channels},
                  },
              458:{ 'run_conditions':
                    {'deg_dz':5,  'time':5144, 'current':0.013625   , 'acceptance':0.045, 'ch_used':d_channels},
                  },
              459:{ 'run_conditions':
                    {'deg_dz':5,  'time':2452, 'current':0.012383929, 'acceptance':0.045, 'ch_used':d_channels},
                  }
              }

 # magic numbers weeee! combination of muon (beam) acceptance 
 # in scint 1 & electron acceptance in scint 2

if __name__ == '__main__':
  print "### This is a config file ###"
  print "Run conditions:"
  for i in files_info:
      print "\t%i:"%i
      for j in files_info[i]:
          print "\t\t% 10s : %s" %(j, str(files_info[i][j]))
