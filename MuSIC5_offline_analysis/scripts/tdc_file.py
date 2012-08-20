#!/usr/bin/env python
# encoding: utf-8
"""
tdc_file.py

Created by Sam Cook on 2012-08-20.
Copyright (c) 2012 . All rights reserved.
"""
import os.path

from ROOT import TH1F, TFile, TBranch

from utilities import get_branch, get_struct

branch_struct = "int adc, tdc0, nhits; int tdc[500];"

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




def main():
    pass


if __name__ == '__main__':
    main()

