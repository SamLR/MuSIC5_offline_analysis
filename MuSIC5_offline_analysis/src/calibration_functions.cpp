//
//  calibration_functions.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 17/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include "calibration_functions.h"


double null_calibration(int const ch, int const val, int const para1) {
    return val;
}

double qdc_calibration(int const ch, int const val, int const para1) {
    return val;
}

double adc_calibration(int const ch, int const val, int const para1) {
    return val;
}

double tdc_calibration(int const ch, int const val, int const para1) {
	// double new_val = ((val - para1)/40)*1.025;
	double new_val = (val - para1)*0.024414;
    return new_val;
}
