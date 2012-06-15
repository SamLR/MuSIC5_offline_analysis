// midus_entry.h
// -- Entry class for the midus ROOT file used as input
// Created: 15/06/2012 Andrew Edmonds

#ifndef MIDUS_ENTRY_H_
#define MIDUS_ENTRY_H_

#include <vector>

#include "entry.h"

class algorithm;

class midus_entry : public entry {
public:
	midus_entry();
	~midus_entry();
	void accept(algorithm *const) const;
	
	double get_QDC_value(int) const;
	double get_TDC_value(int) const;
	int get_event_number() const;
	
	int get_number_QDC_values() const;
	int get_number_TDC_values() const;

private:
	std::vector<double> QDC_m;
	std::vector<double> TDC_m;
	int event_number_m;
};

#endif
