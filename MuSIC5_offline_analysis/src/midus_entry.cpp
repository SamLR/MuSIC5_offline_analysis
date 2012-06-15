// midus_entry.cpp
// -- Implements the midus_entry methods
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>

#include "midus_entry.h"

midus_entry::midus_entry() {std::cout << "midus_entry constructor" << std::endl;}

midus_entry::~midus_entry() {std::cout << "midus_entry destructor" << std::endl;}

void midus_entry::accept(algorithm *const alg) const
{
}
