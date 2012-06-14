// printer.h
// -- An algorithm that prints each entry
// Created: 14/06/2012 Andrew Edmonds

#ifndef PRINTER_H_
#define PRINTER_H_

#include <iostream>

#include "../../include/algorithm.h"
#include "line.h"

class printer : public algorithm{
public:
    printer():ln_m(0) {;};
	printer(line*);
	~printer();
	void process(line *);   

private: 
    line* ln_m;
};

#endif
