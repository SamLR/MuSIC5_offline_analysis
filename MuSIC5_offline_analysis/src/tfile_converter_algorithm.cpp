// tfile_converter_algorithm.cpp
// -- Implements the methods to convert from an input midus ROOT file to another format of ROOT file
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <sstream>

#include "tfile_converter_algorithm.h"

#include "TTree.h"

tfile_converter_algorithm::tfile_converter_algorithm(TFile *const out_file): tfile_export_algorithm(out_file) {
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
	double QDC_values[in_entry->get_number_QDC_channels()];
	double TDC_values[in_entry->get_number_TDC_channels()][in_entry->get_number_TDC_hits()];
	
	// Set the branch addresses
	// Each QDC branch will represent one channel
	for (int i = 0; i < in_entry->get_number_QDC_channels(); i++) {
		std::stringstream ss;
		ss << "QDC.ch" << (i+1);
		tree_m->Branch(ss.str().c_str(), &QDC_values[i]);
	}
	// Each TDC branch will represent one channel but will have many hits
	for (int i = 0; i < in_entry->get_number_TDC_channels(); i++) {
		std::stringstream ss;
		ss << "TDC.ch" << (i+1);
		
		std::stringstream leaflist;
		leaflist << "Hit[" << in_entry->get_number_TDC_hits() << "]/D";
		tree_m->Branch(ss.str().c_str(), TDC_values[i], leaflist.str().c_str());
	}
	
	// Get the values
	for (int i = 0; i < in_entry->get_number_QDC_channels(); i++) {
		QDC_values[i] = in_entry->get_QDC_value(i);
	}
	
	for (int i = 0; i < in_entry->get_number_TDC_channels(); i++) {
		for (int j = 0; j < in_entry->get_number_TDC_hits(); j++) {
			TDC_values[i][j] = in_entry->get_TDC_value(j*in_entry->get_number_TDC_channels() + i);
		}
	}
		
	// Fill the tree
	tree_m->Fill();	
}
