// mega_test.cpp
// -- Test everything


#include <iostream>

#include "../../include/midus_file.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/calibration_functions.h"

int main() {
	// Open midus file
	midus_file* file = new midus_file("../../rootfiles/run00077.root");

	// add algorithm and calibration functions
	// Add calibration functions
	calib_func* calib_fns[4] = { &null_calibration, &adc_calibrtion, &phadc_calibration, &tdc_calibration };
	file->add_calibration_func(branch_qdc, calib_fns[1]);
	file->add_calibration_func(branch_adc0, calib_fns[2]);
	file->add_calibration_func(branch_adc1, calib_fns[2]);
	file->add_calibration_func(branch_tdc, calib_fns[3]);
	
	// Call loop
	file->loop();
	return 0;
}
