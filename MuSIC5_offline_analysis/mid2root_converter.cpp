//
//  main.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include <cstdlib>
#include <sstream>

#include "midus_file.h"

#include "tfile_converter_algorithm.h"
#include "hist_branch_channel.h"

int main(int argc, 	char * argv[])
{
	// Command line args - string filename to process
	//					 - optional output file name (xxxx_converted.root)
	//					 - optional flags to control display of ADC (e.g. -ADC and next number is which ADC to plot)
	// -i input
	// -o output
	// -q qdc channel
	// -a adc channel
	// -t tdc channelegitbuild proect not producing binary
	
	// The command line arguments
	std::string input_filename;
	std::string output_filename;
	
	std::string long_arg;
	std::string channel;
	int qdc_chs_to_draw[13]; // NB need to change array limit
	int n_qdcs_to_draw = 0; // 1 to 13
	int adc_chs_to_draw[2]; 
	int n_adcs_to_draw = 0; // 0 to 1 (Ge0, Ge1)
	int tdc_chs_to_draw[16]; 
	int n_tdcs_to_draw = 0; // 0 to 15 (t0, U0...U7, D0...D4, Ge0, Ge1)
	
	if (argc < 2) {
		std::cout << "Incorrect number of arguments" << std::endl;
		std::cout << "Arguments: -i [input_filename] -o [output_filename] -q \"[qdc_channel_numbers]\" -a \"[adc_channel_numbers]\" " 
				<< "-t \"[tdc_channel_numbers]\" " << std::endl;
		exit(1);
	}
	
	int c;
	while ((c = getopt(argc, argv, "i:o:q:a:t:")) != -1) {
		switch(c) {
		case 'i':
			input_filename = optarg;
			break;
			
		case 'o':
			output_filename = optarg;
			break;
			
		case 'q':
			// optarg will come in as a string of numbers separated by spaces
			long_arg = optarg;
			for (int i = 0; i <= long_arg.size(); i++) {
				if (i == long_arg.size() || long_arg[i] == ' ') {
					// later will convert from string
					qdc_chs_to_draw[n_qdcs_to_draw] = atoi(channel.c_str());
					n_qdcs_to_draw++;	
					channel.clear();
				}
				else {
					channel.push_back(long_arg[i]);
				}
			}
			break;
			
		case 'a':
			// optarg will come in as a string of numbers separated by spaces
			long_arg = optarg;
			for (int i = 0; i <= long_arg.size(); i++) {
				if (i == long_arg.size() || long_arg[i] == ' ') {
					// later will convert from string
					adc_chs_to_draw[n_adcs_to_draw] = atoi(channel.c_str());
					n_adcs_to_draw++;
					channel.clear();
				}
				else {
					channel.push_back(long_arg[i]);
				}
			}
			break;
			
		case 't':
			// later will convert from string
			tdc_chs_to_draw[n_tdcs_to_draw] = atoi(optarg);
			n_tdcs_to_draw++;
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
    	output_filename += "_converted.root";
    }
    smart_tfile* out_file = smart_tfile::getTFile(output_filename, "RECREATE");
    
    
    // Find out if we want to plot a qdc channel
    hist_branch_channel* qdc_ch_hist[n_qdcs_to_draw];
    for (int i = 0; i < n_qdcs_to_draw; i++) {
   		if (qdc_chs_to_draw[i] < qdc_ch_U0 || qdc_chs_to_draw[i] > qdc_ch_D4) {
   			std::cout << "Invalid qdc channel number " << qdc_chs_to_draw[i] << std::endl;
    		qdc_ch_hist[i] = NULL;
   		}
   		std::stringstream histname;
   		histname << "X" << qdc_chs_to_draw[i] << ".ADC";
   		qdc_ch_hist[i] = new hist_branch_channel(out_file, histname.str().c_str(), qdc_chs_to_draw[i], branch_qdc, 100, 0, 3500);
    }	
    
    
    // Find out if we want to plot an adc channel
    hist_branch_channel* adc_ch_hist[n_adcs_to_draw];
    for (int i = 0; i < n_adcs_to_draw; i++) {
    	if (adc_chs_to_draw[i] < phadc_ch_Ge0 || adc_chs_to_draw[i] > phadc_ch_Ge1) {
    		std::cout << "Invalid adc channel number " << adc_chs_to_draw[i] << std::endl;
    		adc_ch_hist[i] = NULL;
    	}
    	else if (adc_chs_to_draw[i] == phadc_ch_Ge0) {
    		adc_ch_hist[i] = new hist_branch_channel(out_file, "Ge1.ADC", 0, branch_adc0, 100, 0, 3000);
    	}
    	else if (adc_chs_to_draw[i] == phadc_ch_Ge1) {
    		adc_ch_hist[i] = new hist_branch_channel(out_file, "Ge2.ADC", 0, branch_adc1, 100, 0, 3000);
    	}
    }
    
    
    // Find out if we want to plot a tdc channel
    hist_branch_channel* tdc_ch_hist[n_tdcs_to_draw];
    for (int i = 0; i < n_tdcs_to_draw; i++) {
    	if (tdc_chs_to_draw[i] < tdc_ch_t0 || tdc_chs_to_draw[i] > tdc_ch_Ge1) {
    		std::cout << "Invalid tdc channel number " << tdc_chs_to_draw[i] << std::endl;
    		tdc_ch_hist[i] = NULL;
    	}
    	else if (tdc_chs_to_draw[i] == tdc_ch_t0) {
    		tdc_ch_hist[i] = new hist_branch_channel(out_file, "T0.TDC", 0, branch_tdc0, 100, 0, 3000);
    	}
    	else if (tdc_chs_to_draw[i] > tdc_ch_t0) {
    		std::stringstream histname;
    		histname << "X" << tdc_chs_to_draw[i] << ".TDC";
    		tdc_ch_hist[i] = new hist_branch_channel(out_file, histname.str().c_str(), 0, branch_tdc0 + tdc_chs_to_draw[i], 100, 0, 3000);
    	}
    }
    
        
    // Create the converter algorithms to use
    tfile_converter_algorithm* converter = new tfile_converter_algorithm(out_file);
    
    // Add algorithms to the midus_file
    in_file->add_algorithm(converter);
    for (int i = 0; i < n_qdcs_to_draw; i++) {
    	if (qdc_ch_hist[i] != NULL)
    		in_file->add_algorithm(qdc_ch_hist[i]);
    }
    for (int i = 0; i < n_adcs_to_draw; i++) {
    	if (adc_ch_hist[i] != NULL)
       		in_file->add_algorithm(adc_ch_hist[i]);
    }
   for (int i = 0; i < n_tdcs_to_draw; i++) {
    	if (tdc_ch_hist[i] != NULL)
	    	in_file->add_algorithm(tdc_ch_hist[i]);
    }
    
    // Loop through the file
    in_file->loop();
    
    // Write and close the output file
    out_file->close();
    
    return 0;
}

