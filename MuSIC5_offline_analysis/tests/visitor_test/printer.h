// printer.h
// -- An algorithm that prints each entry
// Created: 14/06/2012 Andrew Edmonds

#ifndef PRINTER_H_
#define PRINTER_H_

#include <iostream>

#include "../../include/algorithm.h"
#include "line.h"

class printer : public algorithm {
public:
	printer();
	~printer();
	void process(line const*);
	
	void test() {std::cout << "This is a printer." << std::endl;};
};

#endif
