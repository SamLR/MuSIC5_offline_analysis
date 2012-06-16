//
//  smart_tfile_test.cpp
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 17/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#include <iostream>
#include "../../include/smart_tfile.h"
#include "TTree.h"

int main() {
    smart_tfile* file = smart_tfile::getTFile("run00020.root", "READ");
    
    TTree* tree = (TTree*) file->Get("Trigger");
    tree->Print();
    
    return 0;
}
