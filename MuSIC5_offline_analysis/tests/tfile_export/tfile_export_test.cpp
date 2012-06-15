// To test the tfile_export_algorithm class

#include "../../include/tfile_converter_algorithm.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"

#include "TFile.h"

int main() {
	TFile* file = new TFile("test.root", "RECREATE");
	tfile_converter_algorithm test(file);
	
	// Create some moch branches
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
	
	midus_entry* mid = new midus_entry(t, q);
	test.process(mid);
	return 0;
}
