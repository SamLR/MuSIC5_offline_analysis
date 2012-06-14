//
//  input_root.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>

#include "input_root.h"
#include "TTree.h"

input_root::input_root(TString const& filename, TString const& treename, ):
TFile(filename, "READ"), tree_m(0), n_next_entry_m(0), n_entries_m(0){
    init(treename);
}

void input_root::init(TString const& treename){
    tree_m = (TTree*) this->Get(treename);
    
}