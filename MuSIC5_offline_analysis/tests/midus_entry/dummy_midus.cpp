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
    for (int i = 0; i < n_loops_m; ++i) {
        
        midus_out_branch b [2];
        for (int j  =0 ; j<2; ++j) {
            b[j].n_entries = 4; 
            for (int k= 0; k < 4; ++k) {
                b[j].data[k] = k + i + j;
            }
        }
        midus_entry entry(b);
        
        for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
            entry.accept(get_algorithm(alg));
        }
        
    }
}