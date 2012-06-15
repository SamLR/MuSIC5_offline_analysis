// midus_file.cpp
// -- Implements the midus_file methods
// Created: 15/06/2012 Andrew Edmonds

#include "midus_file.h"
#include "midus_entry.h"

midus_file::midus_file(std::string filename) {
	std::cout << filename << std::endl;
	file_m = new TFile(filename.c_str(), "READ");
}

midus_file::~midus_file() {
	file_m->Close();
}

void midus_file::loop() {
	// Call default loop method
	input_file::loop();
	std::cout << "Entered loop" << std::endl;
	
	//midus_entry entry;
	// Get the TTrees from the ROOT file
	TTree* trigger = (TTree*) file_m->Get("Trigger;1");
	TTree* scaler = (TTree*) file_m->Get("Scaler;1");
	
	//TBranch* qdc = (TBranch*) trigger->GetBranch();
	
	// Loop over all the registered algorithms
	for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
    	//entry.accept(get_algorithm(alg));
    }
}
