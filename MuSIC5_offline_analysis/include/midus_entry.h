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
    midus_entry(TDC_branch const&, QDC_branch const&);
    ~midus_entry(){;} ;
    void accept(algorithm* const) const;
    
    inline int get_number_QDC_values() const {return QDC_m.size();};
    inline int get_number_QDC_channels() const {return n_qdc_ch;};
    inline int get_number_TDC_values() const {return TDC_m.size();};
    inline int get_number_TDC_channels() const {return n_tdc_ch;};
    inline int get_number_TDC_hits() const {return n_tdc_hits_m;};
    inline double get_QDC_value(int i) const {return QDC_m[i];};
    inline double get_TDC_value(int i) const {return TDC_m[i];};
    
private:
    void init(TDC_branch const&, QDC_branch const&);
    midus_entry();
    
    std::vector<int> QDC_m;
    std::vector<int> TDC_m;
    
    int n_tdc_hits_m;
    int n_tdc_ch;
    int n_qdc_ch;
};

#endif
