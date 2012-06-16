// tfile_converter_algorithm.cpp
// -- Implements the methods to convert from an input midus ROOT file to another format of ROOT file
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <sstream>

#include "tfile_converter_algorithm.h"

#include "TTree.h"

tfile_converter_algorithm::tfile_converter_algorithm(smart_tfile *const out_file): tfile_export_algorithm(out_file) {
}

tfile_converter_algorithm::~tfile_converter_algorithm() {
}

void tfile_converter_algorithm::process(line_entry const * in_entry) {
	std::cout << "Called with a line entry" << std::endl;
}

void tfile_converter_algorithm::process(midus_entry const * in_entry) {
	tfile_export_algorithm::process(in_entry);
	
	//Create the TTree
	tree_m = new TTree("Event", "Event");
	
	// Create the arrays where we'll read the values to
	double QDC_values[in_entry->get_number_QDC_values()];
	double TDC_values[in_entry->get_number_TDC_values()];
	
	// Set the branch addresses
	for (int i = 0; i < in_entry->get_number_QDC_values(); i++) {
		std::stringstream ss;
		ss << "QDC.ch" << (i+1);
		tree_m->Branch(ss.str().c_str(), &QDC_values[i]);
	}
	// Each TDC branch will represent one channel but will have many hits
	for (int i = 0; i < in_entry->get_number_TDC_values(); i++) {
		std::stringstream ss;
		ss << "TDC.ch" << (i+1);
		
		std::stringstream leaflist;
		//leaflist << "Hit[" << in_entry->get_number_TDC_hits() << "]/D";
		tree_m->Branch(ss.str().c_str(), &TDC_values[i]);
	}
	
	// Get the values
	for (int i = 0; i < in_entry->get_number_QDC_values(); i++) {
		QDC_values[i] = in_entry->get_QDC_value(i);
	}
	
	for (int i = 0; i < in_entry->get_number_TDC_values(); i++) {
		TDC_values[i] = in_entry->get_TDC_value(i);
	}
		
	// Fill the tree
	tree_m->Fill();
}
