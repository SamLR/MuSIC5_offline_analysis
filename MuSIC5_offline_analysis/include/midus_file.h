// midus_file.h
// -- Class for the midus_file
// Created: 15/06/2012 Andrew Edmonds

#ifndef MIDUS_FILE_H_
#define MIDUS_FILE_H_

#include <iostream>

#include "input_file.h"

class midus_file : public input_file {
public:
	midus_file();
	~midus_file();
	
	void loop();
};

#endif
