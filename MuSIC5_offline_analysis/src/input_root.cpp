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

// declaration
#include "input_root.h"

// initialise everything
input_root::input_root(TString const& filename, TString const& treename,  
                       ttree_entry const *const entry):
tree_m(0), entry_m(entry), filename_m(filename),
n_next_entry_m(0), n_entries_m(0) {
    init(treename);
}

input_root::~input_root(){
    delete tree_m;
}

void input_root::init(TString const& treename) {
    tree_m = (TTree*) this->Get(treename);
    entry_m->set_branch_addresses(tree_m);
    n_entries_m = tree_m->GetEntries();
}

ttree_entry const *const input_root::next_entry() const {
    if (n_next_entry_m >= n_entries_m) {
        // warning/error here?
        std::cerr<<"WARNING: out of entries, looping"<< std::endl;
        n_next_entry_m = 0;
        tree_m->GetEntry(n_next_entry_m);
        return entry_m;
    } else {
        tree_m->GetEntryNumberWithIndex(n_next_entry_m);
        ++n_next_entry_m;
        return entry_m;
    }
}

void input_root::open(){
    if (!this->IsOpen()) {
        this->Open(filename_m);
    }
}

void input_root::close(){
    this->Close();
}

void input_root::write(){
    this->Write();
}