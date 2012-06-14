// visitor.cpp
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>

#include "visitor.h"

// Constructor
visitor::visitor(input_file const* in_file, algorithm const* algthm):
input_file_m(in_file), algorithm_m(algthm){
}

// Destructor
visitor::~visitor() {
}

// loop()
// Goes through the input_file, grabbing each entry and passing it to the algorithm to process
void visitor::loop() const {
	while (input_file_m->has_next()) {
		algorithm_m->process(input_file_m->get_entry());
	}
}
