// tfile_converter_algorithm.cpp
// -- Implements the methods to convert from an input midus ROOT file to another format of ROOT file
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <sstream>

#include "tfile_converter_algorithm.h"

#include "TTree.h"

tfile_converter_algorithm::tfile_converter_algorithm(smart_tfile *const out_file): tfile_export_algorithm(out_file), ref_count_m(0) {
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
	
	ref_count_m++;
	
	// Set the branch
	int channel[MAX_ENTRIES];	
	for (int i = 0; i < in_entry->get_entries_in_branch(0); i++) {
		channel[i] = in_entry->get_value_in_branch(0, i);
	}
	for (int i = in_entry->get_entries_in_branch(0); i < in_entry->get_entries_in_branch(0) + in_entry->get_entries_in_branch(1); i++) {
		channel[i] = in_entry->get_value_in_branch(1, i);
	}
	
	std::stringstream branchname;
	branchname << "U" << ref_count_m;
	std::stringstream leaflist;
	leaflist << "ADC[" << in_entry->get_entries_in_branch(0) << "]/I:TDC[" << in_entry->get_entries_in_branch(1) << "]/I";
	tree_m->Branch(branchname.str().c_str(), channel, leaflist.str().c_str());
		
	// Fill the tree
	tree_m->Fill();
}
