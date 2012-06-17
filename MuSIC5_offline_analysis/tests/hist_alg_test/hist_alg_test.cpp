// To test the tfile_export_algorithm class

#include <iostream>

#include "../../include/hist_branch_channel.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/smart_tfile.h"

#include "TFile.h"

int main() {
	smart_tfile* file = smart_tfile::getTFile("test.root", "RECREATE");
	
	hist_branch_channel* adc_U1_hist = new hist_branch_channel(file, "U1.ADC", adc_ch_U1, branch_adc);
	hist_branch_channel* adc_U2_hist = new hist_branch_channel(file, "U2.ADC", adc_ch_U2, branch_adc);
	hist_branch_channel* tdc0_hist = new hist_branch_channel(file, "TDC0", 0, branch_T0, 200, 0, 3000);
	hist_branch_channel* tdc1_hist = new hist_branch_channel(file, "TDC1", 0, branch_TDC1);
	hist_branch_channel* tdc2_hist = new hist_branch_channel(file, "TDC2", 0, branch_TDC2);
	
	// Create some mock events
	midus_out_branch tr1 [n_branches_in_trigger_tree]; // 0 = ADC, 1 = PHADC, 2 = T0, 3 = TDC1, 4 = TDC2
	tr1[branch_adc].n_entries = 2; // ADC (2 channels - U1 U2)
	tr1[branch_phadc].n_entries = 0; // PHADC
	tr1[branch_T0].n_entries = 1; // TDC0 (T0 - 1 entry (time when event triggered))
	tr1[branch_TDC1].n_entries = 5; // TDC1 (channel U1)
	tr1[branch_TDC2].n_entries = 10; // TDC2 (channel U2)
	for (int i = 0; i < tr1[branch_adc].n_entries; i++) {
		tr1[branch_adc].data[i] = i + 1;
	}
	tr1[branch_T0].data[0] = 1000;
	for (int i = 0; i < tr1[branch_TDC1].n_entries; i++) {
		tr1[branch_TDC1].data[i] = i*4 + 1;
	}
	for (int i = 0; i < tr1[branch_TDC2].n_entries; i++) {
		tr1[branch_TDC2].data[i] = i*10 + 1;
	}
	
	midus_out_branch tr2 [n_branches_in_trigger_tree]; // 0 = ADC, 1 = PHADC, 2 = T0, 3 = TDC1, 4 = TDC2
	tr2[branch_adc].n_entries = 2; // ADC (2 channels - U1 U2)
	tr2[branch_phadc].n_entries = 0; // PHADC
	tr2[branch_T0].n_entries = 1; // TDC0 (T0 - 1 entry (time when event triggered))
	tr2[branch_TDC1].n_entries = 15; // TDC1 (channel U1)
	tr2[branch_TDC2].n_entries = 20; // TDC2 (channel U2)
	for (int i = 0; i < tr2[branch_adc].n_entries; i++) {
		tr2[branch_adc].data[i] = i + 1;
	}
	tr2[branch_T0].data[0] = 2000;
	for (int i = 0; i < tr2[branch_TDC1].n_entries; i++) {
		tr2[branch_TDC1].data[i] = i*3 + 1;
	}
	for (int i = 0; i < tr2[branch_TDC2].n_entries; i++) {
		tr2[branch_TDC2].data[i] = i*20 + 1;
	}
	
	midus_entry* event = new midus_entry(tr1);
	midus_entry* event2 = new midus_entry(tr2);
	
	adc_U1_hist->process(event);
	adc_U1_hist->process(event2);
	adc_U2_hist->process(event);
	adc_U2_hist->process(event2);
	tdc0_hist->process(event);
	tdc0_hist->process(event2);
	tdc1_hist->process(event);
	tdc1_hist->process(event2);
	tdc2_hist->process(event);
	tdc2_hist->process(event2);
	
	file->close();
	return 0;
}
