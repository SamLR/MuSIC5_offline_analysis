// text_file.cpp
// -- A text file to use for testing
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>
#include <string>
#include <sstream>

#include "text_file.h"

text_file::text_file(char* filename):
filename_m (filename){
}

text_file::~text_file() {
}

void text_file::open() {
	in_file_m.open(filename_m);
}

void text_file::close(){
	in_file_m.close();
}

bool const text_file::has_next() const {
	return in_file_m.eof();
}

line const *const text_file::next_entry() {
    char buffer[80];
	std::stringstream ss;
    in_file_m.getline(buffer, 80);
    
    ss << buffer;
	line const *const new_line = new line(this, ss.str());
	return new_line;
}
