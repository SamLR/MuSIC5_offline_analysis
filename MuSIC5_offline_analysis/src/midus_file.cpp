// midus_file.cpp
// -- Implements the midus_file methods
// Created: 15/06/2012 Andrew Edmonds

#include "midus_file.h"
#include "midus_entry.h"
#include "midus_tree_structs.h"

midus_file::midus_file(std::string filename) {
	file_m = new TFile(filename.c_str(), "READ");
}

midus_file::~midus_file() {
	file_m->Close();
}

void midus_file::loop() {
	// Call default loop method
	input_file::loop();
	std::cout << "Entered loop" << std::endl;
	
	// Get the TTrees from the ROOT file
	TTree* trigger = (TTree*) file_m->Get("Trigger;1");
	//TTree* scaler = (TTree*) file_m->Get("Scaler;1");
	
	//std::cout << trigger->GetEntries() << std::endl;
	trigger->Print();
	
	// FIll the QDC_branch and TDC_branch which will be passed to midus_entry to create the entry
	/*QDC_branch qdc_br;
	trigger->SetBranchAddress("QDC/nQDC", &qdc_br.n_ch_m);
	trigger->SetBranchAddress("QDC/QDC", 
	
	trigger->GetEvent(21);
	std::cout << qdc_br.n_ch_m << std::endl;*/
	
	// Loop over all the registered algorithms
	for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
    	//entry.accept(get_algorithm(alg));
    }
}
