// hist_mu_lifetime.cpp
// -- Plots a histogram of <eqn> corresponding to muon lifetime
// Created: 17/06/2012 Andrew Edmonds

#include <iostream>
#include "hist_mu_lifetime.h"

hist_mu_lifetime::hist_mu_lifetime(smart_tfile *const out_file, std::string histname, int n_bins, double x_low, double x_high): hist_maker_algorithm(out_file, histname, n_bins, x_low, x_high) {
}

hist_mu_lifetime::~hist_mu_lifetime() {
}

void hist_mu_lifetime::process(line_entry const * in_entry) {
	hist_maker_algorithm::process(in_entry);
}

void hist_mu_lifetime::process(midus_entry const * in_entry) {
	
	int tdc0 = in_entry->get_value_in_branch(branch_T0, 0);
	
	for (int i = 0; i < in_entry->get_entries_in_branch(branch_TDC1); i++) {
		int tdc1 = in_entry->get_value_in_branch(branch_TDC1, i);
		hist_maker_algorithm::fill_hist(tdc1 -tdc0);
	}
	
	for (int i = 0; i < in_entry->get_entries_in_branch(branch_TDC2); i++) {
		int tdc2 = in_entry->get_value_in_branch(branch_TDC2, i);
		hist_maker_algorithm::fill_hist(tdc2 -tdc0);
	}
}
