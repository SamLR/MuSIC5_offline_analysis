// midus_file.cpp
// -- Implements the midus_file methods
// Created: 15/06/2012 Andrew Edmonds

#include "midus_file.h"

midus_file::midus_file() {
}

midus_file::~midus_file() {
}

void midus_file::loop() {
	// Call default loop method
	input_file::loop();
	std::cout << "Entered loop" << std::endl;
}
