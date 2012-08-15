#!/usr/bin/env python
# encoding: utf-8
"""
count_muons.py

Created by Sam Cook on 2012-07-23.
Copyright (c) 2012 . All rights reserved.
"""

from time import sleep
from ROOT import TH1F, TFile, TF1, Double, TCanvas, gStyle
import os.path

from utilities import *


file_info = ({'id':448, 'deg_dz':0,  'time':9221 ,'current':0.0153375  },
             {'id':451, 'deg_dz':0.5,'time':1001 ,'current':0.0154625  },
             {'id':452, 'deg_dz':0.5,'time':4944 ,'current':0.013132143},
             {'id':455, 'deg_dz':1,  'time':6307 ,'current':0.013321429},
             {'id':458, 'deg_dz':5,  'time':5144 ,'current':0.013625   },
             {'id':459, 'deg_dz':5,  'time':2452 ,'current':0.012383929})
    
u_channels = tuple(["U%i"%i for i in range(1,9)]) # range(x,y) returns x:(y-1)
d_channels = tuple(["D%i"%i for i in range(1,6)])
all_channels = u_channels + d_channels
    
branch_struct = "int adc, tdc0, nhits; int tdc[500];"
fitting_defaults =(("N_{B}"      ,200  ),               
                   ("N_{#mu^{-}}",100  ),
                   ("#tau_{Cu}"  ,163.5), # PDG value
                   ("N_{#mu^{+}}",50   ),
                   ("#tau_{#mu}" ,2000 ))

t_window_start = 100
t_window_stop  = 20000


def get_tdc_file(tdc_hist_file_name, recreate=False):
    """
    If the file already exists open it, if not recreate it
    """
    if (not os.path.isfile(tdc_hist_file_name)) or recreate:
        print "TDC hist file (%s) not found, creating... "%tdc_hist_file_name
        return create_tdc_hist_file(file_info, tdc_hist_file_name)
    else:
        print "Found TDC hist file (%s) opening..."%tdc_hist_file_name
        return TFile(tdc_hist_file_name, "READ")


def get_file_name_from_id(id):
    return "../../../converted_data/run00%i_converted.root"%(id)


def make_tdc_hist(name, xmin=0, xmax=20000, description=None):
    description = description if description != None else name
    res = TH1F(name, description, (xmax - xmin), xmin, xmax)
    res.GetXaxis().SetTitle("time since trigger (ns)")
    res.GetYaxis().SetTitle("count")
    return res


def create_tdc_hist_file(in_file_info, out_file_name):
    out_file = TFile(out_file_name, "RECREATE")
    in_branch_struct = get_struct(branch_struct, "in_branch_struct")
    hists={}
    for file_entry in file_info:
        # open the file and load the tree
        id = file_entry['id']
        file_name = get_file_name_from_id(id)
        file_ptr = TFile(file_name, 'READ')
        print "\n Opened file ID: %i File name: %s"%(id,file_name)
        tree = file_ptr.Get("Trigger")
        # add an empty dictionary for this file's histograms
        hists[id] = {}
        
        # load all the branches and create the histograms in the out file
        branches = {}
        for ch in all_channels:
            branches[ch] = get_branch(tree, ch, in_branch_struct)
            hist_name = "file_%i_ch_%s"%(id,ch)
            out_file.cd()
            hists[id][ch] = make_tdc_hist(hist_name)
        
        n_entries = tree.GetEntries()
        for i in range(n_entries):
            tree.GetEntry(i)
            
            for branch in branches.items():
                for i in range(branch[1]['nhits']):
                    hists[id][branch[0]].Fill(branch[1]['tdc'][i])
        file_ptr.Close() # clean up after ourselves
    out_file.Write()
    out_file.Close()
    # return the newly created file but in read mode
    return TFile(out_file_name, "READ")


def get_fitting_func(name):
    #
    res = TF1(name, "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])", t_window_start, t_window_stop)
    for val in fitting_defaults:
        param_number = fitting_defaults.index(val)
        res.SetParName(param_number, val[0])
        if val[0] == "#tau_{Cu}":
            res.SetParameter(param_number, val[1])
            # The error on the lifetime of muonic copper is 1, limit the fit to this
            res.SetParLimits(param_number, val[1] - 1, val[1] + 1)
        else:
            res.SetParameter(param_number, val[1])
    return res


def rebin(hist, n_bins, new_name=''):
    """
    Rebins a histogram to have n_bins, if new_name is not provided then 
    the original is modified. 
    NOTE: if n_bins is not an exact factor of the existing number of bins 
    then n_bins will be created and the excess (at the upper bin) will be 
    added to the overflow bin
    """
    xmin = hist.GetXaxis().GetXmin()
    xmax = hist.GetXaxis().GetXmax()
    new_bin_width = int(float(xmax - xmin)/n_bins)
    if (hist.GetNbinsX()%new_bin_width != 0): 
        print "WARNING: unable to form an integer number of bins, \
        x max will be lowered"
    return hist.Rebin(new_bin_width, new_name)


def get_id_and_ch_from_hist(hist):
    name = hist.GetName()
    junk1, file_id, junk2, channel = name.split('_') # get the useful info
    file_id = int(file_id)
    return file_id, channel


