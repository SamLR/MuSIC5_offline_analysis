//
//  algorithm.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
//  Algorithm implements the 'visitor' part of the visitor
//  pattern with the entry class

#ifndef MuSIC5_offline_analysis_algorithm_h
#define MuSIC5_offline_analysis_algorithm_h

class line_entry;
class midus_entry;

class algorithm {
public:
    algorithm(){;};
    virtual ~algorithm() {;};
    
    // There needs to be a pure virtual process
    // for each type of entry that will be passed 
    // in that will specify the specific behaviour
    virtual void process(line_entry const *) = 0;
    virtual void process(midus_entry const *) = 0;
};

#endif
