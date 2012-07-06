TString const* create_file_name(TString const&, TString const&, int const&);
TH1F* create_histogram(int const, TString const&);
TF1* create_function(int const, TString const&);
void get_component_funcs(TF1*, TF1*&, TF1*&, TF1*&);

void set_up(){
	gSystem->SetIncludePath("-I. -I../include -I$ROOTSYS/include");
	gROOT->ProcessLine(".L ../src/midus_structure.cpp+");
	gROOT->ProcessLine(".L ../src/root_functions.cpp+");
	gStyle->SetOptFit();
}

void muon_count(){
	// bool const testing = true;
	bool const testing = false;
	set_up();
	// list tfiles & thicknesses
	// for each file
	//		open file
	//		create tree
	//		choose specific channel?
	//		fill histogram with TDC data
	// 		fit histogram data
	//		plot hist & save
	//		extract parameters & get integral of exp paramets
	//		close tree & file
	// plot thickness Vs integral of fits

	TString const file_prefix = "../../../converted_data/run00";
	TString const file_suffix = "_converted.root";

	int const n_files = 6;
	int const n_ch = 15;
	int const file_ids[n_files] = {448,451,452,455,458,459};
	float const thicknesses[n_files] = {0, 0.5, 0.5, 1, 5, 5}; // degrader thicknesses in mm Al

	// where to save the output
	TFile* out_file = new TFile ("out_muon_count.root", "RECREATE");
	TCanvas* canvases[n_files];
	TH1F* tdc_hists [n_files][n_ch];
	TH1F* all_muon_hists [n_ch]; 
	// TH1F* fast_muon_hists [n_ch]; 
	// TH1F* slow_muon_hists [n_ch];

	TF1* fit_fns [n_files][n_ch];
	TF1* comb_muons_fns [n_files][n_ch];
	TF1* fast_muons_fns [n_files][n_ch];
	TF1* slow_muons_fns [n_files][n_ch];

	for(unsigned int ch = 0; ch < n_ch; ++ch) {
		TString name("muons_Vs_degrader_channel:");
		name += midus_structure::tdc_names[ch+1];
		// all_muon_hists[ch] = new TH2F(name,name,12, -0.25, 5.75, 2000, 0, 10000);
		all_muon_hists[ch] = new TH1F(name,name,6, -0.5, 5.5);
	}


	for(unsigned int f_id = 0; f_id < n_files; ++f_id) {
		// open the file
		TString const* file_name = create_file_name(file_prefix, file_suffix, file_ids[f_id]);
		std::cout << (*file_name) << std::endl;
		TFile* in_file = new TFile((*file_name), "READ");
		TTree* in_tree = (TTree*) in_file->Get("Trigger");
		in_branch branches[n_ch];
		set_branch_addresses(branches, in_tree);

		// create the histograms and make sure they're saved to the outfile
		out_file->cd();
		for(unsigned int ch = 0; ch < n_ch; ++ch) {
			tdc_hists[f_id][ch] = create_histogram(thicknesses[f_id], file_ids[f_id], branches[ch].branchname);
			fit_fns[f_id][ch] = create_function(file_ids[f_id], branches[ch].branchname);
		}
		
		// unsigned int const n_entries = in_tree->GetEntries();
		unsigned int const n_entries = (testing) ? 10000:in_tree->GetEntries();
		
		for(unsigned int entry = 0; entry < n_entries; ++entry) {
			in_tree->GetEntry(entry);
			if (entry%10000==0) cout <<entry<<" entry of "<<n_entries<<endl;
			for(unsigned int ch = 0; ch < n_ch; ++ch) {
				int n_hits = branches[ch].in_channel.n_tdc_hits;
				for(unsigned int hit = 0; hit < n_hits; ++hit) {
					tdc_hists[f_id][ch]->Fill(branches[ch].in_channel.tdc[hit]);
				}
			}
		}

		out_file->cd();
		TString* can_name = new TString("run00"); 
		(*can_name) += file_ids[f_id];
		canvases[f_id] = new TCanvas((*can_name), (*can_name), 1436,856);
		canvases[f_id]->Divide(4,4); 
								// Draw it
		for(unsigned int ch = 0; ch < n_ch; ++ch) {
			canvases[f_id]->cd(ch+1);
			tdc_hists[f_id][ch]->Draw();
			tdc_hists[f_id][ch]->Fit(fit_fns[f_id][ch], "RQ");
			get_component_funcs(fit_fns[f_id][ch], comb_muons_fns[f_id][ch],
				fast_muons_fns[f_id][ch], slow_muons_fns[f_id][ch]);
			double const weight = comb_muons_fns[f_id][ch]->Integral(0,20000)/n_entries;
			cout << weight << endl;
			all_muon_hists[ch]->Fill(f_id, weight);
			// all_muon_hists[ch]->Fill(thicknesses[f_id], weight);
			TString save_file(*can_name);
			// save_file += ".eps";
			save_file = "images/"+save_file+ ".eps";
			if(!testing) canvases[f_id]->SaveAs(save_file);
		}

		delete can_name;
		delete file_name;
		delete in_tree;
		delete in_file;
	}	
	TCanvas* can_final[n_ch];
	for(unsigned int ch = 0; ch < n_ch; ++ch) {
		TString f_can_name ("mu_vs_z_");
		f_can_name += ch;
		can_final[ch] =  new TCanvas(f_can_name,f_can_name, 1436,856);
		all_muon_hists[ch]->Draw();
		for(unsigned int f_id = 0; f_id < n_files; ++f_id) {
			TString binname("");
			binname+=thicknesses[f_id];
			all_muon_hists[ch]->GetXaxis()->SetBinLabel(f_id+1, binname);
		}
//		f_can_name += ".eps";
		f_can_name = "images/"+f_can_name + ".eps";
		if(!testing) can_final[ch]->SaveAs(f_can_name);
	}	
	out_file->Write();
}


