//
//  visitor.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
// Loops over an input file and passes the results to 
// algorithms
//

#ifndef MuSIC5_offline_analysis_visitor_h
#define MuSIC5_offline_analysis_visitor_h

class input_file;
class algorithm;

class visitor {
public:
    visitor();
    virtual ~visitor();
    void loop() const; 
    
private:
    input_file const* input_file_m;
    algorithm const* algorithm_m;
};


#endif
