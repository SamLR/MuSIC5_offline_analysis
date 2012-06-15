// midus_test.cpp
// -- To test the midus_entry class
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>

#include "../../include/midus_entry.h"
#include "../../include/printer_alg.h"

int main() {
	midus_entry const* test = new midus_entry();
	printer_alg* printer = new printer_alg();
	printer->process(test);
	
	delete printer;
	delete test;
	return 0;
}
