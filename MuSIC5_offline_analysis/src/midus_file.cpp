// midus_file.cpp
// -- Implements the midus_file methods
// Created: 15/06/2012 Andrew Edmonds

#include <cstdlib>

#include "midus_file.h"
#include "midus_entry.h"
#include "midus_tree_structs.h"
#include "TTree.h"


midus_file::midus_file(std::string const& filename)
: TFile(filename, "READ"), filename_m(filename), 
qdc_tree_m(0), tdc_tree_m(0), scaler_tree_m(0), q_branch_m(), t_branch_m(){
    init();
}

midus_file::~midus_file() {
	this->Close();
}

void midus_file::loop() {
	// Call default loop method
	input_file::loop();          
	
	// Loop over all the registered algorithms
	for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
    	//entry.accept(get_algorithm(alg));
    }
}

void midus_file::init() {
    // initialise the tree

    qdc_tree_m = (TTree*) this->Get("Trigger");
    if (!tree_m) {
        std::cerr << "There was a problem opening the tree" << std::endl;
        std::exit(1);
    } else {
    }
}

