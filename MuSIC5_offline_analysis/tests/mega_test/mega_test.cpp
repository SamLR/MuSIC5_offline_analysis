// mega_test.cpp
// -- Test everything


#include <iostream>

#include "../../include/midus_file.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/calibration_functions.h"
#include "../../include/tfile_converter_algorithm.h"
#include "../../include/smart_tfile.h"
#include "../../include/printer_alg.h"
#include "../../include/hist_branch_channel.h"
#include "../../include/hist_mu_lifetime.h"


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
//	hist_branch_channel* adc_U1_hist = new hist_branch_channel(out_file, "U1.adc", qdc_ch_U1, branch_qdc, 400, 0, 200);
//	hist_branch_channel* adc_Ge0_hist = new hist_branch_channel(out_file, "Ge0.adc", phadc_ch_Ge0, branch_adc0, 400, 0, 400);
//	hist_branch_channel* adc_Ge1_hist = new hist_branch_channel(out_file, "Ge1.adc", phadc_ch_Ge1, branch_adc1, 400, 0, 400);
//	hist_branch_channel* tdc0 = new hist_branch_channel(out_file, "tdc0", 0, branch_tdc0, 400, 0, 1e7);
//	hist_branch_channel* tdc7 = new hist_branch_channel(out_file, "tdc7", 0, qdc_ch_U6 + branch_tdc0, 1000, 0, 1e7); // NB tdc corresponds to channel U6 (because tdc1 corresponds to U0)
	hist_mu_lifetime* mu_lifetime = new hist_mu_lifetime(out_file, "mu_life");
    
	in_file->add_algorithm(tca);
//    in_file->add_algorithm(pa);
//	in_file->add_algorithm(adc_U1_hist);
//	in_file->add_algorithm(adc_Ge0_hist);
//	in_file->add_algorithm(adc_Ge1_hist);
//	in_file->add_algorithm(tdc0);
//	in_file->add_algorithm(tdc7);
	in_file->add_algorithm(mu_lifetime);
    
	
	// Call loop
	in_file->loop();
    out_file->close();
	return 0;
}
