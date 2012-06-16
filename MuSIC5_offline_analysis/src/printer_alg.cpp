//
//  printer_alg.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>

#include "printer_alg.h"
#include "line_entry.h"
#include "midus_entry.h"

// print lines of a file
void printer_alg::process(line_entry const* in_entry){
    std::cout << in_entry->get_line() << std::endl;
}

// currently print errors, once more is known this will 
// act as a scan and print actual information
void printer_alg::process(midus_entry const* in_entry){
    for (int b = 0; b < in_entry->get_number_of_branches(); ++b) {
        int leaves = in_entry->get_entries_in_branch(b);
        std::cout << "number of leaves: " << leaves<<std::endl;
        for (int i = 0; i < leaves; ++i) {
            std::cout<<"data is: "<<in_entry->get_value_in_branch(b, i) << std::endl;
        }
    }
}
