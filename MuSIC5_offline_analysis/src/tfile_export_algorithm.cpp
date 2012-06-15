// tfile_export_algorithm.cpp
// -- Implements the methods
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>

#include "tfile_export_algorithm.h"

tfile_export_algorithm::tfile_export_algorithm(TFile* const in_file): in_file_m(in_file) {
	in_file_m->cd();
}

tfile_export_algorithm::~tfile_export_algorithm() {
}

void tfile_export_algorithm::process(line_entry const *) {
	std::cout << "Called with a line entry" << std::endl;
}

void tfile_export_algorithm::process(midus_entry const *) {
	std::cout << "Called with a midus_entry" << std::endl;
}
