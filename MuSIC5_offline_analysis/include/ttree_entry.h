//
//  ttree_entry.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_ttree_entry_h
#define MuSIC5_offline_analysis_ttree_entry_h

#include "entry.h"

class TTree;

class ttree_entry: public entry{
public:
    void set_branch_addresses(TTree const*);
};

#endif
