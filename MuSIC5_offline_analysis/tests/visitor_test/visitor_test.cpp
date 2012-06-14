// visitor_test.cpp
// -- Tests the visitor class on a simple text file
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>

#include "text_file.h"
#include "printer.h"
#include "line.h"
#include "../../include/visitor.h"

int main() {
    
    char name[] = "test_input.txt";
	std::cout << "Testing visitor class" << std::endl;
	text_file * const input = new text_file(name);
	std::cout << "Created text_file object" << std::endl;
	
	input->open();
	std::cout << "Opened input file" << std::endl;
	
	printer* printer_object = new printer();
	std::cout << "Created printer object" << std::endl;
	
	visitor tester(input, printer_object);
	std::cout << "Created tester" << std::endl;
	
	//visitor->loop();
	
	input->close();
	std::cout << "Closed input file" << std::endl;
	return 0;
}
