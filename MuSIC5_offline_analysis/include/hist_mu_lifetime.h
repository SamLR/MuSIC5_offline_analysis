// hist_mu_lifetime.h
// -- Plots a histogram of tdc - tdc0 (for all tdc channels and all hits in each channel) corresponding to muon lifetime
// Created: 17/06/2012 Andrew Edmonds

#ifndef HIST_MU_LIFETIME_H_
#define HIST_MU_LIFETIME_H_

#include "hist_maker_algorithm.h"

class hist_mu_lifetime : public hist_maker_algorithm {
public:
	hist_mu_lifetime(smart_tfile *const, std::string, int n_bins = 100, double x_low = 0, double x_high = 100);
	~hist_mu_lifetime();
	
	void process(line_entry const *);
	void process(midus_entry const *);
	
private:
};

#endif
