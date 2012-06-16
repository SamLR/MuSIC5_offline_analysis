// hist_maker_algorithm.h
// -- Creates a histogram from the input midus file
// Created: 16/06/2012 Andrew Edmonds

#ifndef HIST_MAKER_ALGORITHM_H_
#define HIST_MAKER_ALGORITHM_H_

#include "tfile_export_algorithm.h"

#include "TH1.h"

class hist_maker_algorithm : public tfile_export_algorithm {
public:
	hist_maker_algorithm(TFile *const, std::string, int n_bins = 100, double x_low = 0, double x_high = 100);
	~hist_maker_algorithm();
	
	void process(line_entry const *);
	void process(midus_entry const *);
	
	void set_title(std::string title) { hist_m->SetTitle(title.c_str()); };
	void set_x_axis_title(std::string title) { hist_m->GetXaxis()->SetTitle(title.c_str()); };
	void set_y_axis_title(std::string title) { hist_m->GetYaxis()->SetTitle(title.c_str()); };

private:
	TH1* hist_m;
	
	std::string histname_m;
	int n_bins_m;
	double x_low_m;
	double x_high_m;
};

#endif
