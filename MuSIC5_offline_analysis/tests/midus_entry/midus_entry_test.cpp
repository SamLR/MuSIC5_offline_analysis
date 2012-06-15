//
//  midus_entry_test.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 15/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include "dummy_midus.h"
#include "../../include/printer_alg.h"


int main(){
    
    dummy_midus* dm = new dummy_midus(10);
    dm->add_algorithm(new printer_alg());
    dm->loop();
    
    return 0;
}