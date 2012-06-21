// root_functions.h
// -- Useful functions when running analyses

#ifndef ROOT_FUNCTIONS_H_
#define ROOT_FUNCTIONS_H_

#include <string>

#include "midus_structure.h"

#include "TTree.h"
#include "TBranch.h"

struct in_branch {
	std::string branchname;
	midus_structure::channel in_channel;
};

void set_branch_addresses(in_branch branches[midus_structure::n_tdc_channels], TTree* in_tree);

#endif