def get_divided_canvas(name, n_x=4, n_y=4, max=False):
    canvas = TCanvas(name, name,1436,856) if max else TCanvas(name,name) 
    canvas.Divide(n_x, n_y)
    return canvas


def get_parameter_dict(fitting_func):
    """Get a human readable dictionary of parameter values"""
    param_names = ("N_b", "N_mu_slow", "t_mu_slow", "N_mu-_cu", "t_mu-_cu")
    param = dict(zip(param_names, fitting_func.GetParameters()))
    errors = dict(zip(param_names, fitting_func.GetParErrors()))
    errors["t_mu-_cu"] = 1.0 # manually set the error given by PDG
    return param, errors


def get_muon_counts_dict(fitting_func, covariance_matrix):
    params, errors = get_parameter_dict(fitting_func)
    
    n_background = params['N_b'] * (t_window_start - t_window_stop) # background is modeled as flat
    
    func_cu = TF1("cu_func", "[0]*exp(-x/[1])", t_window_start, t_window_stop)
    func_cu.SetParameter(0, fitting_func.GetParameter(1))
    func_cu.SetParError (0, fitting_func.GetParError(1))
    
    func_cu.SetParameter(1, fitting_func.GetParameter(2))
    func_cu.SetParError (1, fitting_func.GetParError(2))
    
    n_cu = func_cu.Integral(t_window_start, t_window_stop)
    cu_covariance = covariance_matrix.GetSub(1,2,1,2).GetMatrixArray()
    n_cu_er = func_cu.IntegralError(t_window_start, t_window_stop, func_cu.GetParameters(), cu_covariance)
    print "%f er: %.2e" % (n_cu, n_cu_er)
    
    func_mu = TF1("slow_func", "[0]*exp(-x/[1])", t_window_start, t_window_stop)
    func_mu.SetParameter(0, fitting_func.GetParameter(3))
    func_mu.SetParError (0, fitting_func.GetParError(3))
    
    func_mu.SetParameter(1, fitting_func.GetParameter(4))
    func_mu.SetParError (1, fitting_func.GetParError(4))
    n_mu = func_mu.Integral(t_window_start, t_window_stop)
    
    mu_covariance = covariance_matrix.GetSub(3,4,3,4).GetMatrixArray()
    for i in range(2): print func_mu.GetParameters()[i]
    n_mu_er = func_mu.IntegralError(t_window_start, t_window_stop, func_mu.GetParameters(), mu_covariance)
    print "%f er: %.2e" % (n_mu, n_mu_er)
    
    
    return {"n_bkgnd":n_background, "n_mu-_cu":(n_cu, n_cu_er), "n_mu_slow":(n_mu, n_mu_er), "n_muons":(n_mu+n_cu)}


def print_covariance_matrix(covariance_matrix):
    dimension = covariance_matrix.GetNcols()
    fmt_string = "% 5.2e " * dimension 
    for i in range (dimension):
        row = tuple([covariance_matrix[i][n] for n in range(dimension)])
        print fmt_string % row


def get_file_index_from_id(id):
    for file in file_info:
        if file['id'] == id: return file_info.index(file)


def convert_current_to_protons(current):
    return current * 6.241e9 # current * n protons in 1nA


def make_canvases():
    res = {}
    for i in file_info:
        id = i['id']
        res[id] = TCanvas(str(id),str(id),1436,856)
        res[id].Divide(3,2)
    return res


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
    # make a dictionary of blank canvases ready to be drawn in
    canvases = make_canvases()
    
    gStyle.SetOptFit()
    
    for key in tdc_file.GetListOfKeys():
        # get the histogram and extract the info about it
        hist = key.ReadObj()
        file_id, ch = get_id_and_ch_from_hist(hist)
        if 'U' in ch: continue
        
        index = get_file_index_from_id(file_id)
        
        # rebin it into bins 50ns (20000/400 = 50) wide 
        rebin(hist, 400)
        canvases[int(file_id)].cd(int(ch[1:]))
        # get the fitting function and fit it to the histogram
        fitting_func = get_fitting_func("fit_file%i_ch%s"%(file_id, ch))
        fit_res = hist.Fit(fitting_func, "S") # fit in the function range
        covariance_matrix = fit_res.GetCovarianceMatrix()
        # print_covariance_matrix(covariance_matrix) 
        counts = get_muon_counts_dict(fitting_func, covariance_matrix)
        # save the info
        if 'results' in file_info[index].keys():
            file_info[index]['results'][ch] = counts
            file_info[index]['results']['n_muons'] += counts['n_muons']
        else:
            file_info[index]['results'] = {}
            file_info[index]['results'][ch] = counts
            file_info[index]['results']['n_muons'] = counts['n_muons']
            
    print "*"*40, '\n'
    print "Thickness | Muon count | Rate (mu/s) | Norm. Rate (mu/s/p)"
    for file in file_info: 
        dz = file['deg_dz']
        n_mu = file['results']['n_muons']
        mu_rate = float(n_mu)/file['time']
        mu_rate_n = mu_rate/convert_current_to_protons(file['current'])
        print "%9.1f | %10i | %11.0f | %19.1e" % (dz, n_mu, mu_rate, mu_rate_n)
    for can in canvases.values(): can.Update()
    sleep (20)
        


if __name__ == '__main__':
    main()

