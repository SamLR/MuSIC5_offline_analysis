// To test the tfile_export_algorithm class

#include "../../include/tfile_export_algorithm.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"

#include "TFile.h"

int main() {
	TFile* file = new TFile("test.root", "RECREATE");
	tfile_export_algorithm test(file);
	
	QDC_branch q;
	TDC_branch t;
	
	midus_entry* mid = new midus_entry(t, q);;
	test.process(mid);
	return 0;
}
