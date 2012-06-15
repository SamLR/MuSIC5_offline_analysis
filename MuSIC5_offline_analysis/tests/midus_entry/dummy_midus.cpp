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
    int const n_ch = 2;
    int const n_hits = 2;
    for (int i = 0; i < n_loops_m; ++i) {
        TDC_branch t;
        t.entry_id_m = i;
        t.n_ch_m = n_ch;
        t.n_hits_m = n_hits;
        
        QDC_branch q;
        q.entry_id_m = i;
        q.n_ch_m = n_ch;
        
        for (int ch = 0; ch < n_ch; ++ch) {
            q.value_m[ch] = i%ch;
            for (int hit = 0; hit<n_hits; ++hit) {
                t.value_m[hit][ch] = (9%ch)%hit;
            }
        }
        midus_entry entry(t, q);
        
        for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
            entry.accept(get_algorithm(alg));
        }
        
    }
}