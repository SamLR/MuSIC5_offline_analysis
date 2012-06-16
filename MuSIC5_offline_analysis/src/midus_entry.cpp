// midus_entry.cpp
// -- Implements the midus_entry methods
// Created: 15/06/2012 Andrew Edmonds

#include <iostream>
#include <vector>

#include "midus_entry.h"
#include "algorithm.h"
#include "midus_tree_structs.h"

midus_entry::midus_entry(counter_struct const& counter): counter_m(counter){
}

void midus_entry::accept(algorithm *const alg) const {
    alg->process(this);
}
