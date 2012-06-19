//
//  scaler_entry.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 17/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>

#include "scaler_entry.h"
#include "midus_structure.h"
#include "scaler_algorithm.h"

scaler_entry::scaler_entry(int const in_values[midus_structure::n_scaler_ch]) {
    for (int ch = 0; ch < midus_structure::n_scaler_ch; ++ch) {
        data[ch] = in_values[ch];
    }
}

void scaler_entry::accept (scaler_algorithm *const alg) const{
    alg->process(this);
}
