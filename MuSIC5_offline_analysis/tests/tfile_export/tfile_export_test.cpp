// To test the tfile_export_algorithm class

#include "../../include/tfile_converter_algorithm.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/smart_tfile.h"

#include "TFile.h"

int main() {
	smart_tfile* file;
	file->getTFile("test.root", "RECREATE");
	tfile_converter_algorithm test(file);
	
	// Create some mock branches
	midus_out_branch tr1 [2]; // 0 = ADC, 1 = TDC
	tr1[0].n_entries = 1;
	tr1[1].n_entries = 10;
	for (int i = 0; i < tr1[0].n_entries; i++) {
		tr1[0].data[i] = i*3 + 1;
	}	
	for (int i = 0; i < tr1[1].n_entries; i++) {
		tr1[1].data[i] = i*4 + 1;
	}
	
	midus_out_branch tr2[2]; // 0 = ADC, 1 = TDC
	tr2[0].n_entries = 1;
	tr2[1].n_entries = 20;
	for (int i = 0; i < tr2[0].n_entries; i++) {
		tr2[0].data[i] = i*5 + 1;
	}	
	for (int i = 0; i < tr2[1].n_entries; i++) {
		tr2[1].data[i] = i*7 + 1;
	}
	
	midus_entry* U1 = new midus_entry(tr1); // a channel
	midus_entry* U2 = new midus_entry(tr2); // a channel
	test.process(U1);
	test.process(U2);
	
	return 0;
}
