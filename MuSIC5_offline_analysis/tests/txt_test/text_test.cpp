//
//  text_test.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include "../../include/txt_file.h"
#include "../../include/printer_alg.h"

using namespace std;

int main(){
    string s("test_input.txt");
    txt_file* tf = new txt_file(s);
    printer_alg* pa = new printer_alg();
    tf->add_algorithm(pa);
    tf->loop();
    
    delete tf;
    delete pa;
}