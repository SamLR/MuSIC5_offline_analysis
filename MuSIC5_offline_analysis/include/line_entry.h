//
//  line_entry.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
//  A class that represents a single line of text in a file
//  Not really useful other than for testing

#ifndef MuSIC5_offline_analysis_line_entry_h
#define MuSIC5_offline_analysis_line_entry_h

#include "entry.h"

class string;
class algorithm;

class line_entry: public entry {
public:
    line_entry();
    line_entry(std::string const&);
    ~line_entry();
    void accept(algorithm *const) const;
    std::string const get_line() const;
    
private:
    std::string const line_m;
};

inline std::string const line_entry::get_line() const {return line_m;}

#endif
