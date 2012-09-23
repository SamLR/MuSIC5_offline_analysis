#!/usr/bin/env python
# encoding: utf-8
"""
count_muons.py

Created by Sam Cook on 2012-07-23.
Copyright (c) 2012 . All rights reserved.
"""

from ROOT import TH1F, TFile, TF1, gStyle, gPad

from utilities import make_hist, rebin_bin_width, make_canvas, print_matrix, \
            set_param_and_error, get_param_and_error, wait_to_quit, \
            printTraverse, saveTraverse

from tdc_file import get_tdc_file

from config import *

def get_muon_yield_per_amp(n_mu, n_mu_er, file_info):
    """Convert number of muons & error to a yield per A proton current"""
    x = detector_efficiency* combined_acceptance* nA
    mu_yield = n_mu / (x * file_info['time'] * file_info['current'])
    mu_yield_er = n_mu_er / (x * file_info['time'] * file_info['current'])
    return mu_yield, mu_yield_er
    


def get_fitting_func(name, hist, window_lo, window_hi, initial_fit_params):
    res = TF1(name, "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])", window_lo, window_hi)
    for param_number, val in enumerate(initial_fit_params):
        res.SetParName(param_number, val[0])
        param_val = val[1](hist)
        if len(val) == 3:
            limit_lo, limit_hi = param_val - val[2], param_val + val[2] 
            res.SetParameter(param_number, param_val)
            res.SetParLimits(param_number, limit_lo, limit_hi)
        else:
            res.SetParameter(param_number, param_val)
    return res


def get_id_and_ch_from_hist(hist):
    name = hist.GetName()
    junk1, file_id, junk2, channel = name.split('_') # get the useful info
    file_id = int(file_id)
    return file_id, channel


def get_parameter_dict(fitting_func):
    """Get a human readable dictionary of parameter values"""
    param_names = ("N_b", "N_mu_slow", "t_mu_slow", "N_mu-_cu", "t_mu-_cu")
    param  = dict(zip(param_names, fitting_func.GetParameters()))
    errors = dict(zip(param_names, fitting_func.GetParErrors()))
    errors["t_mu-_cu"] = 1.0 # manually set the error given by PDG
    return param, errors


def copy_param_and_er(param_mapping, func_src, func_dest):
    for src, dest in param_mapping:
        par, er = get_param_and_error(src, func_src)
        set_param_and_error(dest, par, er, func_dest)


def calc_integral_from_exp_fit(param_mapping, fitting_func, covariance_matrix, window_lo, window_hi):
    func = TF1("tmp", "[0]*exp(-x/[1])", window_lo, window_hi,)    
    
    copy_param_and_er(param_mapping, fitting_func, func)
    
    # get the integral and then calculate the error on it
    count = func.Integral(window_lo, window_hi)
    sub_matrix_vals = (param_mapping[0][0], param_mapping[1][0],\
                        param_mapping[0][0],param_mapping[1][0])
    sub_matrix = covariance_matrix.GetSub(*sub_matrix_vals)
    er = func.IntegralError(window_lo, window_hi, \
                func.GetParameters(), sub_matrix.GetMatrixArray())
    return count, er


def make_muon_counts_dict(fitting_func, covariance_matrix, window_lo, window_hi, bin_width=0):
    n_bkgnd = fitting_func.GetParameter(0) * (window_lo - window_hi) # background is modeled as flat
    # TODO calculate n_background properly!
    bin_width = 1 if bin_width == 0 else bin_width # dodge div0 errors (bin width 0 == no rebin)
    print "bin_width:", bin_width
    # create and intialise the parameters for the copper portion of the exponential
    cu_mapping = ((1,0), (2,1))
    n_cu, n_cu_er = calc_integral_from_exp_fit(cu_mapping, fitting_func, \
                            covariance_matrix, window_lo, window_hi)                            
    print "Integral results (copper):            %.2e er: %.2e" % (n_cu, n_cu_er)
    n_cu, n_cu_er = n_cu/bin_width, n_cu_er/bin_width
    print "Integral results (copper normalised): %.2e er: %.2e" % (n_cu, n_cu_er)
    
    # now intialise the slow portion
    mu_mapping = ((3,0), (4,1))
    n_mu, n_mu_er = calc_integral_from_exp_fit(mu_mapping, fitting_func, \
                            covariance_matrix, window_lo, window_hi)
    print "Integral results (slow)             %.2e er: %.2e" % (n_mu, n_mu_er)
    n_mu, n_mu_er = n_mu/bin_width, n_mu_er/bin_width
    print "Integral results (slow normalised): %.2e er: %.2e" % (n_mu, n_mu_er)
    
    return {"n_bkgnd":(n_bkgnd, 0), "n_mu_cu":(n_cu, n_cu_er), "n_mu_slow":(n_mu, n_mu_er),}


