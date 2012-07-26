#!/usr/bin/env python
# encoding: utf-8
"""
count_muons_tests.py

Created by Sam Cook on 2012-07-23.
Copyright (c) 2012 . All rights reserved.
"""

from count_muons import *
from utilities import *

def test_get_struct():
    struct_fmt = "int a, b, c; float d[5];"
    struct_name = "test1"
    test1 = get_struct(struct_fmt, struct_name)
    a = test1()
    print dir(a)
    

def test_ids():
    ids = ((1, 'pass'), (2, 'pass'), (3, 'pass'), ('a', 'fail'), (None, 'fail'))
    for i in ids:
        try:
            print "trying \'%s\' it should %s"%(i[0],i[1])
            print get_file_name_from_id(i[0])
        except Exception, e:
            print (e)
        

def test_get_branch():
    branch_struct = "int adc, tdc0, nhits; int tdc[500];"
    in_branch = get_struct(branch_struct, "in_branch")
    in_file = TFile("../../../converted_data/run00458_converted.root")
    tree = in_file.Get("Trigger")
    branch = get_branch(tree, "D1", in_branch)
    print "branch name =", branch.GetName()
    branch.GetEntry(0)
    print "First ADC value is",branch['adc']
    branch.MONKEY()
    

def main():
    # run all the test
    # test_ids()
    # test_get_struct()
    test_get_branch()


if __name__ == '__main__':
    main()

