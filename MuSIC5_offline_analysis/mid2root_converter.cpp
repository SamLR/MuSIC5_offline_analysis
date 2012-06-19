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
#include "printer_alg.h"

#include "TApplication.h"
#include "TCanvas.h"

void HelpMessage();

int main(int argc, 	char * argv[])
{
	// The command line arguments
	std::string input_filename;
	std::string output_filename;
	
	std::string long_arg;
	std::string channel;
	int max_qdc_hists = midus_structure::n_qdc_channels;
	int qdc_chs_to_draw[max_qdc_hists];
	int n_qdcs_to_draw = 0; // 0 to 12
	int max_adc_hists = midus_structure::n_adc_channels;
	int adc_chs_to_draw[max_adc_hists]; 
	int n_adcs_to_draw = 0; // 0 to 1 (Ge0, Ge1)
	int max_tdc_hists = midus_structure::n_tdc_channels;
	int tdc_chs_to_draw[max_tdc_hists]; 
	int n_tdcs_to_draw = 0; // 0 to 15 (t0, U0...U7, D0...D4, Ge0, Ge1)
	
	bool display_hists = false;
	int n_entries_to_process = 0;
	
	if (argc < 2) {
		HelpMessage();
		exit(1);
	}
	
	int c;
	while ((c = getopt(argc, argv, "hi:o:q:g:t:dan:")) != -1) {
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
			
		case 'g':
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
			long_arg = optarg;
			for (int i = 0; i <= long_arg.size(); i++) {
				if (i == long_arg.size() || long_arg[i] == ' ') {
					// later will convert from string
					tdc_chs_to_draw[n_tdcs_to_draw] = atoi(channel.c_str());
					n_tdcs_to_draw++;
					channel.clear();
				}
				else {
					channel.push_back(long_arg[i]);
				}
			}
			break;
		
		case 'd':
			display_hists = true;
			break;
		
		case 'a':
			for (int i = 0; i < max_qdc_hists; i++) {
				qdc_chs_to_draw[i] = i+1;
			}
			n_qdcs_to_draw = max_qdc_hists;
			for (int i = 0; i < max_adc_hists; i++) {
				adc_chs_to_draw[i] = i;
			}
			n_adcs_to_draw = max_adc_hists;
			for (int i = 0; i < max_tdc_hists; i++) {
				tdc_chs_to_draw[i] = i;
			}
			n_tdcs_to_draw = max_tdc_hists;
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
    	output_filename += "_converted.root";
    }
    smart_tfile* out_file = smart_tfile::getTFile(output_filename, "RECREATE");
    
    
    // Find out if we want to plot a qdc channel
    hist_branch_channel* qdc_ch_hist[n_qdcs_to_draw];
    for (int i = 0; i < n_qdcs_to_draw; i++) {
   		if (qdc_chs_to_draw[i] < midus_structure::eQDC_U1 || qdc_chs_to_draw[i] > midus_structure::eQDC_D5) {
   			std::cout << "Invalid qdc channel number " << qdc_chs_to_draw[i] << std::endl;
    		qdc_ch_hist[i] = NULL;
    		continue;
   		}
   		std::stringstream histname;
 		histname << midus_structure::get_channel_name(qdc_chs_to_draw[i]) << ".ADC";
   		qdc_ch_hist[i] = new hist_branch_channel(out_file, histname.str().c_str(), qdc_chs_to_draw[i], midus_structure::eMEB_qdc, 100, 0, 3500);
    }	
    
    
    // Find out if we want to plot an adc channel
    hist_branch_channel* adc_ch_hist[n_adcs_to_draw];
    for (int i = 0; i < n_adcs_to_draw; i++) {
    	if (adc_chs_to_draw[i] == 0) {
    		adc_ch_hist[i] = new hist_branch_channel(out_file, "Ge1.ADC", 0, midus_structure::eMEB_adc0, 100, 0, 3000);
    	}
    	else if (adc_chs_to_draw[i] == 1) {
    		adc_ch_hist[i] = new hist_branch_channel(out_file, "Ge2.ADC", 0, midus_structure::eMEB_adc1, 100, 0, 3000);
    	}
    	else {
    		std::cout << "Invalid adc channel number " << adc_chs_to_draw[i] << std::endl;
    		adc_ch_hist[i] = NULL;
    		continue;
    	}
    }
    
    
    // Find out if we want to plot a tdc channel
    hist_branch_channel* tdc_ch_hist[n_tdcs_to_draw];
    for (int i = 0; i < n_tdcs_to_draw; i++) {
    	if (tdc_chs_to_draw[i] < midus_structure::eTDC_0 || tdc_chs_to_draw[i] > midus_structure::eTDC_15) {
    		std::cout << "Invalid tdc channel number " << tdc_chs_to_draw[i] << std::endl;
    		tdc_ch_hist[i] = NULL;
    		continue;
    	}
    	else if (tdc_chs_to_draw[i] == midus_structure::eTDC_0) {
    		tdc_ch_hist[i] = new hist_branch_channel(out_file, "T0.TDC", 0, midus_structure::eMEB_tdc0, 100, 0, 500000);
    	}
    	else if (tdc_chs_to_draw[i] > midus_structure::eTDC_0) {
    		std::stringstream histname;
    		histname << midus_structure::get_channel_name(tdc_chs_to_draw[i]) << ".TDC";
    		tdc_ch_hist[i] = new hist_branch_channel(out_file, histname.str().c_str(), 0, tdc_chs_to_draw[i], 100, 0, 500000);
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
    
    //printer_alg* printer = new printer_alg();
    //in_file->add_algorithm(printer);
    
    // Loop through the file
    if (n_entries_to_process != 0) {
    	in_file->loop(n_entries_to_process);
    }
    else {
    	in_file->loop();
    }
    
    // Display the histograms if that's what has been asked for	
    if (display_hists == true) {
    	TApplication theApp("App", &argc, argv);
		TCanvas *c = new TCanvas("c", "c");
    	for (int i = 0; i < n_qdcs_to_draw; i++) {
    		if (qdc_ch_hist[i] != NULL) {
	  			qdc_ch_hist[i]->draw_hist();
   				c->Update();
   				getchar();
   			}
   		}
   		for (int i = 0; i < n_adcs_to_draw; i++) {
   			if (adc_ch_hist[i] != NULL) {
	  			adc_ch_hist[i]->draw_hist();
   				c->Update();
   				getchar();
   			}
   		}
   		for (int i = 0; i < n_tdcs_to_draw; i++) {
   			if (tdc_ch_hist[i] != NULL) {
	  			tdc_ch_hist[i]->draw_hist();
   				c->Update();
   				getchar();
   			}
   		}
   	}
    // Write and close the output file
    out_file->close();
    
    return 0;
}

void HelpMessage() {
	std::cout << "The mid2root_converter converts from a MIDAS ROOT input file to another ROOT file with a different tree structure\n";
	std::cout << "It can also add histograms of specific channels to the root file\n\n";
	std::cout << "Command line arguments: " << std::endl;
	std::cout << "\t -h  --  prints this help message\n";
	std::cout << "\t -i  --  filename of the input MIDAS ROOT file to convert (e.g. -i example.root)\n";
	std::cout << "\t -o  --  filename of the output ROOT file\n\t\t (if not given then the output file is called example_converted.root in the same directory as the input file)\n\n";
	std::cout << "The following commands take an integer or a series of integers separated by spaces and enclosed within \" \"\n";
	std::cout << "\t -q  --  channel numbers of the channels whose ADC values you want to plot\n\t\t (where 0 = U1, 1 = U2, ..., 7 = U8, 8 = D1, ..., 12 = D5)\n\t\t Example: -q \"1 10\" creates histograms of U2.ADC and D3,ADC\n";
	std::cout << "\t -g  --  channel numbers of the Ge channels whose ADC values you want to plot\n\t\t (where 0 = Ge0, 1 = Ge1)\n\t\t Example -a 0 creates a histogram of Ge0.ADC\n";
	std::cout << "\t -t  --  channel numbers of the channels whose TDC values you want to plot\n\t\t (where 0 = TDC0, 1 = U0, ..., 8 = U7, 9 = D0, ..., 13 = D4, 14 = Ge0, 15 = Ge1)\n\t\t Example -t \"12 0 4\" creates histograms of D3.TDC, TDC0 and U3.TDC\n\n";
	std::cout << "Other useful commands:\n";
	std::cout << "\t -d  --  displays all the histograms that are generated. Go through them by pressing enter on the command line\n";
	std::cout << "\t -a  --  create histograms for all ADC and TDC channels\n\t\t (don't use in conjunction with -q, -g or -t)\n";
	std::cout << "\t -n  --  the number of entries in the input file to process\n";
}

