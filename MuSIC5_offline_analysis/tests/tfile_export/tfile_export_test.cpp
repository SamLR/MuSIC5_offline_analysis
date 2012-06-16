// To test the tfile_export_algorithm class

#include "../../include/tfile_converter_algorithm.h"
#include "../../include/midus_entry.h"
#include "../../include/counter_struct.h"
#include "../../include/smart_tfile.h"

int main() {
	smart_tfile* file;
	file->getTFile("test.root", "RECREATE");
	tfile_converter_algorithm test(file);
	
	// Create some mock branches
	counter_struct tr1;
	tr1.n_hits = 10;
	tr1.data = 211;
	for (int i = 0; i < n_hits; i++) {
		tr1.tdc[i] = i*3;
	}	
	
	midus_entry* mid = new midus_entry(tr1);
	test.process(mid);
	
	return 0;
}
