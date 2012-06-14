//
//  txt_file.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>

#include "txt_file.h"
#include "line_entry.h"

txt_file::txt_file(){;}

txt_file::txt_file(string const* filename):ifstream_m(filename, ifstream::in) {;}

txt_file::~txt_file(){
    ifstream_m.close();
}

void txt_file::loop(){
    while (ifstream_m.good()) {
        for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
            line_entry l(ifstream_m.get());
            l.accept(get_algorithm(alg));
        }
    }
}