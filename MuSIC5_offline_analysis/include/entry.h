//
//  entry.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
//  An empty abstract base class to represent entries in input files

#ifndef MuSIC5_offline_analysis_entry_h
#define MuSIC5_offline_analysis_entry_h

class input_file;
class algorithm;

class entry {
public:
    entry(){;} ;
    virtual ~entry();
    virtual void accept(algorithm const&) const = 0;
};


#endif
