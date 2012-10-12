#!/usr/bin/env python
# encoding: utf-8
"""
tdc_file.py

Created by Sam Cook on 2012-08-20.
Copyright (c) 2012 . All rights reserved.
"""
import os.path

from ROOT import TH1F, TFile, TBranch

from root_utilities import get_branch, get_struct, make_hist

_branch_struct = "int adc, tdc0, nhits; int tdc[500];"
_file_location_fmt = "../../../converted_data/run00%i_converted.root"


def _make_tdc_hist(name):
    """Wrapper that sets basic values"""
    return make_hist(name, xmin=0, xmax=20000, xtitle="Time (ns)", ytitle="Count")
    

def _get_file_name_from_id(id):
    """Simple helper function"""
    return _file_location_fmt%(id)


def _get_id_and_ch_from_hist(hist):
    name = hist.GetName()
    junk1, file_id, junk2, channel = name.split('_') # get the useful info
    file_id = int(file_id)
    return file_id, channel

def _attach_hist_to_file_info(tfile_ptr,files_info):
    """
    This will loop over the contents of the tdc histogram TFile and attach 
    dictionaries of the histograms to the correct file
    """
    for key in tfile_ptr.GetListOfKeys():
        # get the histogram and extract the info about it
        hist = key.ReadObj()
        file_id, ch_str = _get_id_and_ch_from_hist(hist)
        
        if not 'hists' in files_info[file_id].keys():
            # make a new entry ('hists') that is a channel indexed dict of hists
            files_info[file_id]['hists'] = {ch_str: hist,}
        else:
            # otherwise add this hist at the correct place
            files_info[file_id]['hists'][ch_str] = hist
        
        

def get_tdc_file(tdc_hist_file_name, files_info, channels, recreate=False):
    """
    If the file already exists open it, if not recreate it
    """
    if (not os.path.isfile(tdc_hist_file_name)) or recreate:
        print "TDC hist file (%s) not found, creating... "%tdc_hist_file_name
        create_tdc_hist_file(files_info, tdc_hist_file_name, channels)
        print "TDC hist file creation complete"
    print "Loading histograms"
    file_ptr = TFile(tdc_hist_file_name, "READ")
    _attach_hist_to_file_info(file_ptr, files_info)
    return file_ptr


def create_tdc_hist_file(in_file_info, out_file_name, channels):
    """
    Open all the files (based on ID) in in_file_info using the 
    _file_location_fmt, process all the information inside them and
    save it as histograms to the out_file_name
    """
    out_file = TFile(out_file_name, "RECREATE")
    in_branch_struct = get_struct(_branch_struct, "in_branch_struct")
    hists={}
    for id,file_entry in in_file_info.items():
        # open the file and load the tree
        file_name = _get_file_name_from_id(id)
        file_ptr = TFile(file_name, 'READ')
        print "\n Opened file ID: %i File name: %s"%(id,file_name)
        tree = file_ptr.Get("Trigger")
        # add an empty dictionary for this file's histograms
        hists[id] = {}
        
        # load all the branches and create the histograms in the out file
        branches = {}
        for ch in channels:
            branches[ch] = get_branch(tree, ch, in_branch_struct)
            hist_name = "file_%i_ch_%s"%(id,ch)
            out_file.cd()
            hists[id][ch] = _make_tdc_hist(hist_name)
            
        n_entries = tree.GetEntries()
        for i in range(n_entries):
            tree.GetEntry(i)
            if i % int(n_entries/20) == 0: print "%i of %i processed"%(i, n_entries)
            for branch in branches.items():
                for i in range(branch[1]['nhits']):
                    hists[id][branch[0]].Fill(branch[1]['tdc'][i])
        file_ptr.Close() # clean up after ourselves
    out_file.Write()
    out_file.Close()


def main():
    # TODO move file info etc into a config file
    print "You probably don't want to do that"
    return
    from config import files_info, tdc_hist_file_name, all_channels
    create_tdc_hist_file(files_info, tdc_hist_file_name, all_channels)


if __name__ == '__main__':
    main()

