// hist_branch_channel.cpp
// -- Simply plots a histogram all the values in a branch (ADC, TDC0 etc.) for a single channel 
// -- An example of how to use hist_maker_algorithm
// Created: 16/06/2012 Andrew Edmonds

#include <iostream>
#include "hist_branch_channel.h"

hist_branch_channel::hist_branch_channel(smart_tfile *const out_file, std::string histname, int channel, int branch, int n_bins, double x_low, double x_high): hist_maker_algorithm(out_file, histname, n_bins, x_low, x_high), channel_m(channel), branch_m(branch) {
}

hist_branch_channel::~hist_branch_channel() {
}

void hist_branch_channel::process(line_entry const * in_entry) {
	hist_maker_algorithm::process(in_entry);
}

void hist_branch_channel::process(midus_entry const * in_entry) {
	
	// Fill the histogram
	std::cout << branch_m << std::endl;
	if (branch_m == 0) { // ADC branch
		hist_maker_algorithm::fill_hist(in_entry->get_value_in_branch(branch_m, channel_m));
	}
	else if (branch_m == 1) { // TDC0 branch
		std::cout << in_entry->get_value_in_branch(branch_m, 0) << std::endl;
		hist_maker_algorithm::fill_hist(in_entry->get_value_in_branch(branch_m, 0)); 
	}
}
