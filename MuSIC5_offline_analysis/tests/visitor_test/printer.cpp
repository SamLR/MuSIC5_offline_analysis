// printer.cpp
// -- Prints a line
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>

#include "printer.h"

printer::printer(line* in_line):ln_m(in_line) {;}



printer::~printer() {;}

void printer::process(entry const* ln) {
    std::cout << ln_m->get_actual_line()<< std::endl;
}
