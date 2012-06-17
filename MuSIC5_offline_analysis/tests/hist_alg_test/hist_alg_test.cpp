// To test the tfile_export_algorithm class

#include "../../include/hist_branch_channel.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/smart_tfile.h"

#include "TFile.h"

int main() {
	smart_tfile* file = smart_tfile::getTFile("test.root", "RECREATE");
	hist_branch_channel* tdc0_U1_hist = new hist_branch_channel(file, "U1.TDC0", 0, 1, 200, 0, 3000);
	hist_branch_channel* tdc0_U2_hist = new hist_branch_channel(file, "U2.TDC0", 1, 1, 200, 0, 3000);
	
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
	
	midus_out_branch tr2 [4]; // 0 = ADC, 1 = TDC0, 2 = TDC1, 3 = TDC2
	tr2[0].n_entries = 2; // ADC (2 channels - U1 U2)
	tr2[1].n_entries = 1; // TDC0 (T0 - 1 entry (time when event triggered))
	tr2[2].n_entries = 15; // TDC1 (channel U1)
	tr2[3].n_entries = 20; // TDC2 (channel U2)
	for (int i = 0; i < tr2[0].n_entries; i++) {
		tr2[0].data[i] = i + 1;
	}
	tr2[1].data[0] = 2000;
	for (int i = 0; i < tr2[2].n_entries; i++) {
		tr2[2].data[i] = i*3 + 1;
	}
	for (int i = 0; i < tr2[3].n_entries; i++) {
		tr2[3].data[i] = i*20 + 1;
	}
	
	midus_entry* event = new midus_entry(tr1);
	midus_entry* event2 = new midus_entry(tr2);
	
	tdc0_U1_hist->process(event);
	tdc0_U1_hist->process(event2);
	tdc0_U2_hist->process(event);
	tdc0_U2_hist->process(event2);
	
	file->close();
	return 0;
}
