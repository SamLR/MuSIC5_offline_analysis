// visitor_test.cpp
// -- Tests the visitor class on a simple text file
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>

#include "text_file.h"
#include "printer.h"
#include "line.h"
#include "../../include/visitor.h"

int main() {
	std::cout << "Testing visitor class" << std::endl;
	text_file * const input = new text_file("test_input.txt");
	std::cout << "Created text_file object" << std::endl;
	
	input->open();
	std::cout << "Opened input file" << std::endl;
	
	printer* printer_object = new printer();
	std::cout << "Created printer object" << std::endl;
	
	visitor* tester = new visitor(input, printer_object);
	std::cout << "Created tester" << std::endl;
	
	std::cout << "Entering loop" << std::endl;
	tester->loop();
	std::cout << "Left loop" << std::endl;
	
	input->close();
	std::cout << "Closed input file" << std::endl;
	return 0;
}
