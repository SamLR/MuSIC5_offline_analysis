// hist_x_ray.h
// -- Plots a histogram of <eqn> corresponding to x-ray energy
// Created: 17/06/2012 Andrew Edmonds

#ifndef HIST_MU_LIFETIME_H_
#define HIST_MU_LIFETIME_H_

#include "hist_maker_algorithm.h"

class hist_x_ray : public hist_maker_algorithm {
public:
	hist_x_ray(smart_tfile *const, std::string, int n_bins, double x_low, double x_high);
	~hist_x_ray();
	
	void process(line_entry const *);
	void process(midus_entry const *);
	
};

#endif
