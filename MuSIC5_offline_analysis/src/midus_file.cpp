// midus_file.cpp
// -- Implements the midus_file methods
// Created: 15/06/2012 Andrew Edmonds

#include "midus_file.h"
#include "midus_entry.h"

midus_file::midus_file() {
}

midus_file::~midus_file() {
}

void midus_file::loop() {
	// Call default loop method
	input_file::loop();
	std::cout << "Entered loop" << std::endl;
	
	midus_entry entry;
	
	// Loop over all the registered algorithms
	for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
    	entry.accept(get_algorithm(alg));
    }
}
