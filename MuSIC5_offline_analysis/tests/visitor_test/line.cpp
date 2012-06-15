// line.cpp
// Represents a line of a text file (inherits from entry)
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>

#include "line.h"

line::line(std::string ln):actual_line_m(ln) {}

line::~line(){;}

std::string line::get_actual_line() const{
	return actual_line_m;
}
