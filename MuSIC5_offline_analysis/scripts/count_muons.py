#!/usr/bin/env python
# encoding: utf-8
"""
count_muons.py

Created by Sam Cook on 2012-07-23.
Copyright (c) 2012 . All rights reserved.
"""

from ROOT import TH1F, TFile, TF1, gStyle

from utilities import make_hist, rebin, make_canvas, print_matrix, \
            set_param_and_error, get_param_and_error, wait_to_quit

from tdc_file import get_tdc_file


file_info = ({'id':448, 'deg_dz':0,  'time':9221 ,'current':0.0153375  },
             {'id':451, 'deg_dz':0.5,'time':1001 ,'current':0.0154625  },
             {'id':452, 'deg_dz':0.5,'time':4944 ,'current':0.013132143},
             {'id':455, 'deg_dz':1,  'time':6307 ,'current':0.013321429},
             {'id':458, 'deg_dz':5,  'time':5144 ,'current':0.013625   },
             {'id':459, 'deg_dz':5,  'time':2452 ,'current':0.012383929})
    
u_channels = tuple(["U%i"%i for i in range(1,9)]) # range(x,y) returns x:(y-1)
d_channels = tuple(["D%i"%i for i in range(1,6)])
all_channels = u_channels + d_channels
    

# lambdas allow dynamically calculated parameters
# form (parameter name, initial value function, [optional] range)
fitting_parameters =(("N_{B}"      ,lambda hist: float(hist.GetMaximum())/10),               
                     ("N_{#mu^{-}}",lambda hist: float(hist.GetMaximum())),
                     ("#tau_{Cu}"  ,lambda hist: 163.5, 1), # PDG value is ± 1 
                     ("N_{#mu^{+}}",lambda hist: float(hist.GetMaximum())/2),
                     ("#tau_{#mu}" ,lambda hist: 2000 ))

t_window_start = 50 #200 #
t_window_stop  = 15000#20000
n_bins         = 50 #100 #0

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


def make_muon_counts_dict(fitting_func, covariance_matrix,window_lo, window_hi, n_bins):
    n_background = fitting_func.GetParameter(0) * (window_lo - window_hi) # background is modeled as flat
    
    # create and intialise the parameters for the copper portion of the exponential
    cu_mapping = ((1,0), (2,1))
    n_cu, n_cu_er = calc_integral_from_exp_fit(cu_mapping, fitting_func, \
                            covariance_matrix, window_lo, window_hi)
    n_cu_norm, n_cu_er_norm = n_cu/n_bins, n_cu_er/n_bins
    print "Integral results (copper):            %.2e er: %.2e" % (n_cu, n_cu_er)
    print "Integral results (copper normalised): %.2e er: %.2e" % (n_cu_norm, n_cu_er_norm)
    
    # now intialise the slow portion
    mu_mapping = ((3,0), (4,1))
    n_mu, n_mu_er = calc_integral_from_exp_fit(mu_mapping, fitting_func, \
                            covariance_matrix, window_lo, window_hi)
    n_mu_norm, n_mu_er_norm = n_mu/n_bins, n_mu_er/n_bins
    print "Integral results (slow)             %.2e er: %.2e" % (n_mu, n_mu_er)
    print "Integral results (slow normalised): %.2e er: %.2e" % (n_mu_norm, n_mu_er_norm)
    
    return {"n_bkgnd":(n_background, 0), "n_mu_cu":(n_cu, n_cu_er), "n_mu_slow":(n_mu, n_mu_er),\
            "n_mu_cu_norm":(n_cu_norm, n_cu_er_norm), "n_mu_slow_norm":(n_mu_norm, n_mu_er_norm),}


def get_file_index_from_id(id):
    for file in file_info:
        if file['id'] == id: return file_info.index(file)


def convert_current_to_protons(current):
    return current * 6.241e9 # current * n protons in 1nA


def make_canvases(file_info,suffix):
    res = {}
    for i in file_info:
        id = i['id']
        name = "%s_%s"%(id, suffix)
        res[id] = make_canvas(name, n_x=3, n_y=2, maximised=True)
    return res


