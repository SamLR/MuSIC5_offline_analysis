//
//  root_test_file_gen.C
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

// This is a root macro for generating a basic tfile with
// simple ttree inside of it

{ 
    // example of macro to read data from an ascii file and 
    // create a root file with an histogram and a TTree 
    gROOT->Reset(); 
    // the structure to hold the variables for the branch 
    
    struct in_branch { 
        Int_t n_hits;
        Int_t dat[500];
    }; 
    // n_branches, 1 for ADC values, 1 for T0 (TDC0) and then 2 other TDC channels
    int n_branches = 4;
    in_branch branches[4]; 
    // create a new ROOT file 
    TFile *f = new TFile("midus_test_in.root","RECREATE"); 
    // create a TTree 
    TTree *tree = new TTree("Trigger","mmmm data!"); 
    // create one branch with all information from the stucture 
    tree->Branch("ADC",&(branches[0]),"n_ch/I:data[n_ch]"); 
    tree->Branch("TDC0",&(branches[1]),"n_hitsT0/I:data[n_hitsT0]"); 
    tree->Branch("TDC1",&(branches[2]),"n_hitsT1/I:data[n_hitsT1]"); 
    tree->Branch("TDC2",&(branches[3]),"n_hitsT2/I:data[n_hitsT2]"); 
    
    int n_events = 10;
    
    for(unsigned int event = 0; event < n_events; ++event) {
         // number of enteries/branch: static for ADC & T0 measuments (2 & 1 
         // respectively) but mutable for TDC hits
        int n_enteries [4] = {2, 1, 5%(event+1), 13%(event+1)};
        for(unsigned int b = 0; b < n_branches; ++b) {
            branches[b].n_hits=n_enteries[b];
            for(unsigned int i = 0; i < n_enteries[b]; ++i) {
                branches[b].dat[i] = i+b;
            }
        }
        tree->Fill();
    }
    
    tree->Print(); 
    f->Write();
}