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
    
    if (tdc_in.entry_id_m != qdc_in.entry_id_m) {
        std::cerr <<"Entry IDs don't match" << std::endl;
        return;
    }
    event_number_m = tdc_in.entry_id_m;
    n_tdc_hits_m = tdc_in.n_hits_m;
    n_tdc_ch = tdc_in.n_ch_m;
    n_qdc_ch = qdc_in.n_ch_m;
    
    for (int hit = 0; hit < n_tdc_hits_m; ++hit) {
        for (int ch = 0; ch < n_tdc_ch; ++ch) {
            int val = tdc_in.value_m[hit][ch];
            TDC_m.push_back(val);
        }
    }   
    
    for (int ch = 0 ; ch < n_qdc_ch; ++ch) {
        int val = qdc_in.value_m[ch];
        QDC_m.push_back(val);
    }
    
}
