// To test the tfile_export_algorithm class

#include "../../include/tfile_converter_algorithm.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/smart_tfile.h"

#include "TFile.h"

int main() {
	smart_tfile* file = smart_tfile::getTFile("test.root", "RECREATE");
	tfile_converter_algorithm* test = new tfile_converter_algorithm(file);
	
	// Create some mock branches
	midus_out_branch tr1 [4]; // 0 = ADC, 1 = TDC0, 2 = TDC1, 3 = TDC2
	tr1[0].n_entries = 2; // ADC (2 channels - U1 U2)
	tr1[1].n_entries = 1; // TDC0 (T0 - 1 entry (time when event triggered))
	tr1[2].n_entries = 5; // TDC1 (channel U1)
	tr1[3].n_entries = 10; // TDC2 (channel U2)
	for (int i = 0; i < tr1[0].n_entries; i++) {
		tr1[0].data[i] = i + 1;
	}
	tr1[1].data[0] = 1000;
	for (int i = 0; i < tr1[2].n_entries; i++) {
		tr1[2].data[i] = i*4 + 1;
	}
	for (int i = 0; i < tr1[3].n_entries; i++) {
		tr1[3].data[i] = i*10 + 1;
	}
	
	midus_entry* event = new midus_entry(tr1); // an event
	test->process(event);
	
	file->close();
	
	return 0;
}
