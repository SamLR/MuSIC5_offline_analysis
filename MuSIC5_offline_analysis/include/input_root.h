//
//  input_root.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_input_root_h
#define MuSIC5_offline_analysis_input_root_h

#include "input_file.h"
#include "TFile.h"
#include "TString.h"

class entry;
class TTree;

class input_root: public input_file, TFile {    
public:
    explicit input_root(TString const&); 
    ~input_root();
    void open();
    void close();
    void write();
    entry const & next_entry() const;
    int const & get_entries() const {return n_entries_m;};
    
private:
    TTree const* tree_m;
    int n_next_entry_m;
    int n_entries_m;
};

#endif
