//
//  input_file.h
//  MuSIC5_offline_analysis
//
//  Created by Sam Cook on 14/06/2012.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
//  This is an abstract base class for input files
//  Each subclass must implement its own version of
//  'loop' that will loop over the entries of the file
//  and apply the registered algorithms to each entry
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
    // the function that must be implemented by all subclasses
    virtual void loop() = 0;
    // add an algorithm to those that will be tested
    void add_algorithm(algorithm* a);
    
protected:
    int const get_number_algorithms() const;
    algorithm *const get_algorithm(int const) const;
    
private: 
    // disable assignment and copy constructors
    input_file& operator= (input_file const &);
    input_file(input_file const&);
    vector<algorithm*> algos_m;
};

inline void input_file::add_algorithm(algorithm* a) {
    algos_m.push_back(a);
};

inline int const input_file::get_number_algorithms() const {
    return algos_m.size();
}

inline algorithm *const input_file::get_algorithm(const int n) const{
    return algos_m[n];
}

inline void input_file::loop(){
    // this is a default implementation of loop, that can add common functionality
    // you must still provide your own version but this can be added
    // to yours using 'input_fill::loop()'
    if (!algos_m.size()) {
        cerr << "WARNING: no algorithms registered" << endl;
    }
}
#endif
