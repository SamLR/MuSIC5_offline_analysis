// hist_x_ray.h
// -- Plots a histogram of <eqn> corresponding to x-ray energy
// Created: 17/06/2012 Andrew Edmonds


#ifndef HIST_X_RAY_H_
#define HIST_X_RAY_H_

#include "hist_maker_algorithm.h"

class hist_x_ray : public hist_maker_algorithm {
public:
	hist_x_ray(smart_tfile *const, std::string, int n_bins = 100, double x_low = 0, double x_high = 100);
	~hist_x_ray();
	
	void process(line_entry const *);
	void process(midus_entry const *);
	
};

#endif
