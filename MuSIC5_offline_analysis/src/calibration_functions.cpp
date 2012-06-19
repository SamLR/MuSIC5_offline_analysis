//
//  calibration_functions.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 17/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include "calibration_functions.h"


int null_calibration(int const ch, int const val, int const para1) {
    return val;
}

int qdc_calibration(int const ch, int const val, int const para1) {
    return val;
}

int adc_calibration(int const ch, int const val, int const para1) {
    return val;
}

int tdc_calibration(int const ch, int const val, int const para1) {
	//std::cout << para1 << std::endl;
	//int new_val = ((val - para1)/40)*1.025;
    return val;
}
