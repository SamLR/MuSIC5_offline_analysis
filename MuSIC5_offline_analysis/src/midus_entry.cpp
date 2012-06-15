// midus_entry.cpp
// -- Implements the midus_entry methods
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>

#include <vector>

#include "midus_entry.h"
#include "algorithm.h"
#include "midus_tree_structs.h"


midus_entry::midus_entry(TDC_branch& tdc_in, QDC_branch& qdc_in) {
    init(tdc_in, qdc_in);
}

void midus_entry::accept(algorithm *const alg) const {
    alg->process(this);
}

void init(TDC_branch& tdc_in, QDC_branch& qdc_in) {
    
    if (tdc_in.entry_id_m != qdc_in.entry_id_m) {
        std::cerr <<"Entry IDs don't match" << std::endl;
    }
    
    for (int hit = 0; hit < tdc_in.n_hits_m; ++hit) {
        for (int ch = 0; ch < tdc_in.n_ch_m; ++ch) {
            TDC_m.push_back(tdc_in.value_m[hit][ch]);
        }
    }   
    
    for (int ch = 0 ; ch < qdc_in.n_ch_m; ++ch) {
        QDC_m.push_back(qdc_in.value_m[ch]);
    }
    
}
