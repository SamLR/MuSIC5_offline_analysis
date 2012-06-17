// hist_x_ray.cpp
// -- Plots a histogram of <eqn> corresponding to x-ray energy
// Created: 17/06/2012 Andrew Edmonds

#include <iostream>
#include "hist_x_ray.h"

hist_x_ray::hist_x_ray(smart_tfile *const out_file, std::string histname, int n_bins, double x_low, double x_high): hist_maker_algorithm(out_file, histname, n_bins, x_low, x_high) {
}

hist_x_ray::~hist_x_ray() {
}

void hist_x_ray::process(line_entry const * in_entry) {
	hist_maker_algorithm::process(in_entry);
}

void hist_x_ray::process(midus_entry const * in_entry) {

	for (int i = 0; i < in_entry->get_entries_in_branch(branch_adc0); i++) { // 3 channels for PHADC
		hist_maker_algorithm::fill_hist(in_entry->get_value_in_branch(branch_adc0, i));
	}
}
