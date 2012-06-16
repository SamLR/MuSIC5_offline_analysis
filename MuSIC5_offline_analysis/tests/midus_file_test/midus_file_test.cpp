//
//  midus_file_test.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 16/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include "../../include/midus_file.h"
#include "../../include/printer_alg.h"

int main(){
    std::string file("run00020.root");
    midus_file* mf = new midus_file(file);
    printer_alg* alg = new printer_alg();
    mf->add_algorithm(alg);
    mf->loop();
    
    
    return 0;
}