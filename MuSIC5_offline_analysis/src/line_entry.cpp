//
//  line_entry.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>

#include <string>
#include "algorithm.h"
#include "line_entry.h"

using namespace std;

line_entry::line_entry(){;}

line_entry::line_entry(string const* line) : line_m(line) {;}

void line_entry::accept(algorithm const& algo) const {
    algo.process(this);
}

