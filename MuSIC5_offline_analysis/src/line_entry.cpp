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


// basic constructor probably shouldn't be used
line_entry::line_entry():line_m("this is a default line"){;}

// tidy up
line_entry::~line_entry(){;}

// initialise the line with a value
line_entry::line_entry(std::string const &line) : line_m(line) {;}

// the required function for the visitor pattern
// essentially let the algorithm know what it's being 
// called on
void line_entry::accept(algorithm *const alg) const{
    alg->process(this);
}