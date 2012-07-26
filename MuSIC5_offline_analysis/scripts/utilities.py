#!/usr/bin/env python
# encoding: utf-8
"""
utilities.py

Created by Sam Cook on 2012-07-25.
Copyright (c) 2012 . All rights reserved.
"""

from ROOT import gROOT, TFile, TTree, TBranch

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
    


