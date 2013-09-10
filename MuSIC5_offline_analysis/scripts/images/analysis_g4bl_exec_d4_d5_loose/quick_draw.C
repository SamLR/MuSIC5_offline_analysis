#include "TCanvas.h"
#include "TFile.h"
#include "TH1D.h"

void quick_draw(){
  TFile* file = new TFile("out.root","READ");
  char* file_ids [6] = {"448", "451", "452", "455", "458", "459"};
  TCanvas* cans [6];
  for(int id = 0; id < 6; ++id) {
    char can_name [10];
    sprintf(can_name, "can_%s", file_ids[id]);
    cans[id] = new TCanvas(can_name, can_name);
    cans[id]->Divide(3,2);
    for(int i = 1; i < 6; ++i) {
      cans[id]->cd(i);
      char buffer[10];
      sprintf(buffer, "%s_D%d", file_ids[id], i);
      TH1D* hist = (TH1D*) file->Get(buffer);
      hist->Draw();   
    }
  }
}