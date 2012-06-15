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
    //std::cout << "probably not smart" << std::endl;
    std::cout << "Test QDC values: " << std::endl;
    for (int i = 0; i < in_entry->get_number_QDC_values(); i++) {
		std::cout << i << ": " << in_entry->get_QDC_value(i) << std::endl;
	}
	std::cout << "Test TDC values: " << std::endl;
    for (int i = 0; i < in_entry->get_number_TDC_values(); i++) {
		std::cout << i << ": " << in_entry->get_TDC_value(i) << std::endl;
	}
	std::cout << "Event number: " << in_entry->get_event_number() << std::endl;
}
