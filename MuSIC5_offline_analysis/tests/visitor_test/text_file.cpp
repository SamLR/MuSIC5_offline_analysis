// text_file.cpp
// -- A text file to use for testing
// Created: 14/06/2012 Andrew Edmonds

#include <iostream>

#include "input_file.h"

class text_file : public input_file {
	public:
		text_file(char* filename);
	
	private:
		char* filename_m;
}

text_file::text_file(char* filename):
filename_m (filename){
}

text_file::open() {
}

text_file::close(){
}

text_file::has_entry() {
}

text_file::get_entry() {
}
