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
    int const n_qdc = in_entry->get_number_QDC_values();
    int const n_tdc = in_entry->get_number_TDC_values();
    std::cout << "Test QDC "<< n_qdc << " values: " << std::endl;
    for (int i = 0; i < n_qdc; i++) {
		std::cout << i << ": " << in_entry->get_QDC_value(i) << std::endl;
	}
	std::cout << "Test TDC "<< n_tdc <<" values: " << std::endl;
    for (int i = 0; i < n_tdc; i++) {
		std::cout << i << ": " << in_entry->get_TDC_value(i) << std::endl;
	}
	std::cout << "Event number: " << in_entry->get_event_number() << std::endl;
}