def get_number_muons(in_dict):
    n_muons = 0
    squared_errors = []
    for ch in in_dict.values():
        n_muons += ch['n_mu_cu'][0] + ch["n_mu_slow"][0]
        squared_errors.append( ch['n_mu_cu'][1]**2 )
        squared_errors.append( ch["n_mu_slow"][1]**2 )
    # print "sum: %.2e sq-sum: %.2e, sqrt(sum): %.2e"% (n_muons, sum(squared_errors), sum(squared_errors)**0.5)
    return n_muons, sum(squared_errors)**0.5
        


def convert_integral_to_hits(val, n_bins):
    # calibration function is:
    # new_val = ((val - para1)/40)*1.025; (para1 = tdc0)
    #   => 1tdc bin = 1.025/40 ns
    bin_width_ns = float(t_window_stop)/n_bins 


def process_tdc_file(tdc_file, file_info, n_bins, window_lo, window_hi, initial_fit_params, canvases):    
    for key in tdc_file.GetListOfKeys():
        # get the histogram and extract the info about it
        hist = key.ReadObj()
        file_id, ch = get_id_and_ch_from_hist(hist)
        if 'U' in ch: continue
        
        index = get_file_index_from_id(file_id)
        
        print "*" * 40, "\n \n", file_id, ch
        
        # rebin it into bins 50ns (20000/400 = 50) wide 
        rebin(hist, n_bins)
        canvases[int(file_id)].cd(int(ch[1:])) # get it drawn in the correct place
        
        # get the fitting function and fit it to the histogram
        fitting_func = get_fitting_func("fit_file%i_ch%s"%(file_id, ch), hist,\
                                        window_lo, window_hi, initial_fit_params)
        fit_res = hist.Fit(fitting_func, "RS") # fit in the function range
        # the covariance matrix can only be retrived from the fit result
        covariance_matrix = fit_res.GetCovarianceMatrix()
        # get the integrals & errors
        counts = make_muon_counts_dict(fitting_func, covariance_matrix, window_lo, window_hi, n_bins)
        # save the info
        if 'results' in file_info[index].keys():
            file_info[index]['results'][ch] = counts
        else:
            file_info[index]['results'] = {}
            file_info[index]['results'][ch] = counts


def main():
    # open .root files
    # for each root file
    #   for each channel
    #       plot all times recorded
    #       fit with: exp + exp + C
    #       add to file sum the integral of the exp corresponding to muons 
    # plot normalised integral of number of muons against file id (hence deg dz)
           
    # get the file containing all the tdc histograms
    tdc_hist_file_name = "music5_tdc_data.root"
    tdc_file = get_tdc_file(tdc_hist_file_name)
    
    gStyle.SetOptFit()
    # make a dictionary of blank canvases ready to be drawn in
    suffix = "a"
    canvases = make_canvases(file_info, suffix)
    process_tdc_file(tdc_file, file_info, n_bins, t_window_start, t_window_stop, fitting_parameters, canvases)
    
    print "*"*40, '\n'
    muon_count_rates = TH1F("Muon_counts","Muon_counts",6,1,6)
    muon_count_rates.GetXaxis().SetTitle("Al Degrader Thickness (mm)")
    muon_count_rates.GetYaxis().SetTitle("Number of muons (normalised to time)")
    
    for bin, file in enumerate(file_info, 1): # bin 0 is underflow 
        n_muons, n_muons_er = get_number_muons(file['results'])
        print (u"%.2e ± %.2e"%(n_muons, n_muons_er))
        muon_count_rates.SetBinContent(bin, float(n_muons)/file['time'])
        # muon_count_rates.SetBinContent(bin, float(n_muons))
        muon_count_rates.SetBinError(bin, float(n_muons_er)/file['time'])
        # muon_count_rates.SetBinError(bin, float(n_muons_er))
        muon_count_rates.GetXaxis().SetBinLabel(bin, str(file['deg_dz']))
        
    for can in canvases.values(): can.Update()
    can_final = make_canvas("normalised_muon_counts", maximised=True)
    muon_count_rates.Draw()
    
    # hack to keep stuff displayed
    wait_to_quit()


if __name__ == '__main__':
    main()

