// tfile_converter_algorithm.h
// -- Converts an input midus file into a nice output file
// Created: 15/06/2012 Andrew Edmonds

#ifndef TFILE_CONVERTER_ALGORITHM_H_
#define TFILE_CONVERTER_ALGORITHM_H_

#include "tfile_export_algorithm.h"

#include "TFile.h"
#include "TTree.h"

class tfile_converter_algorithm : public tfile_export_algorithm {
public:
	tfile_converter_algorithm(smart_tfile *const);
	~tfile_converter_algorithm();
	
	void process(line_entry const *);
	void process(midus_entry const *);

private:
	void init();
	TTree* tree_m;
};

#endif
