// tfile_converter_algorithm.cpp
// -- Implements the methods to convert from an input midus ROOT file to another format of ROOT file
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>

#include "tfile_converter_algorithm.h"

#include "TTree.h"
#include "TH1.h"

tfile_converter_algorithm::tfile_converter_algorithm(TFile *const out_file): tfile_export_algorithm(out_file) {
	//Create the TTree
	tree_m = new TTree("t", "t");
}

tfile_converter_algorithm::~tfile_converter_algorithm() {
}

void tfile_converter_algorithm::process(line_entry const * in_entry) {
	std::cout << "Called with a line entry" << std::endl;
}

void tfile_converter_algorithm::process(midus_entry const * in_entry) {
	tfile_export_algorithm::process(in_entry);
	
	// Create the branche for the event
	double QDC_ch2 = in_entry->get_QDC_value(1);
	std::cout << QDC_ch2 << std::endl;
	tree_m->Branch("QDC.ch2", &QDC_ch2);
	
	// Take the entry (contains <vectors>)
	tree_m->Fill();
	
	// Write to the TTree
	tfile_export_algorithm::write();
}
