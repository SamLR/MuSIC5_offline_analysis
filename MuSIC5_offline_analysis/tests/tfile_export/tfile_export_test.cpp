// To test the tfile_export_algorithm class

#include "../../include/tfile_converter_algorithm.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"
//#include "../../include/smart_tfile.h"

int main() {
	TFile* file = new TFile("test.root", "RECREATE");
	tfile_converter_algorithm test(file);
	
	// Create some mock branches
	midus_out_branch tr1 [2]; // 0 = ADC, 1 = TDC0
	tr1[0].n_entries = 1;
	tr1[1].n_entries = 10;
	for (int i = 0; i < tr1[0].n_entries; i++) {
		tr1[0].data[i] = i*3 + 1;
	}	
	for (int i = 0; i < tr1[1].n_entries; i++) {
		tr1[1].data[i] = i*4 + 1;
	}
	
	midus_entry* mid = new midus_entry(tr1); // an event
	test.process(mid);
	
	return 0;
}
