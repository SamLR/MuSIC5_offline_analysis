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

#include <string>

namespace midus_structure {
    
    
    //
    // General data flow:
    // Midus root file -> Midus entry -> algorithm
    //
    // The midus root file contains two trees (apparently grouped
    // by when they're read). For MuSIC these are: "Trigger" and
    // "Scaler"; representing the read out due to trigger events
    // and the periodic read out of the scaler respectively. 
    // 
    // The two trees contain a number of branches corresponding
    // to the equipment that is read out at that time. This means
    // that the Trigger has 5 branches (TDC, QDC, ADC0, ADC1 
    // and ERR) whilst the Scaler has 1 (SCLR). NOTE: the branches
    // ADC0 and ADC1 represent channels not individual ADCs whilst
    // ERR is error data from the VME crate rather than a module.
    //
    // The data in all of these branches is stored in the same
    // format (the number of channels/hits and then an array). 
    // 
    // The data from the TDC & QDC is serialised so that the
    // channels are not linear; the TDC also has a number
    // of hits per channel so is split into separate branches
    // in the midus entry (one per channel).
    //
    
    // some helper functions for matching names 
    // to branch/channel numbers and visa-versa
    int const get_branch_number(std::string const);
    int const get_channel_number(std::string const);
    
    std::string const get_branch_name(const int);
    std::string const get_channel_name(const int);;
    
    // Some basic values 
    int const n_tdc_channels = 16;
    int const n_qdc_channels = 13;
    int const n_adc_channels = 2;
    // The TDC branch is split up so that each channel
    // has its own branch. This is in addition to the
    // QDC & 2 ADC branches
    int const n_branches_in_midus_entry = n_tdc_channels + 2 + 1;
    // initial number of branches in the midus root file
    int const n_branches_in_trigger_tree = 5;
    // max_data_entries is a wholly arbitary number
    int const max_data_entries = 500;
    int const n_scaler_ch = 8;
    
    std::string const branch_names[n_branches_in_midus_entry] = {
        "QDC",     "ADC1",   "ADC2",   "TDC_t0", 
        "TDC_U1",  "TDC_U2", "TDC_U3", "TDC_U4",
        "TDC_U5",  "TDC_U6", "TDC_U7", "TDC_U8",
        "TDC_D1",  "TDC_D2", "TDC_D3", "TDC_D4", "TDC_D5",
        "TDC_Ge1", "TDC_Ge2"
    };
    
    std::string const tdc_names[n_qdc_channels] = {
        "t0",
        "U1",  "U2", "U3", "U4", "U5",  "U6", "U7", "U8",
        "D1",  "D2", "D3", "D4", "D5",
        "Ge1", "Ge2"
    };
    
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
    enum midus_entry_branch {
        eMEB_qdc  = 0,
        eMEB_adc0 = 1,
        eMEB_adc1 = 2,
        eMEB_tdc0 = 3,
        eMEB_U1   = 4,
        eMEB_U2   = 5,
        eMEB_U3   = 6,
        eMEB_U4   = 7,
        eMEB_U5   = 8,
        eMEB_U6   = 9,
        eMEB_U7   = 10,
        eMEB_U8   = 11,
        eMEB_D1   = 12,
        eMEB_D2   = 13,
        eMEB_D3   = 14,
        eMEB_D4   = 15,
        eMEB_D5   = 16,
        eMEB_Ge1  = 17,
        eMEB_Ge2  = 18
    };
    
    // qdc array entries as stored in the QDC branch
    enum qdc_ch {
        eQDC_U1 = 0 ,
        eQDC_U2 = 1 ,
        eQDC_U3 = 2 ,
        eQDC_U4 = 3 ,
        eQDC_U5 = 4 ,
        eQDC_U6 = 5 ,
        eQDC_U7 = 6 ,
        eQDC_U8 = 7 ,
        eQDC_D1 = 8 ,
        eQDC_D2 = 9 ,
        eQDC_D3 = 10,
        eQDC_D4 = 11,
        eQDC_D5 = 12
    };
    // tdc channels as stored in the TDC branch
    enum tdc_ch {
        eTDC_0  = 0 ,
        eTDC_1  = 1 ,
        eTDC_2  = 2 ,
        eTDC_3  = 3 ,
        eTDC_4  = 4 ,
        eTDC_5  = 5 ,
        eTDC_6  = 6 ,
        eTDC_7  = 7 ,
        eTDC_8  = 8 ,
        eTDC_9  = 9 ,
        eTDC_10 = 10,
        eTDC_11 = 11,
        eTDC_12 = 12,
        eTDC_13 = 13,
        eTDC_14 = 14,
        eTDC_15 = 15
    };
    
    // scaler channels as stored in the SCLR branch of the scaler tree
    enum scaler_ch_names {
        eSCLR_sec    = 0,
        eSCLR_trig   = 1,
        eSCLR_gdTrig = 2,
        eSCLR_U      = 3,
        eSCLR_D      = 4,
        eSCLR_scint  = 5,
        eSCLR_na     = 6,
        eSCLR_clk    = 7
    };
};
#endif
