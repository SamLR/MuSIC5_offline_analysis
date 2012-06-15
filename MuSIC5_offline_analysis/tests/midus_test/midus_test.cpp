// midus_test.cpp
// -- To test the midus_entry class
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <string>

#include "../../include/midus_entry.h"
#include "../../include/printer_alg.h"
#include "../../include/midus_file.h"

int main() {
	std::string filename("../../rootfiles/tests/run00459.root");
	midus_file* file = new midus_file(filename);
	//printer_alg* printer = new printer_alg();
	
	//file->add_algorithm(printer);
	//file->loop();
	
	delete file;
	//delete printer;
	return 0;
}
