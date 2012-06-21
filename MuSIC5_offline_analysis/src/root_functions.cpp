// root_functions.cpp
// -- Useful functions when running analyses

#include <iostream>
#include "root_functions.h"

void set_branch_addresses(in_branch branches[midus_structure::n_tdc_channels], TTree* in_tree) {
	for (int i = 1; i < midus_structure::n_tdc_channels; i++) {
		in_tree->SetBranchAddress(midus_structure::tdc_names[i].c_str(), &branches[i-1].in_channel);
	}
}
