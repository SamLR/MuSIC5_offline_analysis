// line.cpp
// Represents a line of a text file (inherits from entry)
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>

#include "line.h"
#include "../../include/input_file.h"

line::line() {
}

line::line(input_file const* in_file): my_source_file_m(in_file) {
}

line::line(input_file const* file):entry(file){}

line::~line(){;}
