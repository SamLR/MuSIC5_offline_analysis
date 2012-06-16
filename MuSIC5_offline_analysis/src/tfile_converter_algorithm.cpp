// tfile_converter_algorithm.cpp
// -- Implements the methods to convert from an input midus ROOT file to another format of ROOT file
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <sstream>

#include "tfile_converter_algorithm.h"

#include "TTree.h"

tfile_converter_algorithm::tfile_converter_algorithm(TFile *const out_file): tfile_export_algorithm(out_file) {
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
	int channel_U1[MAX_ENTRIES];	
	for (int i = 0; i < in_entry->get_entries_in_branch(0); i++) {
		channel_U1[i] = in_entry->get_value_in_branch(0, i);
	}
	for (int i = in_entry->get_entries_in_branch(0); i < in_entry->get_entries_in_branch(0) + in_entry->get_entries_in_branch(1); i++) {
		channel_U1[i] = in_entry->get_value_in_branch(1, i);
	}
	
	std::stringstream leaflist;
	leaflist << "ADC1[" << in_entry->get_entries_in_branch(0) << "]/I:TDC1[" << in_entry->get_entries_in_branch(1) << "]/I";
	tree_m->Branch("U1", channel_U1, leaflist.str().c_str());
		
	// Fill the tree
	tree_m->Fill();
}
