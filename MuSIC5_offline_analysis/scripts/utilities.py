#!/usr/bin/env python
# encoding: utf-8
"""
utilities.py

Created by Sam Cook on 2012-07-25.
Copyright (c) 2012 . All rights reserved.
"""

from ROOT import gROOT, TFile, TTree, TBranch, TCanvas

class Branch(object):
    """Represents a branch of a TTree, but also local stores the associated data"""
    # TODO make this an iterable object so we can easily loop over all entries
    def __init__(self, branch_ptr, data_object):
        self.ptr = branch_ptr
        self.data = data_object
    
    def __getitem__(self, key):
        return self.data.__getattribute__(key)
        
    def __getattr__(self, name):
        return self.ptr.__getattribute__(name)


def get_branch(tree, branch_name, data_class):
    """
    Gets a branch from a ROOT TTree and returns it as a useful object
    data_class must be a callable object that ROOT can write into
    """
    branch_ptr = tree.GetBranch(branch_name)
    branch_data = data_class()
    branch_ptr.SetAddress(branch_data)
    return Branch(branch_ptr, branch_data)


def get_struct(struct_fmt, struct_name):
    """
    Imports a named C struct with members given in struct comp at global scope.
    
    struct_fmt should be a string containing valid C defining the member
    variables of the struct all lines should be ended with a ';'
    """
    struct = "struct %s{%s};"%(struct_name, struct_fmt)
    # create the struct in CINT
    gROOT.ProcessLine(struct)
    # because we don't know the name of the struct we need to be able to 
    # access the entire ROOT module and use getattr to extract it dynamically
    tmp = __import__("ROOT")
    return tmp.__getattr__(struct_name)
    


def make_hist(name, xmin=0, xmax=20000, description=None, xtitle="time since trigger (ns)", ytitle="count"):
    description = description if description != None else name
    res = TH1F(name, description, (xmax - xmin), xmin, xmax)
    res.GetXaxis().SetTitle(xtitle)
    res.GetYaxis().SetTitle(ytitle)
    return res


def rebin(hist, n_bins, new_name=''):
    """
    Rebins a histogram to have n_bins, if new_name is not provided then 
    the original is modified. 
    NOTE: if n_bins is not an exact factor of the existing number of bins 
    then n_bins will be created and the excess (at the upper bin) will be 
    added to the overflow bin
    """
    if n_bins == 0:
        return hist
    xmin = hist.GetXaxis().GetXmin()
    xmax = hist.GetXaxis().GetXmax()
    new_bin_width = int(float(xmax - xmin)/n_bins)
    if (hist.GetNbinsX()%new_bin_width != 0): 
        print "WARNING: unable to form an integer number of bins, \
        x max will be lowered"
    return hist.Rebin(new_bin_width, new_name)


def make_canvas(name, n_x=4, n_y=4, maximised=False):
    name = str(name)
    canvas = TCanvas(name, name,1436,856) if maximised else TCanvas(name,name) 
    if n_x or n_y: canvas.Divide(n_x, n_y)
    return canvas


def print_matrix(covariance_matrix):
    dimension = covariance_matrix.GetNcols()
    fmt_string = "% 5.2e " * dimension 
    for i in range (dimension):
        row = tuple([covariance_matrix[i][n] for n in range(dimension)])
        print fmt_string % row


def set_param_and_error(param_number, param, error, function):
    function.SetParameter(param_number, param)
    function.SetParError (param_number, error)


def get_param_and_error(param_number, function):
    return function.GetParameter(param_number), function.GetParError(param_number)


def wait_to_quit():
    print "press ctrl+C to stop"
    try:
        while(True):
            pass
    except KeyboardInterrupt, e:
        pass
    print "bye bye"

