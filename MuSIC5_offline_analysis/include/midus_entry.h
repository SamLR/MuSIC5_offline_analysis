// midus_entry.h
// -- Entry class for the midus ROOT file used as input
// Created: 15/06/2012 Andrew Edmonds

#ifndef MIDUS_ENTRY_H_
#define MIDUS_ENTRY_H_

#include "entry.h"
#include "midus_tree_structs.h"
#include <vector>

class algorithm;

class midus_entry: public entry {
public:
    midus_entry(TDC_branch&, QDC_branch&);
    ~midus_entry(){;} ;
    void accept(algorithm* const) const;
    
private:
    void init(TDC_branch&, QDC_branch&);
    midus_entry();
    
    std::vector<double> QDC_m;
    std::vector<double> TDC_m;
    
    int event_number_m;
    int n_tdc_hits_m;
    
};

#endif
