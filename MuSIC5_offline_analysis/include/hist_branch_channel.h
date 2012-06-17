// hist_branch_channel.h
// -- Simply plots a histogram all the values in a branch (ADC, TDC0 etc.) for a single channel 
// -- An example of how to use hist_maker_algorithm
// Created: 16/06/2012 Andrew Edmonds

#ifndef HIST_BRANCH_CHANNEL_H_
#define HIST_BRANCH_CHANNEL_H_

#include "hist_maker_algorithm.h"

class hist_branch_channel : public hist_maker_algorithm {
public:
	hist_branch_channel(smart_tfile *const, std::string, int channel, int branch, int n_bins = 100, double x_low = 0, double x_high = 100);
	~hist_branch_channel();
	
	void process(line_entry const *);
	void process(midus_entry const *);
	
private:
	int channel_m;
	int branch_m;
};

#endif
