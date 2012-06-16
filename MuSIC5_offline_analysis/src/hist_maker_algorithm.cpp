// hist_maker_algorithm.cpp
// -- Implements the methods to create a hisotgram from all input midus_entry
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <sstream>

#include "hist_maker_algorithm.h"

#include "TH1.h"

hist_maker_algorithm::hist_maker_algorithm(smart_tfile *const out_file, std::string histname, int n_bins, double x_low, double x_high): tfile_export_algorithm(out_file), histname_m(histname), n_bins_m(n_bins), x_low_m(x_low), x_high_m(x_high) {
	// Create the histogram
	hist_m = new TH1F(histname_m.c_str(), histname.c_str(), n_bins_m, x_low_m, x_high_m);
}

hist_maker_algorithm::~hist_maker_algorithm() {
}

void hist_maker_algorithm::process(line_entry const * in_entry) {
	std::cout << "Called with a line entry" << std::endl;
}
