//
//  entry.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
//  An empty abstract base class to represent entries in input files
//  Entry is the 'element/node/visted' class of the visitor pattern
//

#ifndef MuSIC5_offline_analysis_entry_h
#define MuSIC5_offline_analysis_entry_h

class input_file;
class algorithm;

class entry {
public:
    entry(){;};
    virtual ~entry(){;};
    // Accept is the function that should be called to
    // implement the visitor class.
    // It should be a call to the algorithm's 'process' function
    // passing 'this' as an argument
    virtual void accept(algorithm *const) const = 0;
    
};


#endif
