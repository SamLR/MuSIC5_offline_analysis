//
//  midus_tree_structs.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 15/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
//
// This struct gives the general layout of data for a piece 
// of equipment (e.g. ADC, TDC) in a midus root file
// 

#ifndef MuSIC5_offline_analysis_midus_tree_structs_h
#define MuSIC5_offline_analysis_midus_tree_structs_h

static int const n_channels = 2;
static int const n_branches_in_trigger_tree = 4;
static int const max_data_entries = 500;

struct midus_out_branch {
    int n_entries;
    int data[max_data_entries];
};

struct channel {
	int adc;
	int tdc0;
	int tdc[max_data_entries];
};

#endif
