//
//  input_root.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
// Designed to read in a root file for use with visitor class


#include <iostream>

// from ROOT
#include "TTree.h"

#include "input_root.h"
#include "ttree_entry.h"


input_root::input_root(TString const& filename, TString const& treename,  ttree_entry const* entry):
TFile(filename, "READ"), tree_m(0), n_next_entry_m(0), n_entries_m(0), entry_m(entry){
    init(treename);
}

void input_root::init(TString const& treename){
    tree_m = (TTree*) this->Get(treename);
    entry_m->set_branch_addresses(tree_m);
    n_entries_m = tree_m->GetEntries();
}

ttree_entry const& input_root::next_entry() const{
    if (n_next_entry_m >= n_entries_m) {
        // warning/error here?
        std::cerr<<"WARNING: out of entries, looping"<< endl;
        n_next_entry_m=0;
        tree_m->GetEntry(n_next_entry_m);
        return entry_m;
    } else {
        tree_m->GetEntryNumberWithIndex(n_next_entry_m);
        ++n_next_entry_m;
        return entry_m;
    }
}
