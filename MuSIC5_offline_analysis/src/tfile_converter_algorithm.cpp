// tfile_converter_algorithm.cpp
// -- Implements the methods to convert from an input midus ROOT file to another format of ROOT file
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <sstream>

#include "tfile_converter_algorithm.h"

#include "TTree.h"

#define MAX_ENTRIES 500

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
	int channel[MAX_ENTRIES];	 // ADC int, TDC0 int. TDC1 ints
	channel[0] = in_entry->get_value_in_branch(0, 0);
	channel[1] = in_entry->get_value_in_branch(1, 0);
	//for (int i = 0; i < in_entry->get_number_of_branches(); i++) { // 4 branches for test
		for (int j = 0; j < in_entry->get_entries_in_branch(2); j++) {
			channel[j + 2] = in_entry->get_value_in_branch(2, j);
		}
	//}
	
	std::string branchname("U1"); // branch is channel
	std::stringstream leaflist;
	leaflist << "ADC.chU1/I:TDC0:TDC.chU1[" << in_entry->get_entries_in_branch(2) << "]";
	tree_m->Branch(branchname.c_str(), channel, leaflist.str().c_str());
		
	// Fill the tree
	tree_m->Fill();
}
