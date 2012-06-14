//
//  line_entry.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_line_entry_h
#define MuSIC5_offline_analysis_line_entry_h

class string;
class algorithm;

class line_entry: public entry {
public:
    line_entry();
    line_entry(string const*);
    ~line_entry();
    void accept(algorithm const&) const;
    string const * get_line() const;
    
private:
    string const* line_m;
};


#endif
