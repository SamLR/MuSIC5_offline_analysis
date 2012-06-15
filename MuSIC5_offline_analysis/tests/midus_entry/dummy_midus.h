//
//  dummy_midus.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 15/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_dummy_midus_h
#define MuSIC5_offline_analysis_dummy_midus_h

#include "../../include/input_file.h"

class dummy_midus: public input_file {
public:
    dummy_midus(int n): n_loops_m(n) {;};
    ~dummy_midus() {;};
    void loop();
    
private:
    dummy_midus();
    int n_loops_m;

};


#endif
