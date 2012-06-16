// midus_file.h
// -- Class for the midus_file
// Created: 15/06/2012 Andrew Edmonds

#ifndef MIDUS_FILE_H_
#define MIDUS_FILE_H_

#include <iostream>
#include <string>

// local gubbins
#include "input_file.h"
#include "midus_tree_structs.h"

class TTree;
class smart_tfile;

class midus_file : public input_file{
public:
	midus_file(std::string const&);
	~midus_file();
	
	void loop();
    // this is here mainly for getting debugging information
    inline smart_tfile* get_file() {return file_m;};
	
private:
    void init();
    
    static int const n_branches=n_branches_in_trigger_tree;    
    smart_tfile* file_m;
    std::string const filename_m;
    TTree* trigger_tree_m;
    TTree* scaler_tree_m;
    midus_out_branch branches_m[n_branches];
    int n_entries;
};

#endif
