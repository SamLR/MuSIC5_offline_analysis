#!/usr/bin/env python
# encoding: utf-8
"""
utilities.py

Created by Sam Cook on 2012-07-25.
Copyright (c) 2012 . All rights reserved.
"""

from ROOT import gROOT, TFile, TTree, TBranch, TCanvas, TH1F

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
    


def make_hist(name, xmin, xmax, xtitle, ytitle, description=None):
    description = description if description != None else name
    res = TH1F(name, description, (xmax - xmin), xmin, xmax)
    res.GetXaxis().SetTitle(xtitle)
    res.GetYaxis().SetTitle(ytitle)
    return res


def rebin_nbins(hist, n_bins, new_name=''):
    """
    Rebins a histogram to have n_bins, if new_name is not provided then 
    the original is modified. 
    NOTE: if n_bins is not an exact factor of the existing number of bins 
    then n_bins will be created and the excess (at the upper bin) will be 
    added to the overflow bin
    """
    if n_bins == 0:
        return hist
    else:
        xmin = hist.GetXaxis().GetXmin()
        xmax = hist.GetXaxis().GetXmax()
        new_bin_width = int(float(xmax - xmin)/n_bins)
        if (hist.GetNbinsX()%new_bin_width != 0): 
            print "WARNING: unable to form an integer number of bins, \
            x max will be lowered"
        return rebin_bin_width(hist, new_bin_width, new_name)


def rebin_bin_width(hist, bin_width, new_name=''):
    if bin_width == 0: 
        return hist
    else:
        return hist.Rebin(bin_width, new_name)


def make_canvas(name, n_x=0, n_y=0, maximised=False):
    name = str(name)
    canvas = TCanvas(name, name,1436,856) if maximised else TCanvas(name,name) 
    if n_x or n_y: canvas.Divide(n_x, n_y)
    return canvas


def get_dict_of_keys_and_file(filename, keyfunc=lambda x:x):
    """
    Opens the named TFile and creates a dictionary out of the 
    objects saved with in it. 
    
    The returned dictionary is formed of object:object_name pairs
    
    The pointer to the file is also returned to keep it in scope.
    
    Keyfunc is a function applied to the object's name to create 
    the dictionary key
    """
    # TODO Look at creating a recursive version of this
    # i.e. if the object has crawlable sub structure (trees, dirs etc)
    # write it into a dict format
    in_file = TFile(filename, "READ")
    res = {}
    for key in in_file.GetListOfKeys():
        # name looks like "Muon_momentum_with_Aluminium_0.5mm"
        obj = key.ReadObj()
        key = keyfunc(obj.GetName())
        res[key] = obj
    return res, in_tfile


def print_square_matrix(matrix):
    dimension = matrix.GetNcols()
    fmt_string = "% 5.2e " * dimension 
    for i in range (dimension):
        row = tuple([matrix[i][n] for n in range(dimension)])
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


def traverse(obj, pmode=False, level=0):
    """
    Traverses an object yielding its contents. Strings are not traversed.
    For dictionaries the key is first returned then the contents at that key.
    Level is a depth counter. 
    A 'True' value of pmode will yield both the value and the level 
    
    Based on the solution given by Jeremy Banks, here: http://stackoverflow.com/questions/6290105/traversing-a-list-tree-and-get-the-typeitem-list-with-same-structure-in-pyth#6290211
    """
    if hasattr(obj, 'keys'):
        for val in obj:
            yield val if not pmode else ('{'+str(val), level)
            level += 1
            for subval in traverse(obj[val], pmode, level):
                yield subval
            level -= 1    
            if pmode: yield ('}', level)
    elif hasattr(obj, '__iter__'):
        for val in obj:
            level += 1
            for subval in traverse(val, pmode, level):
                yield subval
            # yield subval, level 
            level -= 1 
    else:
        yield obj if not pmode else (obj, level)


def printTraverse(obj,spacer='.'):
    """
    prints the contents of obj in a nested manner
    """
    for i in traverse(obj, pmode=True): print "%s%s"%(spacer*i[1], i[0])          


def saveTraverse(obj,file,spacer='.',header=''):
    """
    Save the contents of obj to a file
    """
    header += "\n"
    file.write(header)
    for i in traverse(obj, pmode=True): file.write("%s%s\n"%(spacer*i[1], i[0]))


def set_bin_val_er_label(hist, bin, val, er, bin_name):
    hist.SetBinContent(bin, float(val))
    hist.SetBinError(bin, float(er))
    hist.GetXaxis().SetBinLabel(bin, str(bin_name))

if __name__ == '__main__':
    d = {'a':1,'b':2,'c':(9,8,7),'d':{'aa':12,'bb':22}}
    for i,j in traverse(d, True): print "%s%s"%(".."*j,i)

    
        
