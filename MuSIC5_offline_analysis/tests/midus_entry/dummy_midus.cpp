//
//  dummy_midus.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 15/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>

#include "dummy_midus.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/midus_entry.h"

void dummy_midus::loop(){
    int n_entries = 5;
    for (int i = 0; i < n_loops_m; ++i) {
        trigger_branch t;
        
        for (int i = 0; i < n_entries; ++i) {
            t.n_qdc = n_entries;
            t.n_tdc = 2*n_entries;
            t.qdc0[i] = i;
            t.tdc0[i*2] = 2*i;
            t.tdc0[i*2+1] = 2*i+1;
        }
        
        
        midus_entry entry(t);
        
        for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
            entry.accept(get_algorithm(alg));
        }
        
    }
}