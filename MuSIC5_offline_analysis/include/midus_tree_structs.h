//
//  midus_tree_structs.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 15/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#ifndef MuSIC5_offline_analysis_midus_tree_structs_h
#define MuSIC5_offline_analysis_midus_tree_structs_h

struct TDC_branch {
    TDC_branch(int const n_hits, int const n_ch): n_hits_m(n_hits), n_ch_m(n_ch) {;} ;
    
    int const n_hits_m;
    int const n_ch_m;
    
    int entry_id_m;
    int value_m [n_hits_m][n_ch_m];
};

struct QDC_branch {
    QDC_branch(int const n_ch) : n_ch_m(n_ch) {;} ;
    
    int const n_ch_m;
    
    int entry_id_m;
    int value_m[n_ch_m];
};

#endif
