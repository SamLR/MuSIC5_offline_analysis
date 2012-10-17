#!/usr/bin/env python
# encoding: utf-8
"""
count_muons.py

Created by Sam Cook on 2012-07-23.
Copyright (c) 2012 . All rights reserved.
"""

from root_utilities import set_bin_val_er_label, get_canvas_with_hists
                      
from list_utilities import add_as_sub_dict, create_sub_dicts_from_keys

from fitting import fit_hist

from constants import uA, nA, detector_efficiency, n_protons_per_amp

def settings_str(fit_lo, fit_hi, bin_width):
 return "lo_%i_hi_%i_bins_%i"%(fit_lo, fit_hi, bin_width)


def calc_muon_yield_at_1uA(n_mu, n_mu_er, acceptance, time, current, scale=uA, **kwargs ):
    """Convert number of muons & error to a yield per A proton current"""
    # using 'kwargs' means we pass "**files_info['run_conditions']" and 
    # all excess parameters get ignored
    x = detector_efficiency * acceptance * time * current *nA
    mu_yield = float(n_mu) / x
    mu_yield_er = float(n_mu_er) / x
    return mu_yield*uA, mu_yield_er*uA   


def convert_current_to_protons(current):
    return current * n_protons_per_amp * nA


def sum_muons_over_all_ch(ch_dict):
    n_muons = 0
    squared_errors = []
    for ch_dat in ch_dict.values():
        n_muons += ch_dat['n_mu_cu'][0] + ch_dat["n_mu_slow"][0]
        squared_errors.append(ch_dat['n_mu_cu'][1]**2 )
        squared_errors.append(ch_dat["n_mu_slow"][1]**2 )
    return n_muons, sum(squared_errors)**0.5


def calculate_derived_values(files_info, initial_fit_params, fit_settings):
    """
    Workhorse function, reads the TDC file, fits the histograms & calculates integrals 
    """
    setting_str = settings_str(**fit_settings)
    print setting_str
    for file_id in files_info:
        print "file id:", file_id
        add_as_sub_dict(files_info[file_id], 'fit_settings', setting_str, fit_settings)
        file_res = {'ch_dat':{}}
        
        for ch_str in files_info[file_id]['run_conditions']['ch_used']:
            # upstream scintillators are not calibrated to detect decay electrons well so skip them
            hist = files_info[file_id]['hists'][ch_str]
            fit_results = fit_hist(hist, initial_fit_params, **fit_settings)
            file_res['ch_dat'][ch_str] = fit_results
        
        n_mu, n_mu_er   = sum_muons_over_all_ch(file_res['ch_dat'])
        mu_yield, mu_yield_er = calc_muon_yield_at_1uA(n_mu, n_mu_er, 
                                        **files_info[file_id]['run_conditions'])
        file_res['total_muons'] = (n_mu, n_mu_er)
        file_res['muon_yields'] = (mu_yield, mu_yield_er)
        
        add_as_sub_dict(files_info[file_id], 'fits', setting_str, file_res)


# def main():
#     # files_info and channels info is importated
#     tdc_file = get_tdc_file_dict(tdc_hist_file_name, files_info, all_channels)
#     gStyle.SetOptFit()
#     gStyle.SetOptStat(0)
#     sleep_time = 30
#     # TODO look through variable names and improve
#     # specifically 'files_info' and the fit parameter names (e.g. N_b->C_b)
#     
#     # from this point it shouldn't matter if it's data or sim_data
#     for settings in fitting_settings:
#         set_name = settings_str(**settings)
#         print "*"*40, "\n\nSettings now: ", settings, "\n"
#         get_derived_values(files_info, fitting_parameters, settings, save_hist=save_hist)        
#             
#     
#     # for general checking, save the final state of files_info
#     with open("file_info.txt", "write") as log_file:
#         # TODO write a proper logger
#         saveTraverse(files_info, log_file,header="# Current state of file_info")
#         
#     hists= get_hists_fitting_parameter_vs_setting(files_info, "n_bkgnd")
#     ch_id_hists = create_sub_dicts_from_keys(hists,
#                 keysplit_function=lambda x: (x.split('+')[1], x.split('+')[2]))
#     canvas = get_canvas_with_hists(ch_id_hists)
#                                 
#     # hists1= get_hists_fitting_parameter_vs_deg_dz(files_info, "n_bkgnd")
#     # setting_ch_hists = create_sub_dicts_from_keys(hists1,
#     #             keysplit_function=lambda x: (x.split('+')[1], x.split('+')[2]))
#     # canvas = get_canvas_with_hists(setting_ch_hists)
#     #                             
#     # hists2= get_hists_file_val_vs_setting(files_info, "muon_yields")
#     # canvas = get_canvas_with_hists(hists2)
#     # 
#     # hists3= get_hists_file_val_vs_deg_dz(files_info, "muon_yields")
#     # canvas = get_canvas_with_hists(hists3)
#     
#     sleep (sleep_time)



if __name__ == '__main__':
    main()

