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
    midus_entry(midus_out_branch const []);
    ~midus_entry(){;} ;
    void accept(algorithm* const) const;
    
    inline int get_number_of_branches() const 
        {return n_branches;};
    inline int get_entries_in_branch(int const b) const 
        {return branches_m[b].n_entries;};
    inline int get_value_in_branch(int const b, int const i) const 
        {return branches_m[b].data[i];};    

private:
    midus_entry();
    void init(midus_out_branch const []);
    
    midus_out_branch branches_m[n_branches_in_trigger_tree];
    
    static int const n_branches;
};



#endif
