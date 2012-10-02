
sim_data_file_name = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/MuSIC5_detector/scripts/dt_hists.root"


# steal these from config? share them somehow? 
#  merge this to config? 
draw = True
fit_lo = 50
fit_hi = 20000
bin_width = 100 
initial_fit_params = (("N_{B}",           lambda hist: float(hist.GetMaximum())/10),               
                     ("N_{#mu_{Cu}}",    lambda hist: float(hist.GetMaximum())),
                     ("#tau_{#mu_{Cu}}", lambda hist: 163.5, 1), # PDG value is  1 
                     ("N_{#mu_{All}}",   lambda hist: float(hist.GetMaximum())/2),
                     ("#tau_{#mu_{All}}",lambda hist: 2000 ))

save_hist=True
