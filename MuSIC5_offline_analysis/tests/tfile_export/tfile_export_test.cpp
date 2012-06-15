// To test the tfile_export_algorithm class

#include "../../include/tfile_export_algorithm.h"

#include "TFile.h"

int main() {
	TFile* file = new TFile("test.root", "RECREATE");
	tfile_export_algorithm test(file);
	return 0;
}
