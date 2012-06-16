// midus_entry.h
// -- Entry class for the midus ROOT file used as input
// Created: 15/06/2012 Andrew Edmonds

#ifndef MIDUS_ENTRY_H_
#define MIDUS_ENTRY_H_

#include "entry.h"
#include "midus_tree_structs.h"

class algorithm;

class midus_entry: public entry {
public:
    midus_entry(trigger_branch const&);
    ~midus_entry(){;} ;
    void accept(algorithm* const) const;
    
    inline int get_number_QDC_values() const {return n_qdc_vals_m;};
    inline int get_number_TDC_values() const {return n_tdc_vals_m;};
    
    inline double get_QDC_value(int i) const {return qdc_vals_m[i];};
    inline double get_TDC_value(int i) const {return tdc_vals_m[i];};
    
private:
    void init(trigger_branch const&);
    midus_entry();
    
    int qdc_vals_m[QDC_CH];
    int tdc_vals_m[MAX_TDC_HITS];
    
    int n_tdc_vals_m;
    int n_qdc_vals_m;
};

#endif
