// root_functions.cpp
// -- Useful functions when running analyses

#include <iostream>
#include "root_functions.h"

void set_branch_addresses(in_branch branches[midus_structure::n_actual_channels], TTree* in_tree) {
	for (int i = 0; i < midus_structure::n_actual_channels; i++) {
		in_tree->SetBranchAddress(midus_structure::tdc_names[i+1].c_str(), &branches[i].in_channel);
	}
}
