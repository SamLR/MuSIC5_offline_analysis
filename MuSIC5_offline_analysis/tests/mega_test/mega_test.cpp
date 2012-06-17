// mega_test.cpp
// -- Test everything


#include <iostream>

#include "../../include/midus_file.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/calibration_functions.h"
#include "../../include/tfile_converter_algorithm.h"
#include "../../include/smart_tfile.h"
#include "../../include/printer_alg.h"
#include "../../include/scaler_printer.h"

int main() {
	// Open midus file
	midus_file* in_file = new midus_file("run00119.root");

	// add algorithm and calibration functions
	// Add calibration functions
	calibrate_func calib_fns[4] = { &null_calibration,
        &adc_calibration,
        &phadc_calibration, 
        &tdc_calibration};
	in_file->add_calibration_func(branch_qdc, calib_fns[1]);
	in_file->add_calibration_func(branch_adc0, calib_fns[2]);
	in_file->add_calibration_func(branch_adc1, calib_fns[2]);
	in_file->add_calibration_func(branch_tdc0, calib_fns[3]);
    
    smart_tfile* out_file = smart_tfile::getTFile("out.root", "RECREATE");
    tfile_converter_algorithm* tca = new tfile_converter_algorithm(out_file);
//    printer_alg* pa = new printer_alg();
    scaler_printer* sp = new scaler_printer();
    
    in_file->add_scaler_algorithm(sp);
    
    in_file->add_algorithm(tca);
//    in_file->add_algorithm(pa);
    
	
	// Call loop
	in_file->loop();
    out_file->close();
	return 0;
}
