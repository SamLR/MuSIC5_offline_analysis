// midus_entry.cpp
// -- Implements the midus_entry methods
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <vector>

#include "midus_entry.h"
#include "algorithm.h"
#include "midus_tree_structs.h"

midus_entry::midus_entry(midus_out_branch const branch []){
    init(branch);
}

void midus_entry::accept(algorithm *const alg) const {
    alg->process(this);
}

void midus_entry::init(midus_out_branch const branch[]) {
    for (int b = 0; b<n_branches; ++b) {
        branches_m[b].n_entries = branch[b].n_entries;
        for (int i = 0; i < branches_m[b].n_entries; ++i) {
            branches_m[b].data[i] = branch[b].data[i];
        }
    }
}
