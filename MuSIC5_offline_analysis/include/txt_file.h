//
//  txt_file.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_txt_file_h
#define MuSIC5_offline_analysis_txt_file_h

#include "input_file.h"


#include <iostream>
#include <fstream>

using namespace std;

class txt_file: public input_file {
public:
    txt_file();
    txt_file(string const*);
    ~txt_file();
    
    void loop();
private:
    ifstream ifstream_m;
};


#endif
