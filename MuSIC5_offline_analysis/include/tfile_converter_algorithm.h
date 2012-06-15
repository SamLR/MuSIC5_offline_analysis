// tfile_converter_algorithm.h
// -- Converts an input midus file into a nice output file
// Created: 15/06/2012 Andrew Edmonds

#ifndef TFILE_CONVERTER_ALGORITHM_H_
#define TFILE_CONVERTER_ALGORITHM_H_

#include "tfile_export_algorithm.h"

class tfile_converter_algorithm : public tfile_export_algorithm {
public:
	tfile_converter_algorithm(TFile *const);
	~tfile_converter_algorithm();
	
	void process(line_entry const *);
	void process(midus_entry const *);

};

#endif
