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

unsigned int const n_channels = 15;     // assigned channels 1:8=u 9:13=D 14:15 = Ge
unsigned int const n_tdc_channels = 13; // assigned channels 1:8=u 9:13=D 14:15 = Ge
TString const channel_names[n_channels] = {"U1", "U2", "U3", "U4", 
	"U5", "U6", "U7", "U8", "D1", "D2", "D3", "D4", "D5"};

struct out_branch {
	int adc;
	int t0;
	int n_hits;
	int tdc[18];
};

struct in_tdc_branch {
    int nTDC;
    int TDC[10000];
};
struct in_adc_branch {
    int nADC;
    int ADC[10000];
};


void convert_Mg_root(){
    // TString const in_file_name = "../../../MuSIC_data_0.5Cu/run448.root";
	char const in_file_fmt [] = "../../../MuSIC_data_Mg/run00%i.root";
    // TString const out_file_name = "../../../converted_data/run00448_converted.root";
	char const out_file_fmt [] = "../../../converted_Mg_data/run00%i_converted.root";

    int const n_files = 4;
    int const file_ids [n_files] = {464, 466, 468, 508};
    
    for(int file_n = 0; file_n < n_files; ++file_n) {
        // Generate the in and out file names
        char in_file_name [42];
        sprintf(in_file_name, in_file_fmt, file_ids[file_n]);
        printf("%s\n",in_file_name);
        char out_file_name [56];
        sprintf(out_file_name, out_file_fmt, file_ids[file_n]);
        printf("%s\n",out_file_name);
            
    	// open up the in file & get the tree
    	TFile* in_file = new TFile(in_file_name, "READ");
    	TTree* in_tree = (TTree*) in_file->Get("t");
    	// locations for the input branches to write to
        in_tdc_branch in_tdc;
        in_adc_branch in_adc;
        in_tree->SetBranchAddress("TDC0", &in_tdc);
        in_tree->SetBranchAddress("QDC",  &in_adc);
        
	
    	// set up the output file & tree
    	TFile* out_file = new TFile (out_file_name, "RECREATE");
    	TTree* out_tree = new TTree("Trigger", "Trigger");
    	// a branch (leaves: ADC val, t0, n_hits and tdc) for each channel
    	out_branch branches[n_channels];
    	TString const leaflist = "ADC/I:TDC0:nHITS:TDC[nHITS]";
    	// set all the branches
    	for(unsigned int ch = 0; ch < n_channels; ++ch) {
    		out_tree->Branch(channel_names[ch], &(branches[ch]), leaflist);
    	}
	
    	// loop over the entries in the input file and write the results to the output
    	unsigned int const n_entries = in_tree->GetEntries();
    	cout << n_entries << " entries found, looping"<< endl;
    	for(unsigned int entry = 0; entry < n_entries; ++entry) {
    		in_tree->GetEntry(entry);
    		if (entry%1000 == 0) cout<<"Entry "<< entry << " of "<< n_entries <<endl;
            
            for(int adc_ch = 0; adc_ch < in_adc.nADC; ++adc_ch) {
                int ch = (in_adc[adc_ch] & 0x0001f0000);
                if (ch==0 || ch > 13) continue;
				branches[ch].adc = (in_adc[adc_ch] & 0x00000fff);
            }    
            
            for(int ch = 0; ch < n_channels; ++ch) {
                // set tdc0 for all channels
    			branches[ch].t0  = in_tdc.TDC[0];
            }    
            int n_hits[n_channels];
        
			for(int hit = 0; hit < in_tdc.nTDC; ++hit) {
                // Now convert all the TDC data
                // branches[ch].tdc[hit] = static_cast<int>(in_tdc[ch+1][hit] - in_tdc[0][0]);
			}
            
            for(int ch = 0; ch < n_channels; ++ch) {
                branches[ch].n_hits = n_hits[ch]
            }
    		out_tree->Fill();
    	}
    	out_file->Write();
        out_file->Close();
        in_file->Close();
        
    }
}

