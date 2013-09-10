#include "TCanvas.h"
#include "TFile.h"
#include "TH1D.h"
#include "TPaveStats.h"
#include "TVirtualPad.h"

void prettify(TVirtualPad* pad, TH1D* hist){
  hist->GetYaxis()->SetTitleOffset(1.3);
  pad->Update();
  TPaveStats *st = (TPaveStats*)hist->FindObject("stats");
  st->SetTextFont(42);
  st->SetX1NDC(0.55);
  st->SetX2NDC(0.90);
  st->SetY1NDC(0.55);
  st->SetY2NDC(0.90);
  pad->Update();
}

void quick_draw(){
  TFile* file = new TFile("out.root","READ");
  char* file_ids [6] = {"448", "451", "452", "455", "458", "459"};
  TCanvas* cans [6];
  for(int id = 0; id < 6; ++id) {
    char can_name [10];
    sprintf(can_name, "can_%s", file_ids[id]);
    // Make it full screen
    cans[id] = new TCanvas(can_name, can_name, 1436,856);
    cans[id]->Divide(3,2);
    for(int i = 1; i < 6; ++i) {
      TVirtualPad* pad = cans[id]->cd(i);
      char buffer[10];
      sprintf(buffer, "%s_D%d", file_ids[id], i);
      TH1D* hist = (TH1D*) file->Get(buffer);
      hist->Draw();
      prettify(pad, hist);
    }
    char img_name [10];
    sprintf(img_name,"%s.svg", file_ids[id]);
    cans[id]->SaveAs(img_name);
    sprintf(img_name,"%s.eps", file_ids[id]);
    cans[id]->SaveAs(img_name);
  }
  
  char* sim_ids[4] = {"5mm_Air_combined_5mm_Air",
                      "1mm_Aluminium_combined_1mm_Aluminium",
                      "5mm_Aluminium_combined_5mm_Aluminium",
                      "0.5mm_Aluminium_combined_0.5mm_Aluminium"};
  TCanvas* sim_can = new TCanvas("sim_can", "sim_can", 1436,856);
  sim_can->Divide(2,2);
  for (int id = 0; id < 4; ++id) {
    TVirtualPad* pad = sim_can->cd(id+1);
    TH1D* hist = (TH1D*) file->Get(sim_ids[id]);
    hist->Draw();
    prettify(pad, hist);
  }
  sim_can->SaveAs("all_sim.svg");
  sim_can->SaveAs("all_sim.eps");
}