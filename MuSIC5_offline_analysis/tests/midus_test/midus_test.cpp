// midus_test.cpp
// -- To test the midus_entry class
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>

#include "../../include/midus_entry.h"
#include "../../include/printer_alg.h"
#include "../../include/midus_file.h"

int main() {
	midus_entry const* test = new midus_entry();
	midus_file* file = new midus_file();
	printer_alg* printer = new printer_alg();
	
	file->add_algorithm(printer);
	file->loop();
	
	delete printer;
	delete test;
	return 0;
}
