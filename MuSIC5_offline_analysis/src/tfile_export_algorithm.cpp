// tfile_export_algorithm.cpp
// -- Implements the methods
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>

#include "tfile_export_algorithm.h"

tfile_export_algorithm::tfile_export_algorithm() {
	std::cout << "Constructed" << std::endl;
}

tfile_export_algorithm::~tfile_export_algorithm() {
}

void tfile_export_algorithm::process(line_entry const *) {
	std::cout << "Called with a line entry" << std::endl;
}

void tfile_export_algorithm::process(midus_entry const *) {
	std::cout << "Called with a midus_entry" << std::endl;
}
