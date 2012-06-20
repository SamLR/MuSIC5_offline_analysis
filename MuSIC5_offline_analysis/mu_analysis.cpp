//
//  main.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
// mu_analysis.cpp -- analyses tdc data

#include <iostream>
#include <cstdlib>
#include <sstream>

#include "midus_file.h"

#include "calibration_functions.h"
#include "hist_branch_channel.h"

void HelpMessage();

int main(int argc, 	char * argv[])
{
	// The command line arguments
	std::string input_filename;
	std::string output_filename;
	int n_entries_to_process = 0;
	
	if (argc < 2) {
		HelpMessage();
		exit(1);
	}
	
	int c;
	while ((c = getopt(argc, argv, "hi:on:")) != -1) {
		switch(c) {
		case 'h':
			HelpMessage();
			return 0;
			break;
			
		case 'i':
			input_filename = optarg;
			break;
			
		case 'o':
			output_filename = optarg;
			break;
			
		case 'n':
			n_entries_to_process = atoi(optarg);
			break;
			
		default:
			std::cout << "Invalid argument " << c << std::endl;
			break;
		}
	}
	
    // Create the input file object
    midus_file* in_file = new midus_file(input_filename);
    
    // Create the output file object
    if (output_filename == "") {
    	std::string temp = input_filename;
    	std::string temp_2;
    	std::stringstream temp_in_file;
    	
    	temp_in_file << temp;
    	std::getline(temp_in_file, temp_2, '.');
    	output_filename = temp_2;
    	output_filename += "_mu_analysis.root";
    }
    smart_tfile* out_file = smart_tfile::getTFile(output_filename, "RECREATE");
    
    
    // Add the tdc histograms
    hist_branch_channel* tdc_ch_hist[midus_structure::n_tdc_channels];
    for (int i = 0; i < midus_structure::n_tdc_channels; i++) {
    	std::stringstream histname;
    	if (i == midus_structure::eTDC_0) {
    		histname << "TDC0";
    	}
    	else if (i <= midus_structure::eQDC_U8 + 1) {
    		histname << "U" << i << ".TDC";
    	}
    	else if (i <= midus_structure::eQDC_D5 + 1) {
    		histname << "D" << i - (midus_structure::eQDC_U8 + 1);
    	}
    	else {
    		histname << "Ge" << i - (midus_structure::eQDC_D5 + 1);
    	}
   		tdc_ch_hist[i] = new hist_branch_channel(out_file, histname.str().c_str(), 0, midus_structure::eMEB_tdc0 + i, 100, 0, 20000);
    }
    
    // Add calibration functions
	in_file->add_calibration_func(midus_structure::eMEB_tdc0, &tdc_calibration); // NB all the tdc branches call the calib fn in calib[tdc0]
    
    // Add algorithms to the midus_file
    for (int i = 0; i < midus_structure::n_tdc_channels; i++) {
    	in_file->add_algorithm(tdc_ch_hist[i]);
    }
    
    // Loop through the file
    if (n_entries_to_process != 0) {
    	in_file->loop(n_entries_to_process);
    }
    else {
    	in_file->loop();
    }
    
    // Now fit function
    TF1* fit_fn = new TF1("fit", "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])",0, 20000);
    fit_fn->SetParName(0, "N_{B}");
    fit_fn->SetParName(1, "N_{#mu^{-}}");
    fit_fn->SetParName(2, "#tau_{Cu}");
    fit_fn->SetParameter(2, 160);
    fit_fn->SetParName(3, "N_{#mu^{+}}");
    fit_fn->SetParName(4, "#tau_{#mu}");
    fit_fn->SetParameter(4, 2200);
    for (int i = 0; i < midus_structure::n_tdc_channels; i++) {
    	tdc_ch_hist[i]->fit_hist(fit_fn);
    }
    
    // Write and close the output file
    out_file->close();
    
    return 0;
}

void HelpMessage() {
	std::cout << "The mu_analysis program does stuff\n";
	std::cout << "Command line arguments: " << std::endl;
	std::cout << "\t -h  --  prints this help message\n";
	std::cout << "\t -i  --  filename of the input MIDAS ROOT file to convert (e.g. -i example.root)\n";
	std::cout << "\t -o  --  filename of the output ROOT file\n\t\t (if not given then the output file is called example_converted.root in the same directory as the input file)\n\n";
	std::cout << "\t -n  --  the number of entries in the input file to process\n";
}

