//
//  conversion_branch_structure.h
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

namespace midus_structure {
    
    static int const n_tdc_channels = 16;
    static int const n_qdc_channels = 13;
    static int const n_adc_channels = 2;
    // number of branches is n_channels + 3 (ADC, PHADC & T0)
    static int const n_branches_in_midus_entry = n_tdc_channels + 3;
    static int const n_branches_in_trigger_tree = 5;
    // max_data_entries is a wholly arbitary number
    static int const max_data_entries = 500;
    static int const n_scaler_ch = 8;
    
    // layout of data in a midus root tree
    // and in a midus entry
    struct midus_out_branch {
        int n_entries;
        int data[max_data_entries];
    };
    
    // layout of data as saved in a converted tree
    struct channel {
        int adc;
        int tdc0;
        int n_tdc_hits;
        int tdc[max_data_entries];
    };
    
    // the layout of branches in a midus_entry
    enum midus_entry_branch_id {
        branch_qdc  = 0,
        branch_adc0 = 1,
        branch_adc1 = 2,
        branch_tdc0 = 3,
        // other tdc numbers are just additions to tdc0
    };
    
    
    enum qdc_ch_names {
        qdc_ch_U1 = 0 ,
        qdc_ch_U2 = 1 ,
        qdc_ch_U3 = 2 ,
        qdc_ch_U4 = 3 ,
        qdc_ch_U5 = 4 ,
        qdc_ch_U6 = 5 ,
        qdc_ch_U7 = 6 ,
        qdc_ch_U8 = 7 ,
        qdc_ch_D1 = 8 ,
        qdc_ch_D2 = 9 ,
        qdc_ch_D3 = 10,
        qdc_ch_D4 = 11,
        qdc_ch_D5 = 12
    };
    
    enum phadc_ch_names {
        phadc_ch_Ge0  = 0,
        phadc_ch_Ge1  = 1,
        phadc_ch_CdTe = 2
    };
    
    enum tdc_ch_names {
        tdc_ch_t0  = 0,
        tdc_ch_U0  = 1 ,
        tdc_ch_U1  = 2 ,
        tdc_ch_U2  = 3 ,
        tdc_ch_U3  = 4 ,
        tdc_ch_U4  = 5 ,
        tdc_ch_U5  = 6 ,
        tdc_ch_U6  = 7 ,
        tdc_ch_U7  = 8 ,
        tdc_ch_D0  = 9 ,
        tdc_ch_D1  = 10,
        tdc_ch_D2  = 11,
        tdc_ch_D3  = 12,
        tdc_ch_D4  = 13,
        tdc_ch_Ge0 = 14,
        tdc_ch_Ge1 = 15
    };
    
    enum scaler_ch_names {
        scaler_ch_sec    = 0,
        scaler_ch_trig   = 1,
        scaler_ch_gdTrig = 2,
        scaler_ch_U      = 3,
        scaler_ch_D      = 4,
        scaler_ch_scint  = 5,
        scaler_ch_na     = 6,
        scaler_ch_clk    = 7
    };
};
#endif