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

int main(int argc, const char * argv[])
{
	// Command line args - string filename to process
	//					 - optional output file name (xxxx_converted.root)
	//					 - optional flags to control display of ADC (e.g. -ADC and next number is which ADC to plot)
	
	if (argc < 2) {
		std::cout << "Incorrect number of arguments" << std::endl;
		std::cout << "Usage: ./mid2root_converter input_filename (optional: output_filename)" << std::endl;
		exit(1);
	}
	
    // Create the input file object
    midus_file* in_file = new midus_file(argv[1]);
    
    // Create the output file object
    std::stringstream out_filename;
    if (argc > 2) {
    	out_filename << argv[2];
    }
    else {
    	std::string temp = argv[1];
    	std::string temp_2;
    	std::stringstream temp_in_file;
    	
    	temp_in_file << temp;
    	std::getline(temp_in_file, temp_2, '.');
    	out_filename << temp_2;
    	out_filename << "_converted.root";
    }
    smart_tfile* out_file = smart_tfile::getTFile(out_filename.str(), "RECREATE");
    
    // Create the algorithms to use
    tfile_converter_algorithm* converter = new tfile_converter_algorithm(out_file);
    
    // Add algorithms to the midus_file
    in_file->add_algorithm(converter);
    
    // Loop through the file
    in_file->loop();
    
    // Write and close the output file
    out_file->close();
    
    return 0;
}

