//
//  input_root_test_main.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>

#include "../../include/input_root.h"
#include "dumb_entry.h"

int main(int argc, const char * argv[])
{
    
    dumb_entry* d =  new dumb_entry();
    input_root* file = new input_root("test.root", "T",d);
    
    return 0;
}