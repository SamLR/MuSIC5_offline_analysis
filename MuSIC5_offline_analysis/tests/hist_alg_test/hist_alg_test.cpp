// To test the tfile_export_algorithm class

#include "../../include/hist_QDC_channel.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"

#include "TFile.h"

int main() {
	TFile* file = new TFile("test.root", "RECREATE");
	std::string histname = "QDC_ch1";
	hist_QDC_channel test(file, histname, 100, 0, 200);
	
	test.set_title("Title");
	test.set_x_axis_title("x.axis");
	test.set_y_axis_title("y.axis");
	
	// Create some mock branches
	QDC_branch q;	
	for (int i = 0; i < 4; i++) {
		q.channel[i] = i;
		q.qdc[i] = 22*i;
	}
	TDC_branch t;	
	for (int i = 0; i < 4; i++) {
		t.channel[i] = i;
		t.n_hits[i] = 5;
		for (int j = 0; j < t.n_hits[i]; j++) {
			t.tdc[j][i] = i + 100*j;
		}
	}
	
	QDC_branch q2;	
	for (int i = 0; i < 4; i++) {
		q2.channel[i] = i;
		q2.qdc[i] = 125*i;
	}
	TDC_branch t2;	
	for (int i = 0; i < 4; i++) {
		t2.channel[i] = i;
		t2.n_hits[i] = 10;
		for (int j = 0; j < t2.n_hits[i]; j++) {
			t2.tdc[j][i] = i + 100*j;
		}
	}
	
	midus_entry* mid = new midus_entry(t, q);
	midus_entry* mid2 = new midus_entry(t2, q2);
	test.process(mid);
	test.process(mid2);
	return 0;
}
