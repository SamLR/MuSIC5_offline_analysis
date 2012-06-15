// line.h 
// -- A line of a text file (inherits from entry)
// Created: 14/06/2012 Andrew Edmonds

#ifndef LINE_H_
#define LINE_H_

#include <iostream>
#include <string>

#include "../../include/entry.h"

class line : public entry {
public:
	line();
    line(std::string ln);
    ~line();
    std::string get_actual_line() const;
    
private:
    std::string actual_line_m;
};

#endif
