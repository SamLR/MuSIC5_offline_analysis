#!/usr/bin/env python
# encoding: utf-8
"""
count_muons.py

Created by Sam Cook on 2012-07-23.
Copyright (c) 2012 . All rights reserved.
"""

from ROOT import TH1F, TFile, TF1, gStyle, gPad

from root_utilities import make_hist, make_canvas, set_bin_val_er_label,\
                            get_canvas_with_hists
                      
from list_utils import add_as_sub_dict, saveTraverse, printTraverse, \
                        create_sub_dicts_from_keys

from general_utilities import wait_to_quit, get_quantised_width_height

from tdc_file import get_tdc_file

from fitting import fit_hist

# TODO reduce this to "file_info", "run_settings", "fit_settings"
from config import files_info, tdc_hist_file_name, u_channels, d_channels, \
                    all_channels, draw, save_hist, fitting_parameters, \
                    fitting_settings
    
from constants import uA, nA, detector_efficiency, n_protons_per_amp    

from sys import maxint             
    

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


def settings_str(fit_lo, fit_hi, bin_width):
    return "lo_%i_hi_%i_bins_%i"%(fit_lo, fit_hi, bin_width)


def get_hists_fitting_parameter_vs_settings(files_info, parameter):
    # setting strings could be culled from the files info but would 
    # come out in a less than useful order
    """
    Generate plots of the fitting parameter (e.g. '#Tau_{#mu_{Cu}}')
    against the settings used to generate the fit. 
    
    Produces a single canvas of one plot per channel; each
    channel's entry displays the values for all settings grouped by 
    file.
    """
    # simple wrapper for make hist with the required defaults
    make_settings_hist = lambda name, n_settings: make_hist(name, 0, n_settings, 'Fit settings', parameter)
    get_hist_key = lambda file_id, ch_id: "%s_file_%s_ch_%s"%(parameter, str(file_id), ch_id)
    hists = {}
    
    for file_id in files_info:
        fits = files_info[file_id]['fits']
        n_settings = len(fits)
        
        for ch_id in files_info[file_id]['run_conditions']['ch_used']:
            hist_key = get_hist_key(file_id, ch_id)
            hists[hist_key] = make_settings_hist(hist_key, n_settings)
            
            for bin, setting_str in enumerate(fits, 1):
            # bin 0 == underflow. bin number != x_axis value
                ch_dat = fits[setting_str]['ch_dat'][ch_id]
                
                val, er  = ch_dat[parameter]                
                if parameter=="chi2":
                    val = float(val)/er # express chi2 as chi2/NDF
                    er = 0.0
                
                set_bin_val_er_label(hists[hist_key], bin, val, er, setting_str)
    return hists


def get_derived_values(files_info, initial_fit_params, fit_lo, fit_hi, bin_width, save_hist=False):
    """
    Workhorse function, reads the TDC file, fits the histograms & calculates integrals 
    """
    setting_str = settings_str(fit_lo, fit_hi, bin_width)
    for file_id in files_info:
        file_res = {'ch_dat':{}}
        for ch_str in files_info[file_id]['run_conditions']['ch_used']:
            # upstream scintillators are not calibrated to detect decay electrons well so skip them
            
            hist = files_info[file_id]['hists'][ch_str]
            fit_results = fit_hist(hist, fit_lo, fit_hi, bin_width, initial_fit_params)
            file_res['ch_dat'][ch_str] = fit_results
            
        n_mu, n_mu_er   = sum_muons_over_all_ch(file_res['ch_dat'])
        mu_yield, mu_yield_er = calc_muon_yield_at_1uA(n_mu, n_mu_er, 
                                        **files_info[file_id]['run_conditions'])
        
        file_res['total_muons'] = (n_mu, n_mu_er)
        file_res['muon_yields'] = (mu_yield, mu_yield_er)
        
        add_as_sub_dict(files_info[file_id], 'fits', setting_str, file_res)


def main():
    # files_info and channels info is importated
    tdc_file = get_tdc_file(tdc_hist_file_name, files_info, all_channels)
    gStyle.SetOptFit()
    gStyle.SetOptStat(0)
    # TODO look through variable names and improve
    # specifically 'files_info' and the fit parameter names (e.g. N_b->C_b)
    
    
    for settings in fitting_settings:
        set_name = settings_str(**settings)
        print "*"*40, "\n\nSettings now: ", settings, "\n"
        get_derived_values(files_info, fitting_parameters, save_hist=save_hist, **settings)        
            
    
    # for general checking, save the final state of files_info
    with open("file_info.txt", "write") as log_file:
        # TODO write a proper logger
        saveTraverse(files_info, log_file,header="# Current state of file_info")
    
    hists= get_hists_fitting_parameter_vs_settings(files_info, "n_bkgnd")
    ch_id_hists = create_sub_dicts_from_keys(hists,
                keysplit_function=lambda x: (x.split('_')[5], x.split('_')[3]))
    canvas = get_canvas_with_hists(ch_id_hists, pad_preffix="channel: ", 
                                legend_preffix="file: ")
    wait_to_quit()



if __name__ == '__main__':
    main()

