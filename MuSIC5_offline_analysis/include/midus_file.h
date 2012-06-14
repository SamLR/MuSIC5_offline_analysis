//
//  midus_file.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_midus_file_h
#define MuSIC5_offline_analysis_midus_file_h

#include <string>

class midus_file: public input_file{
    string filename;
    
public:
    midus_file(string filename);
    ~midus_file();
    
};

#endif
