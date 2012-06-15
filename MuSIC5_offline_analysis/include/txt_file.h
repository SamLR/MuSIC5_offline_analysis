//
//  txt_file.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
//  A subclass of the input_file for dealing with text files.
//  at each loop it creates a line_entry to be passed to the algorithm
//  This is mainly for debugging

#ifndef MuSIC5_offline_analysis_txt_file_h
#define MuSIC5_offline_analysis_txt_file_h

#include "input_file.h"

#include <iostream>
#include <fstream>
#include <string>

class txt_file: public input_file {
public:
    // initialise with the file to be read in
    txt_file(std::string const & filename);
    ~txt_file();
    
    // the concrete implementation of the loop function
    // all it does is read each line individually
    void loop();
private:
    // this constructor shouldn't be used
    txt_file(){;} ;
    std::ifstream ifstream_m;
};


#endif
