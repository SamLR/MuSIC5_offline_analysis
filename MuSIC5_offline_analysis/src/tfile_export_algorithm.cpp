// tfile_export_algorithm.cpp
// -- Implements the methods
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>

#include "tfile_export_algorithm.h"

tfile_export_algorithm::tfile_export_algorithm(TFile* *const out_file): out_file_m(out_file) {
}

tfile_export_algorithm::~tfile_export_algorithm() {
	out_file_m->close(); // will write if no more pointer pointing
}

void tfile_export_algorithm::process(midus_entry const *) {
}
