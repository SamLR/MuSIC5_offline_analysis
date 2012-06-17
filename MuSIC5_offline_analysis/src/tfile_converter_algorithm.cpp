// tfile_converter_algorithm.cpp
// -- Implements the methods to convert from an input midus ROOT file to another format of ROOT file
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <sstream>

#include "tfile_converter_algorithm.h"

#include "TTree.h"

tfile_converter_algorithm::tfile_converter_algorithm(smart_tfile *const out_file): tfile_export_algorithm(out_file) {
	init();
}

void tfile_converter_algorithm::init() {
	// Create the Trigger tree
	tree_m = new TTree("Trigger", "Trigger");
}

tfile_converter_algorithm::~tfile_converter_algorithm() {
}

void tfile_converter_algorithm::process(line_entry const * in_entry) {
	std::cout << "Called with a line entry" << std::endl;
}

void tfile_converter_algorithm::process(midus_entry const * in_entry) {
	tfile_export_algorithm::process(in_entry);
	
	// Set the branch
	channel ch[n_channels];	 // 2 channels (U1 & U2),for each channel: ADC int, TDC0 int. TDC1 ints
	std::string channel_names[2];
	channel_names[0] = "U1";
	channel_names[1] = "U2";
	
	// Fill the data into the branch (channel) and create branch
	for (int i = 0; i < n_channels; i++) {
		ch[i].adc = in_entry->get_value_in_branch(0, i);
		ch[i].tdc0 = in_entry->get_value_in_branch(1, 0);
		for (int j = 0; j < in_entry->get_entries_in_branch(i + 2); j++) {
			ch[i].tdc[j] = in_entry->get_value_in_branch(i + 2, j);
		}
		std::stringstream leaflist;
		leaflist << "ADC/I:TDC0:TDC[" << in_entry->get_entries_in_branch(i + 2) << "]";
		tree_m->Branch(channel_names[i].c_str(), &ch[i], leaflist.str().c_str());	
	}
		
	// Fill the tree
	tree_m->Fill();
}
