// printer.cpp
// -- Prints a line
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>

#include "printer.h"

printer::printer() {
}

printer::~printer() {
}

void printer::process(line const* ln) {
	std::cout << "In printer process()" << std::endl;
	std::cout << ln->get_actual_line() << std::endl;
}
