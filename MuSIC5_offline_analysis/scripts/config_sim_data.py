
# sim_data_file_name = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/MuSIC5_detector/scripts/dt_hists.root"
tdc_hist_file_name = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/MuSIC5_detector/scripts/dt_hists.root"


# steal these from config? share them somehow? 
#  merge this to config? 
draw = True
fit_lo = (50,)
fit_hi = (20000,)
bin_width = (100,) 
# fit_lo = (50, 100, 150)
# fit_hi = (20000,)
# bin_width = (50, 100, 200) 
settings = [(i,j,k) for i in fit_lo for j in fit_hi for k in bin_width]
initial_fit_params = (("N_{B}",          lambda hist: float(hist.GetMaximum())/10),               
                     ("N_{#mu_{Cu}}",    lambda hist: float(hist.GetMaximum())),
                     ("#tau_{#mu_{Cu}}", lambda hist: 163.5, 1), # PDG value is  1 
                     ("N_{#mu_{All}}",   lambda hist: float(hist.GetMaximum())/2),
                     ("#tau_{#mu_{All}}",lambda hist: 2000 ))

# Assume using 1uA of current (ie 1,000nA), have 100M protons ~16us of beam
# Acceptance is 1 as this is a 'perfect' simulation
sim_time = 0.000016
sim_current = 1000
sim_acceptance = 1
hist_keys = ("Air_5mm", "Aluminium_0.5mm", "Aluminium_1mm", 
             "Aluminium_5mm", "Aluminium_8mm", "Aluminium_12mm")

make_value = lambda x:{'deg_dz':x.split('_')[1], 'material':x.split('_')[0], \
                    'time':sim_time, 'current':sim_current, 'acceptance':sim_acceptance}

files_info = {i:make_value(i) for i in hist_keys}

save_hist=False
# save_hist=True