def convert_current_to_protons(current):
    return current * 6.241e9 # current * n protons in 1nA


def make_ch_canvases(files_info,suffix=''):
    res = {}
    for id in files_info:
        name = "%s_%s"%(id, suffix) if suffix else "%s"%id
        res[id] = make_canvas(name, n_x=3, n_y=2, maximised=True)
    return res


def sum_muons_for_all_ch(fit_dict):
    n_muons = 0
    squared_errors = []
    for ch_id in fit_dict:
        counts = fit_dict[ch_id]['counts']
        n_muons += counts['n_mu_cu'][0] + counts["n_mu_slow"][0]
        squared_errors.append(counts['n_mu_cu'][1]**2 )
        squared_errors.append(counts["n_mu_slow"][1]**2 )
    return n_muons, sum(squared_errors)**0.5


def get_fit_param(fit_func):
    res = {}
    n_par = fit_func.GetNpar()
    for i in range(n_par):
        par  = fit_func.GetParameter(i)
        name = fit_func.GetParName(i)
        er   = fit_func.GetParError(i)
        res[name] = (par, er)
    res['chi2'] = (fit_func.GetChisquare(), fit_func.GetNDF())
    return res


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
            
            orig_hist = files_info[file_id]['hists'][ch_str]
            
            new_name = orig_hist.GetName() + "_" + setting_str
            # local, rebinned copy of the hist
            hist = rebin_bin_width(orig_hist, bin_width, new_name) 
        
            # get the fitting function and fit it to the histogram
            fit_name = "fit_" + new_name
            fitting_func = get_fitting_func(fit_name, hist,\
                                            fit_lo, fit_hi, initial_fit_params)
                                            
            # the covariance matrix can only be retrived from the fit result
            fit_res = hist.Fit(fitting_func, "RS") # fit in the function range
            covariance_matrix = fit_res.GetCovarianceMatrix()
            fit_param = get_fit_param(fitting_func)
            # get the integrals & errors
            counts = make_muon_counts_dict(fitting_func, covariance_matrix, fit_lo, fit_hi, bin_width)
        
            fit_results = {}
            fit_results['counts']    = counts
            fit_results['fit_param'] = fit_param
        
            if save_hist: fit_results['hist'] = hist
        
            # Save the generated information in the appropriate dictionary
            if not 'fits' in files_info[file_id].keys():
                files_info[file_id]['fits'] = {setting_str:{ch_str:fit_results}}
            elif not setting_str in files_info[file_id]['fits']:
                files_info[file_id]['fits'][setting_str] = {ch_str:fit_results}
            else:
                files_info[file_id]['fits'][setting_str][ch_str] = fit_results
        


def set_bin_val_er_label(hist, bin, val, er, name):
    hist.SetBinContent(bin, float(val))
    hist.SetBinError(bin, float(er))
    hist.GetXaxis().SetBinLabel(bin, str(name))


def settings_str(fit_lo, fit_hi, bin_width):
    return "lo_%i_hi_%i_bins_%i"%(fit_lo, fit_hi, bin_width)


def get_all_val_er_pair(files_info, search_terms, path=()):
    """
    Recursively walks through files_info looking for keys
    that match the given search_terms. As matching keys are met 
    they are popped. When all the search terms have been met
    the resultant value is added to a dictionary of all results 
    which is returned
    """
    

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
    # TODO Add function to display dictionary item X vs Y
    # make a dictionary of blank canvases ready to be drawn in
    canvases = {}
    
    for settings in fitting_settings:
        set_name = settings_str(**settings)
        
        print "*"*40, "\n\nSettings now: ", settings, "\n"
        
        get_derived_values(files_info, fitting_parameters, save_hist=save_hist, **settings)        
        for id in files_info:
            fit_data = files_info[id]['fits'][set_name]
            n_muons, n_muons_er = sum_muons_for_all_ch(fit_data)
            fit_data['total_muons'] = (n_muons, n_muons_er)
            
            mu_yield, mu_yield_er = get_muon_yield_per_amp(n_muons, n_muons_er, files_info[id])
            mu_yield, mu_yield_er = [i*uA for i in (mu_yield, mu_yield_er)]
            fit_data['muon_yields'] = (mu_yield, mu_yield_er)
            display_string = "degrader dz %.1f yields %5.2e er %5.2e"
            print '*'*40
            print display_string%(files_info[id]['deg_dz'], mu_yield, mu_yield_er)
    
    # for general checking, save the final state of files_info
    with open("file_info.txt", "write") as log_file:
        # TODO write a proper logger
        saveTraverse(files_info, log_file,header="# Current state of file_info")
    # hack to keep stuff displayed
    # wait_to_quit()


if __name__ == '__main__':
    main()

