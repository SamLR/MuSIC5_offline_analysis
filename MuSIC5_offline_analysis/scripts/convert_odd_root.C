// This is a script for converting from the strange format that
// Nam created for some root files into the one used by us. 
// 
// This is not a compilable script and should be run via CINT
// this is because I am lazy
//

#include "TFile.h"
#include "TTree.h"
#include <iostream>

using namespace std;

unsigned int const n_channels = 15; // assigned channels 1:8=u 9:13=D 14:15 = Ge
unsigned int const n_tdc_channels = 16; // assigned channels 1:8=u 9:13=D 14:15 = Ge
TString const channel_names[n_channels] = {"U1", "U2", "U3", "U4", 
	"U5", "U6", "U7", "U8", "D1", "D2", "D3", "D4", "D5", "Ge1", "Ge2"};

struct out_branch {
	int adc;
	int t0;
	int n_hits;
	int tdc[18];
};

void set_branch_address(int phadc[2], int qdc[n_channels + 1], // qdc has channel '0' unused & nulls
	// tdc has channel 0 as trigger
	int nhits[n_channels + 1], double tdc[n_channels + 1][18], TTree* tree); 

void convert_odd_root(){
	TString const in_file_name = "../../../MuSIC_data_0.5Cu/run448.root";
	TString const out_file_name = "../../../converted_data/run00448_converted.root";

	// open up the in file & get the tree
	TFile* in_file = new TFile(in_file_name);
	TTree* in_tree = (TTree*) in_file->Get("t");
	// locations for the input branches to write to
	int in_phadc[2];
	int in_qdc[n_tdc_channels];
	int in_nhits[n_tdc_channels];
	double in_tdc[n_tdc_channels][18];
	// set all the input branchs
	set_branch_address(in_phadc, in_qdc, in_nhits, in_tdc, in_tree);
	
	// set up the output file & tree
	TFile* out_file = new TFile (out_file_name, "RECREATE");
	TTree* out_tree = new TTree("Trigger", "Trigger");
	// a branch (leaves: ADC val, t0, n_hits and tdc) for each channel
	out_branch branches[n_channels];
	TString const leaflist = "ADC/I:TDC0:nHITS:TDC[nHITS]";
	// set all the branches
	for(unsigned int ch = 0; ch < n_channels - 1; ++ch) {
		out_tree->Branch(channel_names[ch], &(branches[ch]), leaflist);
	}
	
	// loop over the entries in the input file and write the results to the output
	unsigned int const n_entries = in_tree->GetEntries();
	for(unsigned int entry = 0; entry < n_entries; ++entry) {
		in_tree->GetEntry(entry);
		if (entry%1000 == 0) cout<<"Entry "<< entry << " of "<< n_entries <<endl;
		// Loop over the OUTPUT channels writing to them from the input channels. 
		// NOTE: Channel 0 (input) is either the trigger time, t0, for tdc
		// 		 readings or not used (but present) for ADC. Output channels
		//		 14 & 15 (numbered from 0) are Ge3 detectors and have ADC values 
		//		 stored the PHADC branch
		for(unsigned int ch = 0; ch < n_channels; ++ch) {
			if (ch < 13) {
				// MPPC counter (either up or down stream)
				branches[ch].adc = in_qdc[ch+1];// index 0 is present but not used
			} else {
				// Ge 1 or 2 (indexes 0 or 1)
				branches[ch].adc = in_phadc[ch-13];
			} 
			branches[ch].t0  = in_tdc[0][0];
			unsigned int n = static_cast<unsigned int>(in_nhits[ch+1]);
			branches[ch].n_hits = static_cast<int>( n );
			// return;
			for(unsigned int hit = 0; hit < n; ++hit) {
				// make sure the tdc data is in a sensible form
				branches[ch].tdc[hit] = static_cast<int>(in_tdc[ch+1][hit]);
			}
			out_tree->Fill();
		}
	}
	out_file->Write();
}



void set_branch_address(int phadc[2], int qdc[n_channels], 
int nhits[n_tdc_channels], double tdc[n_tdc_channels][18], TTree* tree) {
	// set the phadc branch
	tree->SetBranchAddress("V006_PHADC", phadc);
	// the qdc branch
	tree->SetBranchAddress("V792N_QDC", qdc);

	// set each individual channels n_hit branch
	for(unsigned int i = 0; i < n_tdc_channels; ++i) {
		TString hit_branch_name("V1290_TDC_NHITS");
		TString tdc_branch_name("V1290_TDC_TIME");
		hit_branch_name += i;
		tdc_branch_name += i;
		tree->SetBranchAddress(hit_branch_name, &(nhits[i]));
		tree->SetBranchAddress(tdc_branch_name, &(tdc[i][0]));	
	}
}
