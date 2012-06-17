// tfile_converter_algorithm.cpp
// -- Implements the methods to convert from an input midus ROOT file to another format of ROOT file
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <sstream>

#include "tfile_converter_algorithm.h"

#include "TTree.h"

std::string const tfile_converter_algorithm::channel_names[n_tdc_channels] = {"U0", "U1", "U2", "U3", "U4",  "U5", "U6",  "U7", "D0",  "D1", "D2",  "D3", "D4",  "Ge0", "Ge1",  "CdTe"};

tfile_converter_algorithm::tfile_converter_algorithm(smart_tfile *const out_file)
: tfile_export_algorithm(out_file) {
	init();
}

void tfile_converter_algorithm::init() {
	// Create the Trigger tree
	tree_m = new TTree("Trigger", "Trigger");
    
    // Fill the data into the branch (channel) and create branch
	for (int i = 0; i < n_tdc_channels; i++) {
        std::string leaflist("ADC/I:TDC0:nHITS:TDC[nHITS]");
		tree_m->Branch(channel_names[i].c_str(), &(channels_m[i]), leaflist.c_str());	
	}
}

tfile_converter_algorithm::~tfile_converter_algorithm() {
    delete tree_m;
}

void tfile_converter_algorithm::process(line_entry const * in_entry) {
	std::cout << "Called with a line entry" << std::endl;
}

void tfile_converter_algorithm::process(midus_entry const * in_entry) {
	tfile_export_algorithm::process(in_entry);
	
    for (int ch = 0; ch < n_tdc_channels; ++ch) {
    	if (ch <= (qdc_ch_D4 - 1)) { // convert to index - qdc_ch_U0 = 1 !!!!)
        	channels_m[ch].adc = in_entry->get_value_in_branch(branch_qdc, ch);
        }
        else if (ch == 15) { // CdTe
        	// no adc2 branch to assign
        	channels_m[ch].adc= -100;
        }
        else {
        	// Ge0 or Ge1 counter
        	channels_m[ch].adc = in_entry->get_value_in_branch(ch - qdc_ch_D4 + 1, 0); // get the correct branch number (1 = adc0, 2 = adc1)
        }
		channels_m[ch].tdc0 = in_entry->get_value_in_branch(branch_tdc0, 0);
        
        int tdc_branch = branch_tdc1 + ch;
        int n_hits = in_entry->get_entries_in_branch(tdc_branch);
        channels_m[ch].n_tdc_hits = n_hits;
		for (int hit = 0; hit < n_hits; hit++) {
			channels_m[ch].tdc[hit] = in_entry->get_value_in_branch(tdc_branch, hit);
		}

    }
	
		
	// Fill the tree
	tree_m->Fill();
}
