// midus_file.cpp
// -- Implements the midus_file methods
// Created: 15/06/2012 Andrew Edmonds

#include <cstdlib>

#include "midus_file.h"
#include "midus_entry.h"
#include "midus_tree_structs.h"
#include "TTree.h"

<<<<<<< HEAD
midus_file::midus_file(std::string const& filename)
: TFile(filename, "READ"), filename_m(filename), treename_m(treename),
qdc_tree_m(0), tdc_tree_m(0), scaler_tree_m(0), q_branch_m(), t_branch_m(){
=======
midus_file::midus_file(std::string const& filename, std::string const& treename): 
TFile(filename.c_str(), "READ"),filename_m(filename), treename_m(treename){
>>>>>>> a26520122f4a561989713069a00920175d680e1a
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
<<<<<<< HEAD
    qdc_tree_m = (TTree*) this->Get("QDC");
    tdc_tree_m = (TTree*) this->Get("TDC");    
    scaler_tree_m = (TTree*) this->Get("Scaler");
    
    if (!(qdc_tree_m && tdc_tree_m && scaler_tree_m) ) {
        std::cerr << "There was a problem opening one of the trees" << std::endl;
        exit(1);
    } else {
        qdc_tree_m->SetBranchAddress("Instance", q_branch_m.channel);
        qdc_tree_m->SetBranchAddress("QDC", q_branch_m.qdc);
        tdc_tree_m->SetBranchAddress("Instance", t_branch_m.channel);
        tdc_tree_m->SetBranchAddress("n_hits", t_branch_m.n_hits);
        tdc_tree_m->SetBranchAddress("TDC", t_branch_m.tdc);
    }
    
    n_entries_m =
}
=======
    tree_m = (TTree*) this->Get("Trigger");
    if (!tree_m) {
        std::cerr << "There was a problem opening the tree" << std::endl;
        std::exit(1);
    } else {
        //tree_m->SetBranchAddress("Instance", &q_branch_m.n_ch_m);
        //tree_m->SetBranchAddress("QDC", q_branch_m.value_m);
    }
    
}
>>>>>>> a26520122f4a561989713069a00920175d680e1a
