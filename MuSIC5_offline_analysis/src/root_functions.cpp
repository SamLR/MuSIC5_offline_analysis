// root_functions.cpp
// -- Useful functions when running analyses

#include <iostream>
#include <string>
#include "root_functions.h"


void set_branch_addresses(in_branch branches[midus_structure::n_actual_channels], TTree* in_tree) {
	for (int i = 0; i < midus_structure::n_actual_channels; i++) {
		in_tree->SetBranchAddress(midus_structure::tdc_names[i+1].c_str(), &branches[i].in_channel);

		branches[i].in_channel.adc = 0;
		branches[i].in_channel.tdc0 = 0;
		branches[i].in_channel.n_tdc_hits = 0;
		for(unsigned int j = 0; j < midus_structure::max_data_entries; ++j) {
			branches[i].in_channel.tdc[j] = 0;
		}

		branches[i].branchname.assign(midus_structure::tdc_names[i+1]);
	}
}
