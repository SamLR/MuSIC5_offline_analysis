//
//  conversion_branch_structure.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 19/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include <string>
#include "midus_structure.h"

namespace {
    // define a useful local-only function
    int const _get_id_from_string(std::string const str, 
                                  int const max, 
                                  std::string const vals[]) {
        for (int i = 0; i < max; ++i) {
            if (str == vals[i]) {
                return i;
            }
        }
        std::cerr << "Sorry, "<< str << " not found; returning '-1'" << std::endl;
        return -1;
    }
}


namespace midus_structure {
    int const get_branch_number(std::string const branch_name) {
        return _get_id_from_string(branch_name, 
                                   n_branches_in_midus_entry, branch_names);
    }
    
    // The QDC and TDC share channel numbers
    int const get_channel_number(std::string const channel_name) {
        return _get_id_from_string(channel_name, 
                                   n_tdc_channels, tdc_names);
    }
    
    std::string const get_branch_name(const int b) {
        return branch_names[b];
    }
    std::string const get_channel_name(const int ch) {
        return tdc_names[ch];
    }    
}
