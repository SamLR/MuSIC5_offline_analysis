//
// Draw all the fitted TDC plots for all the converted root files in a directory
// Each file will have its own canvas split into 16 
// 

#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TF1.h"

void draw_fitted_TDCs() {
 
} 

void list_files(const char *dirname, const char *ext="_mu_analysis.root") {
    TSystemDirectory dir(dirname, dirname);
    TList *files = dir.GetListOfFiles();
    if (files) {
       TSystemFile *file;
       TString fname;
       TIter next(files);
       while ((file=(TSystemFile*)next())) {
          fname = file->GetName();
          if (!file->IsDirectory() && fname.EndsWith(ext)) {
             cout << fname.Data() << endl;
          }
       }
    }
 }