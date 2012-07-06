

void quick_tdc(){
	gSystem->SetIncludePath("-I. -I../include -I$ROOTSYS/include");
	gROOT->ProcessLine(".L ../src/midus_structure.cpp+");
	gROOT->ProcessLine(".L ../src/root_functions.cpp+");
	gStyle->SetOptFit();
	
	TFile* in_file = new TFile("../../../converted_data/run00455_converted.root","READ");
	TTree* in_tree = (TTree*) in_file->Get("Trigger");
	in_branch branches[15];
	set_branch_addresses(branches, in_tree);
	TString name ("TDC hits in channel D5 for 1mm Al degrader & 0.5 Cu target");
	TString title ("TDC");
	TH1F* hist = new TH1F(title, name, 200, 0, 20000);
	hist->GetXaxis()->SetTitle("Time(ns)");
	hist->GetYaxis()->SetTitle("Count");
	
	int const channel = 12;
	int const n_entries = in_tree->GetEntries();
	int const tenth = n_entries/10;
	cout << "Starting" << endl;
	for(unsigned int entry = 0; entry < n_entries; ++entry) {
		in_tree->GetEntry(entry);
		if(entry % (tenth) == 0) cout << "=";

		int const n_hits = branches[channel].in_channel.n_tdc_hits;
		for(unsigned int hit = 0; hit < n_hits; ++hit) {
			hist->Fill(branches[channel].in_channel.tdc[hit]);
		}

	}
	cout <<endl << "Done"<<endl;
	hist->Draw();
	TF1* fit_fn = new TF1("fit", "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])",60, 20000);
	fit_fn->SetParName(0, "N_{B}");
	fit_fn->SetParName(1, "N_{#mu^{-}}");
	fit_fn->SetParName(2, "#tau_{Cu}");
	fit_fn->SetParameter(2, 160);
	fit_fn->SetParName(3, "N_{#mu^{+}}");
	fit_fn->SetParName(4, "#tau_{#mu}");
	fit_fn->SetParameter(4, 2000);
	hist->Fit(fit_fn, "R");
	
	
}