//
//  txt_file.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include <cstdlib>
#include <string>

#include "txt_file.h"
#include "line_entry.h"


// Constructor
// initialse and open the file, exit if the file failed to open
txt_file::txt_file(std::string const& filename) {
    ifstream_m.open(filename.c_str());
    if (!ifstream_m.is_open()) {
        cerr << "Error opening file! Exiting"<< endl;
        exit(1);
    }
}

// tidy up
txt_file::~txt_file(){
    ifstream_m.close();
}

// the required loop function
void txt_file::loop(){
    // call the default implementation first
    // currently just checks that there are 
    // registered algorithms
    input_file::loop();
    // check the file is actually open
    if (ifstream_m.is_open()) {
        // for all lines of the file
        while (ifstream_m.good()) {
            // read in
            std::string line;
            getline(ifstream_m, line);
            line_entry entry(line);
            // now loop over all the registered algorithms
            for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
                entry.accept(get_algorithm(alg));
            }
        }
    } else {
        cerr << "file not open" << endl;
    }   
}
