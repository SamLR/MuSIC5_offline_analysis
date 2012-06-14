//
//  dumb_entry.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include "dumb_entry.h"
#include "TTree.h"

void dumb_entry::set_branch_addresses(TTree* tree) const {
    tree->SetBranchAddress("numbers", &data_m);   
}

dumb_entry::~dumb_entry(){ ; }