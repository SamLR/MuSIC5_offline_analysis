//
//  scaler_printer.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 17/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include "scaler_printer.h"
#include "scaler_entry.h"

void scaler_printer::process(scaler_entry const* entry){
    for (int ch = 0; ch < scaler_entry::get_n_channels(); ++ch) {
        std::cout << scaler_entry::get_channel_name(ch) << " has value ";
        std::cout << entry->get_value(ch) << std::endl;
    }
}