// To test the tfile_export_algorithm class

#include "../../include/hist_QDC_channel.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/smart_tfile.h"

#include "TFile.h"

int main() {
	smart_tfile* file;
	file->getTFile("test.root", "RECREATE");
	hist_QDC_channel channel2(file, "QDC_ch2", 2, 100, 0, 200);
	hist_QDC_channel channel3(file, "QDC_ch3", 3, 100, 0, 200);
	
	channel2.set_title("QDC.ch2");
	channel2.set_x_axis_title("x.axis");
	channel2.set_y_axis_title("y.axis");
	
	channel3.set_title("QDC.ch3");
	channel3.set_x_axis_title("x.axis");
	channel3.set_y_axis_title("y.axis");
	
	// Create some mock branches
	trigger_branch tr1;
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
	channel2.process(mid);
	channel2.process(mid2);
	channel3.process(mid);
	channel3.process(mid2);
	
	return 0;
}
