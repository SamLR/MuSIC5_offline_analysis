//
//  input_file.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
// This is an abstract base class for input files
// that is designed to give access to each entry
// within some structure(s)
// 


#ifndef MuSIC5_offline_analysis_input_file_h
#define MuSIC5_offline_analysis_input_file_h

class entry;

class input_file {
public:
    input_file();
    virtual ~input_file();
    virtual void open() = 0;
    virtual void close() = 0;
    virtual bool has_next() = 0;
    virtual entry const *const next_entry() = 0;
    
private: 
    // disable assignment and copy constructors
    input_file& operator= (input_file const &);
    input_file(input_file const&);
};

#endif
