#!/usr/bin/env python
# encoding: utf-8
"""
count_muons.py

Created by Sam Cook on 2012-07-23.
Copyright (c) 2012 . All rights reserved.
"""

from ROOT import TH1F, TFile, TF1, gStyle, gPad

from utilities import make_hist, make_canvas, wait_to_quit, \
                      saveTraverse, set_bin_val_er_label

from tdc_file import get_tdc_file

from fitting import fit_hist

from config import *

def get_muon_yield_per_amp(file_info):
    """Convert number of muons & error to a yield per A proton current"""
    n_mu, n_mu_er = file_info['fits']['total_muons']
    x = detector_efficiency* file_info['acceptance'] * file_info['time'] * file_info['current'] *nA
    mu_yield = float(n_mu) / x
    mu_yield_er = float(n_mu_er) / x
    return mu_yield, mu_yield_er
    


def get_id_and_ch_from_hist(hist):
    junk1, file_id, junk2, channel = (hist.GetName()).split('_')
    file_id = int(file_id)
    return file_id, channel


def convert_current_to_protons(current):
    return current * 6.241e9 # current * n protons in 1nA


def sum_muons_for_all_ch(fit_dict):
    n_muons = 0
    squared_errors = []
    for ch_id in fit_dict:
        counts = fit_dict[ch_id]['counts']
        n_muons += counts['n_mu_cu'][0] + counts["n_mu_slow"][0]
        squared_errors.append(counts['n_mu_cu'][1]**2 )
        squared_errors.append(counts["n_mu_slow"][1]**2 )
    return n_muons, sum(squared_errors)**0.5


def settings_str(fit_lo, fit_hi, bin_width):
    return "lo_%i_hi_%i_bins_%i"%(fit_lo, fit_hi, bin_width)


def fitting_parameter_plots_vs_settings(files_info, parameter, setting_strs, canvas=None):
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
    make_settings_hist = lambda name: make_hist(name, 0, len(setting_strs), 'fit settings', parameter)
    get_hist_key = lambda file_id, ch_id: "%s_file_%i_ch_%s"%(parameter, file_id, ch_id)
    hists = {}
    ch_ranges = {}
    for file_id, file_dat in files_info.items():
        for bin, setting_str in enumerate(setting_strs, 1):
            # bin 0 == underflow. bin number != x_axis value
            for ch_id, ch_dat in file_dat['fits'][setting_str].items():
                if not ch_id in all_channels:continue
                
                hist_key = get_hist_key(file_id, ch_id)
                val, er  = ch_dat['fit_param'][parameter][0], ch_dat['fit_param'][parameter][1]
                
                if not hist_key in hists.keys():
                    hists[hist_key] = make_settings_hist(hist_key)
                set_bin_val_er_label(hists[hist_key], bin, val, er, setting_str)
                
                if not ch_id in ch_ranges.keys(): 
                    ch_ranges[ch_id] = {'min':val-er, 'max':val+er}
                elif (val + er) > ch_ranges[ch_id]['max']:
                    ch_ranges[ch_id]['max'] = val + er
                elif (val - er) < ch_ranges[ch_id]['min']:
                    ch_ranges[ch_id]['min'] = val - er
    # now draw it
    canvas = canvas if canvas else make_canvas(parameter, 3, 2, True) 
    for pad_id, ch_id in enumerate(ch_ranges.keys(), 1): # pad 0 is the entire canvas
        canvas.cd(pad_id)
        first = True
        draw_options = "P"
        for colour_id, file_id in enumerate(files_info,1):
            hist_key = get_hist_key(file_id, ch_id)
            if first:
                # TODO ADD legend
                hists[hist_key].SetMinimum(ch_ranges[ch_id]['min'])
                hists[hist_key].SetMaximum(ch_ranges[ch_id]['max'])
                
            hists[hist_key].SetLineColor(colour_id)
            hists[hist_key].Draw(draw_options)
            draw_options= "P SAME"
            first = False
    return canvas, hists


def get_derived_values(files_info, initial_fit_params, fit_lo, fit_hi, bin_width, save_hist=False):
    """
    Workhorse function, reads the TDC file, fits the histograms & calculates integrals 
    """
    for file_id in files_info:
        for ch_str in files_info[file_id]['hists']:
            if not ch_str in d_channels: continue
            
            # upstream scintillators are not calibrated to detect decay electrons well so skip them
            setting_str = settings_str(fit_lo, fit_hi, bin_width)
            print "*" * 40, "\n \n", file_id, ch_str, setting_str
            
            hist = files_info[file_id]['hists'][ch_str]
            fit_results = fit_hist(hist,fit_lo, fit_hi, bin_width, initial_fit_params, save_hist)
            
            # Save the generated information in the appropriate dictionary
            if not 'fits' in files_info[file_id].keys():
                files_info[file_id]['fits'] = {setting_str:{ch_str:fit_results}}
            elif not setting_str in files_info[file_id]['fits']:
                files_info[file_id]['fits'][setting_str] = {ch_str:fit_results}
            else:
                files_info[file_id]['fits'][setting_str][ch_str] = fit_results


def main():
    # open .root files
    # for each root file
    #   for each channel
    #       plot all times recorded
    #       fit with: exp + exp + C
    #       add to file sum the integral of the exp corresponding to muons 
    # plot normalised integral of number of muons against file id (hence deg dz)
    
    # get the file containing all the tdc histograms
    tdc_file = get_tdc_file(tdc_hist_file_name, files_info, all_channels)
    gStyle.SetOptFit()
    gStyle.SetOptStat(0)
    # make a dictionary of blank canvases ready to be drawn in
    canvases = {}
    
    for settings in fitting_settings:
        set_name = settings_str(**settings)
        
        print "*"*40, "\n\nSettings now: ", settings, "\n"
        
        get_derived_values(files_info, fitting_parameters, save_hist=save_hist, **settings)        
        for id in files_info:
            fit_data = files_info[id]['fits'][set_name]
            n_muons, n_muons_er = sum_muons_for_all_ch(fit_data)
            files_info[id]['fits']['total_muons'] = (n_muons, n_muons_er)
            
            mu_yield, mu_yield_er = get_muon_yield_per_amp(files_info[id])
            mu_yield, mu_yield_er = [i*uA for i in (mu_yield, mu_yield_er)]
            files_info[id]['fits']['muon_yields'] = (mu_yield, mu_yield_er)
            display_string = "degrader dz %.1f yields %5.3e er %5.2e"
            print '\n','*'*40
            print display_string%(files_info[id]['deg_dz'], mu_yield, mu_yield_er)
            
    
    # for general checking, save the final state of files_info
    with open("file_info.txt", "write") as log_file:
        # TODO write a proper logger
        saveTraverse(files_info, log_file,header="# Current state of file_info")
    
    setting_strs = [settings_str(**i) for i in fitting_settings]
    # TODO make chi2, tau_mu_all etc a variable
    canvas = make_canvas('chi2', 3, 2, True) 
    canvas2 = make_canvas('#tau_{#mu_{All}}', 3, 2, True) 
    canvas, hists = fitting_parameter_plots_vs_settings(files_info,'chi2',setting_strs, canvas)
    canvas2, hists = fitting_parameter_plots_vs_settings(files_info,'#tau_{#mu_{All}}',setting_strs, canvas2)
    canvas.Update()
    canvas2.Update()
    canvas3 = make_canvas('c2')
    files_info[451]['fits']['lo_50_hi_15000_bins_10']['D4']['hist'].Draw()
    wait_to_quit()


if __name__ == '__main__':
    main()

