// line.h 
// -- A line of a text file (inherits from entry)
// Created: 14/06/2012 Andrew Edmonds

#ifndef LINE_H_
#define LINE_H_

#include <iostream>

#include "../../include/entry.h"

class text_file;

class line : public entry {
public:
    line(input_file const*);
    ~line();
private:
    
    line();

};

#endif
