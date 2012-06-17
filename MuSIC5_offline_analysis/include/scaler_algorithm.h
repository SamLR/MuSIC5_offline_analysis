//
//  scaler_algorithm.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 17/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
// visitor class for scaler trees
//

#ifndef MuSIC5_offline_analysis_scaler_algorithm_h
#define MuSIC5_offline_analysis_scaler_algorithm_h

#include "scaler_entry.h"
class scaler_entry;

class scaler_algorithm {
public:
    scaler_algorithm(){;} ;
    virtual ~scaler_algorithm(){;} ;
    
    virtual void process(scaler_entry const* ) = 0;
};

#endif
