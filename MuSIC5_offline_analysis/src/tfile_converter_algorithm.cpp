// tfile_converter_algorithm.cpp
// -- Implements the methods to convert from an input midus ROOT file to another format of ROOT file
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <sstream>

#include "tfile_converter_algorithm.h"

#include "TTree.h"

std::string const tfile_converter_algorithm::channel_names[midus_structure::n_tdc_channels] =
{ "U1", "U2", "U3", "U4",  "U5", "U6",  "U7", "U8", "D1", "D2", "D3", "D4", "D5", "Ge1", "Ge2",  "CdTe"};

tfile_converter_algorithm::tfile_converter_algorithm(smart_tfile *const out_file)
: tfile_export_algorithm(out_file) {
	init();
}

void tfile_converter_algorithm::init() {
	// Create the Trigger tree
	tree_m = new TTree("Trigger", "Trigger");
    
    // Fill the data into the branch (channel) and create branch
	for (int i = 0; i < midus_structure::n_tdc_channels; i++) {
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
	
    for (int ch = 0; ch < midus_structure::n_tdc_channels; ++ch) {
    	if (ch <= midus_structure::eQDC_D5) {
        	channels_m[ch].adc = in_entry->get_value_in_branch(midus_structure::eMEB_qdc, ch);
        }
        else if (ch == midus_structure::eQDC_D5 + 1) { // Ge1
        	channels_m[ch].adc = in_entry->get_value_in_branch(midus_structure::eMEB_adc0, 0); 
        }
        else if (ch == midus_structure::eQDC_D5 + 2) { // Ge2
        	channels_m[ch].adc = in_entry->get_value_in_branch(midus_structure::eMEB_adc1, 0); 
        }
		channels_m[ch].tdc0 = in_entry->get_value_in_branch(midus_structure::eMEB_tdc0, 0);
        
        int tdc_branch = midus_structure::eMEB_tdc0 + ch + 1;
        int n_hits = in_entry->get_entries_in_branch(tdc_branch);
        channels_m[ch].n_tdc_hits = n_hits;
		for (int hit = 0; hit < n_hits; hit++) {
			channels_m[ch].tdc[hit] = in_entry->get_value_in_branch(tdc_branch, hit);
		}

    }
	
		
	// Fill the tree
	tree_m->Fill();
}
