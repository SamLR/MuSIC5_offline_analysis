// tfile_export_algorithm.h
// -- A class to export tfiles (will have derived classes)
// Created: 15/06/2012 Andrew Edmonds

#ifndef TFILE_EXPORT_ALGORITHM_H_
#define TFILE_EXPORT_ALGORITHM_H_

#include "algorithm.h"

class tfile_export_algorithm : public algorithm {
public:
	tfile_export_algorithm();
	virtual ~tfile_export_algorithm();
	
	void process(line_entry const *);
    void process(midus_entry const *);
};

#endif
