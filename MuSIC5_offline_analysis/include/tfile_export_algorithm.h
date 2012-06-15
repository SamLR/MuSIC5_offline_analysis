// tfile_export_algorithm.h
// -- A class to export tfiles (will have derived classes)
// Created: 15/06/2012 Andrew Edmonds

#ifndef TFILE_EXPORT_ALGORITHM_H_
#define TFILE_EXPORT_ALGORITHM_H_

#include "algorithm.h"

#include "TFile.h"

class tfile_export_algorithm : public algorithm {
public:
	tfile_export_algorithm(TFile *const);
	virtual ~tfile_export_algorithm();
	
	virtual void process(line_entry const *) = 0;
	virtual void process(midus_entry const *);
    
private:
	TFile *const in_file_m;
};

#endif
