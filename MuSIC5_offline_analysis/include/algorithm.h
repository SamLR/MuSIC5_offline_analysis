//
//  algorithm.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
// This is the base class for algorithm
// 

#ifndef MuSIC5_offline_analysis_algorithm_h
#define MuSIC5_offline_analysis_algorithm_h

class entry;

class algorithm {
public:
    algorithm() {;};
    virtual ~algorithm() {;};
    virtual void process(entry const*) = 0;   
};


#endif
