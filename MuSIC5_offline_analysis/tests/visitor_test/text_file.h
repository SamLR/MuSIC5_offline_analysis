//  text_file.h
//  -- Class declaration of text_file
//  Created: 14/06/2012 Andrew Edmonds


#ifndef TEXT_INPUT_H_
#define TEXT_INPUT_H_

#include <iostream>
#include <fstream>

#include "../../include/input_file.h"

class text_file : public input_file {
	public:
		text_file(char* filename);
		~text_file();
		
		void open();
    	void close();
    	bool has_next();
    	entry const* next_entry() const;	
	
	private:
		char* filename_m;
		std::ifstream in_file_m;
};

#endif
