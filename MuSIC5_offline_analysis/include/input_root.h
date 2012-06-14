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
// include ttree_entry here as input_root needs to know that it is
// covarient with entry (i.e. it inherits from it)
#include "ttree_entry.h"

class TTree;

class input_root: public input_file, TFile {    
public:
    explicit input_root(TString const&,TString const&, ttree_entry const *const); 
    ~input_root();
    void open();
    void close();
    void write();
    ttree_entry const *const next_entry() const;
    bool const has_next() const;
    int const get_entries() const {return n_entries_m;};
    
private:
    void init(TString const&);
    
    // member variables
    TTree * tree_m;
    ttree_entry const *const entry_m;
    TString const filename_m;
    mutable int n_next_entry_m;
    mutable int n_entries_m;
};

inline bool const input_root::has_next() const{
    return (n_next_entry_m < n_entries_m);
}

#endif
