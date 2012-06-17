// hist_ADC_channel.cpp
// -- Simply plots a histogram of the charges in a single ADC channel
// -- An example of how to use hist_maker_algorithm
// Created: 16/06/2012 Andrew Edmonds

#include <iostream>
#include "hist_ADC_channel.h"

hist_ADC_channel::hist_ADC_channel(smart_tfile *const out_file, std::string histname, int channel, int n_bins, double x_low, double x_high): hist_maker_algorithm(out_file, histname, n_bins, x_low, x_high), channel_m(channel) {
}

hist_ADC_channel::~hist_ADC_channel() {
}

void hist_ADC_channel::process(line_entry const * in_entry) {
	hist_maker_algorithm::process(in_entry);
}

void hist_ADC_channel::process(midus_entry const * in_entry) {
	
	// Fill the histogram
	hist_maker_algorithm::fill_hist(in_entry->get_value_in_branch(0, channel_m));
}
