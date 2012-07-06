// midus_file.cpp
// -- Implements the midus_file methods
// Created: 15/06/2012 Andrew Edmonds

#include <cstdlib>
#include <assert.h>

#include "midus_file.h"
#include "midus_entry.h"
#include "midus_structure.h"
#include "smart_tfile.h"
#include "TTree.h"
#include "calibration_functions.h"
#include "scaler_entry.h"

midus_file::midus_file(std::string const& filename)
: file_m(0), filename_m(filename), 
trigger_tree_m(0), scaler_tree_m(0), branches_m(),  n_entries(0), 
scaler_algs(0){
    init();
}

midus_file::~midus_file() {
	file_m->close();
}

void midus_file::loop(int const n_events) {
	// Call default loop method
	input_file::loop();          
    for (int entry_number = 0; entry_number<n_events; ++entry_number) {	
        trigger_tree_m->GetEntry(entry_number);
        if (entry_number%10000 == 0) std::cout << "Entry "<< entry_number<<std::endl;
        if (branches_m[err_i].data[0] > 0) {
            std::cerr << "error found in entry " << entry_number;
            std::cerr << ". Skipping this entry"<< std::endl;
            continue;
        }
        
        midus_structure::midus_out_branch parallel_branches[midus_structure::n_branches_in_midus_entry];
        
        extract_values_to(parallel_branches);
        
        midus_entry entry(parallel_branches);
        // Loop over all the registered algorithms
        for (int alg = 0; alg < get_number_algorithms() ; ++alg) {
            entry.accept(get_algorithm(alg));
        }
    }
    
    if(scaler_algs.size()==0) return;
    
    int const n_scaler_entries = scaler_tree_m->GetEntries();
    for (int sclr_entry = 0; sclr_entry < n_scaler_entries; ++sclr_entry) {
        scaler_tree_m->GetEntry();
        scaler_entry s_entry(scaler_vals);
        for (int s_alg = 0; s_alg < scaler_algs.size(); ++s_alg) {
            s_entry.accept(scaler_algs[s_alg]);
        }
    }
}

void midus_file::init() {
    std::string const file_mode("READ");
    file_m = smart_tfile::getTFile(filename_m, file_mode);
    
    trigger_tree_m = (TTree*) file_m->Get("Trigger");
    if (!trigger_tree_m) {
        std::cerr << "There was a problem opening the trigger tree" << std::endl;
    } else {
        trigger_tree_m->SetBranchAddress("QDC",  &(branches_m[qdc_i] ));
        trigger_tree_m->SetBranchAddress("ADC0", &(branches_m[adc0_i]));
        trigger_tree_m->SetBranchAddress("ADC1", &(branches_m[adc1_i]));
        trigger_tree_m->SetBranchAddress("TDC0", &(branches_m[tdc_i] ));
        trigger_tree_m->SetBranchAddress("ERR",  &(branches_m[err_i] ));
    }
    n_entries = trigger_tree_m->GetEntries();
    
    // initialise the calibration functions
    for (int b = 0; b<n_branches_in; ++b) {
        calibration_funcs [b] = &(null_calibration);
    }
    
    scaler_tree_m = (TTree*) file_m->Get("Scaler");
    if (!scaler_tree_m) {
        std::cerr << "There was a problem opening the scaler tree" << std::endl;
    } else {
        scaler_tree_m->SetBranchAddress("SCLR", scaler_vals);
    }
    
}

void midus_file::add_calibration_func(const int branch, calibrate_func func){
    if (branch > n_branches_in) {
        std::cerr <<"branch" << branch<< " number out of range, max = "<< n_branches_in << std::endl;
    } else {
        calibration_funcs[branch] = func;
    }
}

void midus_file::add_scaler_algorithm(scaler_algorithm *const alg){
    scaler_algs.push_back(alg);
}

void midus_file::extract_values_to(midus_structure::midus_out_branch* out_branches) const {
    // copy and process each branch in turn
    
    // QDC branch
    int n_entries = branches_m[qdc_i].n_entries;
    out_branches[midus_structure::eMEB_qdc].n_entries = n_entries;
    
    for (int ch = 0 ; ch<branches_m[qdc_i].n_entries; ++ch) {
        // all QDC channels (0-18) are read out but only using 
        // channels 1-13 (which will become indexes 0-12)
        int calc_ch = get_qdc_ch(ch);
		bool good_dat = is_good_qdc_measure(ch);
        if (   calc_ch < midus_structure::eQDC_U1 
            || calc_ch > midus_structure::eQDC_D5 
            || !good_dat) continue;
        int val = calibration_funcs[qdc_i](calc_ch, get_qdc_val(ch), 0);
        out_branches[0].data[calc_ch - 1] = val;
    }
    
    // ADC channel 0, just needs copying across
    n_entries = branches_m[adc0_i].n_entries;
    out_branches[midus_structure::eMEB_adc0].n_entries = n_entries;
    for (int ch = 0; ch < n_entries; ++ch) {
        int val = calibration_funcs[adc0_i](ch, branches_m[adc0_i].data[ch],0);
        out_branches[midus_structure::eMEB_adc0].data[ch] = val;
    }
    // ADC channel 1 is the same as channel 0
    n_entries = branches_m[adc1_i].n_entries;
    out_branches[midus_structure::eMEB_adc1].n_entries = n_entries;
    for (int ch = 0; ch < n_entries; ++ch) {
        int val = calibration_funcs[adc1_i](ch, branches_m[adc1_i].data[ch],0);
        out_branches[midus_structure::eMEB_adc1].data[ch] = val;
    }
    
    int n_hits[midus_structure::n_tdc_channels];
    for (int ch = 0; ch < midus_structure::n_tdc_channels; ++ch) n_hits[ch] = 0;
    
    n_entries = branches_m[tdc_i].n_entries;
    for (int hit = 0; hit<n_entries; ++hit) {
        if (!is_good_tdc_measure(hit))  continue;
        
        // split 
        
        int const tdc_ch = get_tdc_ch(hit);
        int const val = get_tdc_val(hit);
        int const branch_no = midus_structure::eMEB_tdc0 + tdc_ch;
        int const ch_hit_no = n_hits[tdc_ch];
        out_branches[branch_no].data[ch_hit_no] = val;
        ++n_hits[tdc_ch];
    }
    
    for (int ch = midus_structure::eMEB_tdc0; ch < (midus_structure::n_tdc_channels+ midus_structure::eMEB_tdc0); ++ch) {

        out_branches[ch].n_entries = n_hits[ch - midus_structure::eMEB_tdc0];
        if (ch == midus_structure::eMEB_tdc0) continue;
        int tdc0 = out_branches[midus_structure::eMEB_tdc0].data[0];

        for (int hit = 0; hit < out_branches[ch].n_entries; ++hit) {
            out_branches[ch].data[hit] = 
                calibration_funcs[tdc_i](ch, out_branches[ch].data[hit], tdc0);
            
        }
    }
    
}










