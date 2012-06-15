//
//  midus_tree_structs.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 15/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_midus_tree_structs_h
#define MuSIC5_offline_analysis_midus_tree_structs_h

#define MAX_TDC_HITS 500
#define TDC_CH 4
#define QDC_CH 4

struct TDC_branch {
    
    int n_hits_m;
    int n_ch_m;
    
    int entry_id_m;
    int value_m [MAX_TDC_HITS][TDC_CH];
};

struct QDC_branch {
    
    int n_ch_m;
    int entry_id_m;
    
    int value_m[QDC_CH];
};

#endif
