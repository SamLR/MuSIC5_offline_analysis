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
#define QDC_CH 16


struct trigger_branch {
    int n_tdc;
    int tdc0[MAX_TDC_HITS];
    int n_qdc;
    int qdc0[QDC_CH];
};

#endif
