// midus_file.cpp
// -- Implements the midus_file methods
// Created: 15/06/2012 Andrew Edmonds

#include <cstdlib>

#include "midus_file.h"
#include "midus_entry.h"
#include "midus_tree_structs.h"
#include "TFile.h"
#include "TTree.h"


midus_file::midus_file(std::string const& filename)
: TFile(filename.c_str(), "READ"), filename_m(filename), 
trigger_tree_m(0), scaler_tree_m(0), t_branch_m(), 
n_qdc_channels_m(0), n_tdc_hits_m(0), n_entries(0) {
    init();
}

midus_file::~midus_file() {
	this->Close();
}

void midus_file::loop() {
	// Call default loop method
	input_file::loop();          
	
    for (int entry_number = 0; entry_number<n_entries; ++entry_number) {
        trigger_tree_m->GetEntryNumber(entry_number);
        
        midus_entry entry(t_branch_m);
        // Loop over all the registered algorithms
        for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
            entry.accept(get_algorithm(alg));
        }
    }
}

void midus_file::init() {

    
    trigger_tree_m = (TTree*) file_m->Get("Trigger");
    if (!trigger_tree_m) {
        std::cerr << "There was a problem opening the tree" << std::endl;
        std::exit(1);
    } else {
        trigger_tree_m->SetBranchAddress("TDC0", &t_branch_m.n_tdc);
        trigger_tree_m->SetBranchAddress("QDC", &t_branch_m.n_qdc);
    }
    n_entries = trigger_tree_m->GetEntries();
}
