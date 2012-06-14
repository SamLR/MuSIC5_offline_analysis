//
//  dumb_entry.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_dumb_entry_h
#define MuSIC5_offline_analysis_dumb_entry_h

#include "../../include/ttree_entry.h"

class TTree;

class dumb_entry : public ttree_entry {
public:
    dumb_entry() {;};
    ~dumb_entry();
    void set_branch_addresses(TTree*) const;
    
private:
    int data_m;
};

#endif
