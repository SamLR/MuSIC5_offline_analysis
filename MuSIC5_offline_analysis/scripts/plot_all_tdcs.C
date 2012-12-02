#include <stdio.h>
#include "TROOT.h"
#include "TString.h"
#include "TTree.h"
#include "TH1D.h"
#include "TFile.h"
#include "TCanvas.h"

struct branch{
    int ADC;
    int TDC0;
    int nHITS;
    int TDC[500];
};

TH1D* make_hist (const TString ch_name, const TString file_root);
void _plot_all_tdcs(const TString file_root);

void plot_all_tdcs() {
    const int n_files = 6;
    const TString file_roots [n_files] = {"448","451","452","455","458","459"};
    for(int file = 0; file < n_files; ++file) {
        _plot_all_tdcs(file_roots[file]);
    }
}


void _plot_all_tdcs(const TString file_root) {
    const TString file_prefix = "../../../converted_data/run00";
    const TString file_suffix = "_converted.root";
    const int n_ch = 5;
    const TString ch [n_ch] = {"D1", "D2", "D3", "D4", "D5"};
    
    const TString file_name = file_prefix + file_root + file_suffix;
    TFile* in_file = new TFile(file_name, "READ");
    TTree* in_tree = (TTree*) in_file->Get("Trigger");
    TH1D* hists [n_ch];
    
    for(int ch_id = 0; ch_id < n_ch; ++ch_id) {
        hists[ch_id] = make_hist(file_root, ch[ch_id]);
        branch ch_branch;
        in_tree->SetBranchAddress(ch[ch_id], &ch_branch);
        const int n_entries = in_tree->GetEntries();
        
        for(int entry = 0; entry < n_entries; ++entry) {
            in_tree->GetEntry(entry);
            
            for(int hit = 0; hit < ch_branch.nHITS; ++hit) {
                hists[ch_id]->Fill(ch_branch.TDC[hit]);
            }
        }
    }
    
    TCanvas* can = new TCanvas(file_root, file_root, 1200, 786);
    can->Divide(3,2);
    for(int ch_id = 0; ch_id < n_ch; ++ch_id) {
        can->cd(ch_id+1);
        hists[ch_id]->Draw();
    }
    const TString save_location = TString("images/raw_tdc_")+file_root;
    can->SaveAs(save_location+".svg");
    can->SaveAs(save_location+".eps");
    // in_file->Close();
    // delete in_file;
}


TH1D* make_hist (const TString ch_name, const TString file_root) {
    const TString name = TString("TDC_file_")+file_root+TString("_ch_")+ch_name;
    TH1D* hist = new TH1D(name, name, 2000, -20000, 20000);
    hist->GetXaxis()->SetTitle("Time (ns)");
    hist->GetYaxis()->SetTitle("Count");
    return hist;
}