// midus_entry.h
// -- Entry class for the midus ROOT file used as input
// Created: 15/06/2012 Andrew Edmonds

#ifndef MIDUS_ENTRY_H_
#define MIDUS_ENTRY_H_

#include "entry.h"

class algorithm;

class midus_file : public entry {
public:
	midus_entry();
	~midus_entry();
	void accept(algorithm *const) const;
};

#endif
