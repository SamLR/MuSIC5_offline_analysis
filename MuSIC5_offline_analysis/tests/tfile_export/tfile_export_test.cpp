// To test the tfile_export_algorithm class

#include "../../include/tfile_converter_algorithm.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/smart_tfile.h"

int main() {
	smart_tfile* file;
	file->getTFile("test.root", "RECREATE");
	tfile_converter_algorithm test(file);
	
	// Create some mock branches
	trigger_branch tr1, tr2;
	for (int i = 0; i < MAX_TDC_HITS; i++) {
		tr1.n_tdc[i] = i;
		tr1.tdc0[i] = 22*i;
		
		tr2.n_tdc[i] = i;
		tr2.tdc0[i] = 22*i + 10;
	}
	for (int i = 0; i < QDC_CH; i++) {
		tr1.n_qdc[i] = i;
		tr1.qdc0[i] = 33*i;
		
		tr2.n_qdc[i] = i;
		tr2.qdc0[i] = 33*i + 10;
	}
	
	midus_entry* mid = new midus_entry(tr1);
	midus_entry* mid2 = new midus_entry(tr2);
	test.process(mid);
	test.process(mid2);
	
	file->Write();
	file->Close();
	return 0;
}
