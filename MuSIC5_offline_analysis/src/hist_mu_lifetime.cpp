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
	
	for (int i = 0; i < n_channels; i++) {
		int branch_id = i + (n_branches_in_trigger_tree - n_channels); // see defn of these variables in midus_tree_structs.h
		for (int j = 0; j < in_entry->get_entries_in_branch(branch_id); j++) {
			int tdc = in_entry->get_value_in_branch(branch_id, j);
			hist_maker_algorithm::fill_hist(tdc - tdc0);
		}
	}
}
