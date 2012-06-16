// midus_entry.cpp
// -- Implements the midus_entry methods
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <vector>

#include "midus_entry.h"
#include "algorithm.h"
#include "midus_tree_structs.h"

midus_entry::midus_entry(midus_out_branch const& branch){
    init(branch);
}

void midus_entry::accept(algorithm *const alg) const {
    alg->process(this);
}

void midus_entry::init(midus_out_branch const& branch){
//    
//    n_tdc_vals_m = branch.n_tdc;
//    n_qdc_vals_m = branch.n_qdc;
//    
//    
//    for (int hit = 0; hit < n_tdc_vals_m; ++hit) {
//        tdc_vals_m[hit] = branch.tdc0[hit];
//    }   
//    
//    for (int ch = 0 ; ch < n_qdc_vals_m; ++ch) {
//        qdc_vals_m[ch] = branch.qdc0[ch];
//    }
    
}