TString const* create_file_name(TString const& prefix, TString const& suffix, int const& id){
	TString* res = new TString(prefix);
	(*res) += id;
	(*res) += suffix;
	return res;
}

TH1F* create_histogram(int const deg_thickness, int const file_id, TString const& channel){
	TString name(channel);
	name += "_run00";
	name += file_id;
	TString title("TDC for ");
	name += deg_thickness;
	name += ("mm Aluminium degrader. Channel: " + channel);

	TH1F* res = new TH1F(name, title, 500, 0, 20000);
	res->GetXaxis()->SetTitle("Time (ns)");
	res->GetYaxis()->SetTitle("Count");
	return res;
}

void get_component_funcs(TF1* in_func, TF1*& comb, TF1*& fast, TF1*& slow) {
	double param[5];
	in_func->GetParameters(param);
	TString name = in_func->GetName();
	comb = new TF1((name+"_comb"), "[0]*exp(-x/[1]) + [2]*exp(-x/[3])",100, 20000);
	comb->FixParameter(0, param[1]);
	comb->FixParameter(1, param[2]);
	comb->FixParameter(2, param[3]);
	comb->FixParameter(3, param[4]);

	fast = new TF1((name+"_fast"), "[0]*exp(-x/[1])",100, 20000);
	fast->FixParameter(0, param[1]);
	fast->FixParameter(1, param[2]);

	slow = new TF1((name+"_slow"), "[0]*exp(-x/[1])",100, 20000);
	slow->FixParameter(0, param[3]);
	slow->FixParameter(1, param[4]);
}

TF1* create_function(int const run_id, TString const& channel) {
	TString name(channel);
	name += "_run00";
	name += run_id;

	TF1* res = new TF1(name, "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])", 60, 20000);
	// give all scalers a default value
	res->SetParameter(0, 200);
	res->SetParameter(1, 100);
	res->SetParameter(3,  50);
	// µ- decay time in copper
	res->SetParameter(2, 160); // this is a known value
	// free muon decay time and decay time in scintillator
	res->SetParameter(4, 2000);
	// set the parameter names
	res->SetParName(0, "N_{B}");
	res->SetParName(1, "N_{#mu^{-}}");
	res->SetParName(2, "#tau_{Cu}");
	res->SetParName(3, "N_{#mu^{+}}");
	res->SetParName(4, "#tau_{#mu}");

	return res;
}
// 
// TF1* create_function(int const run_id, TString const& channel) {
// 	TString name(channel);
// 	name += "_run00";
// 	name += run_id;
// 
// 	TF1* res = new TF1(name, "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])",100, 20000);
// 	res->SetParName(0, "N_{B}");
// 	res->SetParName(1, "N_{#mu^{-}}");
// 	res->SetParName(2, "#tau_{Cu}");
// 	res->SetParameter(2, 100);
// 	res->SetParName(3, "N_{#mu^{+}}");
// 	res->SetParName(4, "#tau_{#mu}");
// 	res->SetParameter(4, 1000);
// 
// 	return res;
// }

