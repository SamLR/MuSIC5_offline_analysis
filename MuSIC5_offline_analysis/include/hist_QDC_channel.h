// hist_QDC_channel.h
// -- Simply plots a histogram of the charges in a single QDC channel
// -- An example of how to use hist_maker_algorithm
// Created: 16/06/2012 Andrew Edmonds

#ifndef HIST_QDC_CHANNEL_H_
#define HIST_QDC_CHANNEL_H_

#include "hist_maker_algorithm.h"

class hist_QDC_channel : public hist_maker_algorithm {
public:
	hist_QDC_channel(TFile *const, std::string, int channel, int n_bins = 100, double x_low = 0, double x_high = 100);
	~hist_QDC_channel();
	
	void process(line_entry const *);
	void process(midus_entry const *);
	
private:
	int channel_m;
};

#endif
