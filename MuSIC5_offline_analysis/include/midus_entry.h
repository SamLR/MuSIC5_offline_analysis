// midus_entry.h
// -- Entry class for the midus ROOT file used as input
// Created: 15/06/2012 Andrew Edmonds

#ifndef MIDUS_ENTRY_H_
#define MIDUS_ENTRY_H_

#include "entry.h"
#include "counter_struct.h"

class algorithm;

class midus_entry: public entry {
public:
    midus_entry(counter_struct const&);
    ~midus_entry(){;} ;
    void accept(algorithm* const) const;
    
    inline int get_number_QDC_values() const {return n_qdc_vals_m;};
    inline int get_number_TDC_values() const {return n_tdc_vals_m;};
    
    inline double get_QDC_value(int i) const {return qdc_vals_m[i];};
    inline double get_TDC_value(int i) const {return tdc_vals_m[i];};
    
private:
    midus_entry();
    
    counter_struct* counter_m;
};

#endif
