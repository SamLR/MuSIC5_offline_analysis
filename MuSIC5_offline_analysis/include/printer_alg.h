//
//  printer_alg.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
// a (very) simple algorithm that should print the contents of what ever it's 
// passed
// Useful for debugging

#ifndef MuSIC5_offline_analysis_printer_alg_h
#define MuSIC5_offline_analysis_printer_alg_h

#include "algorithm.h"

class line;
class midus_entry;

class printer_alg : public algorithm {
public:
    printer_alg() {;} ;
    ~printer_alg() {;} ;
    
    void process(line_entry const *);
    void process(midus_entry const *);
};

#endif
