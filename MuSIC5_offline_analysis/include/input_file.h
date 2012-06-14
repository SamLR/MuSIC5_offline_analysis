//
//  input_file.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
// This is an abstract base class for input files
// that is designed to give access to each entry
// within some structure(s)
// 


#ifndef MuSIC5_offline_analysis_input_file_h
#define MuSIC5_offline_analysis_input_file_h

class entry;
class algorithm;

#include <vector>

using namespace std;

class input_file {
public:
    input_file(){;};
    virtual ~input_file() {;};
    virtual void loop() = 0;
    
    void add_algorithm(algorithm *const a);
    
protected:
    int const get_number_algorithms() const;
    algorithm *const get_algorithm(int const) const;
    
private: 
    // disable assignment and copy constructors
    input_file& operator= (input_file const &);
    input_file(input_file const&);
    vector<algorithm *const> algos_m;
};

inline void input_file::add_algorithm(algorithm *const a) {
    algos_m.push_back(a);
};

inline int const input_file::get_number_algorithms() const {
    return algos_m.size();
}

inline algorithm *const input_file::get_algorithm(const int n) const{
    return algos_m[n];
}

#endif
