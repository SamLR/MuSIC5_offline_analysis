#include "drawing.C"
#include "TFile.h"
#include "TTree.h"
#include "TROOT.h"
#include "TH1F.h"
#include "TF1.h"
#include "TCanvas.h"


void example_fits()
{
    TFile* sim_file = new TFile("inclusive_dt_hists.root", "READ");
    TFile* dat_file = new TFile("music5_tdc_data.root", "READ");
    TH1F* sim_hist = (TH1F*) sim_file->Get("parent-daughter_dts_for_Aluminium_0.5mm");
    sim_hist->Rebin(50);
    TH1F* dat_hist = (TH1F*) dat_file->Get("file_451_ch_D5");
    dat_hist->Rebin(50);
    TF1*  fit = new TF1("sim_fit", "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])", 50,20000);
    fit->SetParName(0, "N_{b}")
    fit->SetParameter(0, param_val)
    // TF1*  dat_fit = new TF1("dat_fit", "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])", 50,20000);
    sim_hist->Fit(fit);
    dat_hist->Fit(fit);
    
    TCanvas* can = new TCanvas("c1", "c1", 1436,856);
    can->Divide(2,1);
    
    can->cd(1);
    sim_hist->SetTitle("Simulated TDC data for 0.5mm Al");
    sim_hist->GetXaxis()->SetTitle("Time (ns)");
    sim_hist->GetYaxis()->SetTitle("Count");
    sim_hist->Draw();
    can->cd(2);
    dat_hist->SetTitle("TDC data for 0.5mm Al");
    dat_hist->GetXaxis()->SetTitle("Time (ns)");
    dat_hist->GetYaxis()->SetTitle("Count");
    dat_hist->Draw();

    
}