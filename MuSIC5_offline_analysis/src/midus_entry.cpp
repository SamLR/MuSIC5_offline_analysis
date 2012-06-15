// midus_entry.cpp
// -- Implements the midus_entry methods
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <vector>

#include "midus_entry.h"
#include "algorithm.h"
#include "midus_tree_structs.h"

midus_entry::midus_entry(TDC_branch const& tdc_in, QDC_branch const& qdc_in): QDC_m(0), TDC_m(0){
    init(tdc_in, qdc_in);
}

void midus_entry::accept(algorithm *const alg) const {
    alg->process(this);
}

void midus_entry::init(TDC_branch const& tdc_in, QDC_branch const& qdc_in){
    
    n_tdc_hits_m = *tdc_in.n_hits;
    n_tdc_ch = 4;
    n_qdc_ch = 4;
    
    for (int hit = 0; hit < n_tdc_hits_m; ++hit) {
        for (int ch = 0; ch < n_tdc_ch; ++ch) {
            int val = tdc_in.value_m[hit][ch];
            TDC_m.push_back(val);
        }
    }   
    
    for (int ch = 0 ; ch < n_qdc_ch; ++ch) {
        int val = qdc_in.qdc[ch];
        QDC_m.push_back(val);
    }
    
}
