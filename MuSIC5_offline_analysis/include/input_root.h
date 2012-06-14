//
//  input_root.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_input_root_h
#define MuSIC5_offline_analysis_input_root_h

// from ROOT
#include "TFile.h"
#include "TString.h"

// Super class
#include "input_file.h"

class ttree_entry;
class TTree;

class input_root: public input_file, TFile {    
public:
    explicit input_root(TString const&,TString const&, ttree_entry const *const); 
    ~input_root();
    void open();
    void close();
    void write();
    ttree_entry const *const next_entry();
    int const get_entries() const {return n_entries_m;};
    
private:
    void init(TString const&);
    TTree * tree_m;
    ttree_entry const *const entry_m;
    int n_next_entry_m;
    int n_entries_m;
};

#endif
