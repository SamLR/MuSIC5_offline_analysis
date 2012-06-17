//
//  scaler_printer.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 17/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_scaler_printer_h
#define MuSIC5_offline_analysis_scaler_printer_h

#include "scaler_algorithm.h"

class scaler_entry;

class scaler_printer: public scaler_algorithm {
public:
    scaler_printer(){;} ;
    ~scaler_printer(){;} ;
    
    void process(scaler_entry const*);
};


#endif
