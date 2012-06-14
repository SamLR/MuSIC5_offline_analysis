// line.cpp
// Represents a line of a text file (inherits from entry)
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>

#include "line.h"
#include "../../include/input_file.h"

line::line(input_file const* file, std::string ln):actual_line_m(ln) {}

line::~line(){;}

std::string line::get_actual_line() const{
	return actual_line_m;
}
