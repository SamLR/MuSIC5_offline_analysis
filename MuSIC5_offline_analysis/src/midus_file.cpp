// midus_file.cpp
// -- Implements the midus_file methods
// Created: 15/06/2012 Andrew Edmonds

#include <cstdlib>

#include "midus_file.h"
#include "midus_entry.h"
#include "midus_tree_structs.h"
#include "TFile.h"
#include "TTree.h"

static int const midus_file::n_branches = n_branches_in_trigger_tree;

midus_file::midus_file(std::string const& filename)
: TFile(filename.c_str(), "READ"), filename_m(filename), 
trigger_tree_m(0), scaler_tree_m(0), branches_m() n_entries(0) {
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
        
        midus_entry entry(branches_m);
        // Loop over all the registered algorithms
        for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
            entry.accept(get_algorithm(alg));
        }
    }
}

void midus_file::init() {
    trigger_tree_m = (TTree*) this->Get("Trigger");
    if (!trigger_tree_m) {
        std::cerr << "There was a problem opening the tree" << std::endl;
        std::exit(1);
    } else {
        if (n_branches < 2) {
            std::cerr <<"This is an unlikely number of branches" << std::endl;
            exit(1);
        } else if (n_branches==2) {
            trigger_tree_m->SetBranchAddress("QDC", &(branches_m[0]));
            trigger_tree_m->SetBranchAddress("TDC0", &(branches_m[1]));
        } else {
            trigger_tree_m->SetBranchAddress("ADC", &(branches_m[0]));
            trigger_tree_m->SetBranchAddress("PHADC", &(branches_m[1]));
            for (int i = 0; i < (n_branches-2); ++i) {
                std::string name("TDC");
                name << i;
                trigger_tree_m->SetBranchAddress(name.c_str(), &(branches_m[i]));
            }
        }
    }
    n_entries = trigger_tree_m->GetEntries();
}
