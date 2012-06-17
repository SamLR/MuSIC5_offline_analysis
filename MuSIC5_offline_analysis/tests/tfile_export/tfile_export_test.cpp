// To test the tfile_export_algorithm class

#include "../../include/tfile_converter_algorithm.h"
#include "../../include/midus_entry.h"
#include "../../include/midus_tree_structs.h"
#include "../../include/smart_tfile.h"

int main() {
	smart_tfile* file = smart_tfile::getTFile("test.root", "RECREATE");
	tfile_converter_algorithm test(file);
	
	// Create some mock branches
	midus_out_branch tr1, tr2;
	for (int i = 0; i < n_branches_in_trigger_tree; i++) {
		tr1.n_entries = i;
		tr1.data[i] = 33*i;
		
		tr2.n_entries = i;
		tr2.data[i] = 33*i + 10;
	}
	
    midus_out_branch b []= {tr1, tr2};
    
	midus_entry* mid = new midus_entry(b);
	test.process(mid);
	
	file->close();
	return 0;
}
