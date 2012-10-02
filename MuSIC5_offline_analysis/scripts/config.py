tdc_hist_file_name = "music5_tdc_data.root"
# current in nA, time in seconds
files_info = {448:{ 'deg_dz':0,  'time':9221 ,'current':0.0153375  },
              451:{ 'deg_dz':0.5,'time':1001 ,'current':0.0154625  },
              452:{ 'deg_dz':0.5,'time':4944 ,'current':0.013132143},
              455:{ 'deg_dz':1,  'time':6307 ,'current':0.013321429},
              458:{ 'deg_dz':5,  'time':5144 ,'current':0.013625   },
              459:{ 'deg_dz':5,  'time':2452 ,'current':0.012383929}
              }
    
u_channels = tuple(["U%i"%i for i in range(1,9)]) # range(x,y) returns x:(y-1)
d_channels = tuple(["D%i"%i for i in range(1,6)])
all_channels = u_channels + d_channels
 # magic numbers weeee! combination of muon (beam) acceptance 
 # in scint 1 & electron acceptance in scint 2
combined_acceptance = 0.4159891591  
detector_efficiency = 0.5 # FIXME THIS IS A MADE UP NUMBER!  
nA = 1e-9 # scale for nano; i.e. the used proton current
uA = 1e-6 # scale for micro; i.e. the maximum proton current
draw = False
# draw = True

# save_hist = False # save the derived histograms (expensive!)
save_hist = True # save the derived histograms (expensive!)

# lambdas allow dynamically calculated parameters
# form (parameter name, initial value function, [optional] range)
fitting_parameters =(("N_{B}",           lambda hist: float(hist.GetMaximum())/10),               
                     ("N_{#mu_{Cu}}",    lambda hist: float(hist.GetMaximum())),
                     ("#tau_{#mu_{Cu}}", lambda hist: 163.5, 1), # PDG value is  1 
                     ("N_{#mu_{All}}",   lambda hist: float(hist.GetMaximum())/2),
                     ("#tau_{#mu_{All}}",lambda hist: 2000 ))


# t_window_starts = (100,)
# t_window_stops  = (20000,)
# bin_widths      = (10,)  
t_window_starts = (50, 75, 100, 125, 150)  
t_window_stops  = (15000, 20000)
bin_widths      = (10, 50, 100, 200)  # 0 refers to no rebinning

fitting_settings = [(i,j,k) for i in t_window_starts for j in t_window_stops for k in bin_widths]
setting_names = ("fit_lo", "fit_hi", "bin_width")
fitting_settings = [dict(zip(setting_names, i)) for i in fitting_settings]

if __name__ == '__main__':
    print "This is a config file, try again"
