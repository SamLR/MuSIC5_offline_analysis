//
//  algorithm.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_algorithm_h
#define MuSIC5_offline_analysis_algorithm_h

class line;
class midus_entry;

class algorithm {
public:
    algorithm();
    virtual ~algorithm();
    virtual void process(line const &) = 0;
    virtual void process(midus_entry const &) = 0;
};

#endif
