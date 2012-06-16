// midus_file.h
// -- Class for the midus_file
// Created: 15/06/2012 Andrew Edmonds

#ifndef MIDUS_FILE_H_
#define MIDUS_FILE_H_

#include <iostream>
#include <string>

// From ROOT
#include "TFile.h"
// local gubbins
#include "input_file.h"
#include "midus_tree_structs.h"

class TTree;

class midus_file : public input_file , TFile{
public:
	midus_file(std::string const&);
	~midus_file();
	
	void loop();
	
private:
    void init();
    
    std::string const filename_m;
    TFile* file_m;
    TTree* trigger_tree_m;
    TTree* scaler_tree_m;

    midus_out_branch t_branch_m[1];
    int n_qdc_channels_m;
    int n_tdc_hits_m;
    int n_entries;
};

#endif
