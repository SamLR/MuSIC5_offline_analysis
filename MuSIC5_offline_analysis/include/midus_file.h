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

typedef int (*calibrate_func)(const int ch, const int val);

class midus_file : public input_file{
public:
	midus_file(std::string const&);
	~midus_file();
	
	inline void loop() {loop(n_entries);};
    void loop(int const n_events);
    
    // this is here mainly for getting debugging information
    inline smart_tfile* get_file() {return file_m;};
    // register functions
    void add_calibration_func(int const, calibrate_func*);
	
private:
    void init();
    void extract_values_to(midus_out_branch[n_tdc_channels]) const;
    
    int get_qdc_val(int const) const;
    int get_qdc_ch(int const) const;
    int get_tdc_val(int const) const;
    int get_tdc_ch(int const) const;
    bool is_tdc_measure(int const) const;
    
    // there are 3 blocks of input equipment:
    // ADC, TDC & PHADC (TDC needs to be parallelised by channel)
    static int const n_branches_in=3; 
    
    smart_tfile* file_m;
    std::string const filename_m;
    TTree* trigger_tree_m;
    TTree* scaler_tree_m;

    midus_out_branch branches_m[n_branches_in];
    calibrate_func* calibration_funcs[n_branches_in];
    int n_entries;
    
    enum in_branch_indexs{
        qdc_i  = 0,
        adc0_i = 1,
        adc1_i = 2,
        tdc_i  = 3
    };
};

inline int midus_file::get_qdc_val(int const index) const {
    static int const underflow_mask = 0x00002000;
    static int const overflow_mask  = 0x00001000;
    static int const data_mask      = 0x00000fff;
    int const val = static_cast<unsigned int>(branches_m[qdc_i].data[index]);
    
    if (   !(val & underflow_mask)
        && !(val & overflow_mask)) { 
        return (val & data_mask); 
    } else {
        return 0;
    }
}

inline int midus_file::get_qdc_ch(const int index) const {
    static int const channel_mask = 0x001f0000;
    int const val = static_cast<unsigned int>(branches_m[qdc_i].data[index]);
    return (val & channel_mask) >> 17;
}

inline int midus_file::get_tdc_val(const int index) const {
    static int const tdc_data_mask    =   0x1fffff;
    int const val = static_cast<unsigned int>(branches_m[tdc_i].data[index]);
    return (val & tdc_data_mask);
}

inline int midus_file::get_tdc_ch(const int index) const {
    static int const tdc_channel_mask = 0x03e00000;
    int const val = static_cast<unsigned int>(branches_m[tdc_i].data[index]);
    return (val & tdc_channel_mask) >> 21;
}

inline bool midus_file::is_tdc_measure(const int index) const {
    static int const tdc_data_type_mask = 0xf8000000;
    static int const tdc_measurement    = 0x00000000;
    int const val = static_cast<unsigned int>(branches_m[tdc_i].data[index]);
    return ((val & tdc_data_type_mask) == tdc_measurement);
}
#endif
