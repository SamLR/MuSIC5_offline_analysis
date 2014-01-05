#include "TFile.h"
#include "TF1.h"

const float l_bound = 50.0;
const float u_bound = 20000.0;

void count_vs_integrals(){
    const int n_files = 4;
    const char prefix [] = "hist_files_offset/degrader_";
    const char suffix [] = "_hists.root";
    const char files [n_files][20] = {
        "0.5mm_Aluminium",
        "1mm_Aluminium",
        "5mm_Aluminium",
        "5mm_Air"
    };
    
    const char hist_name_prefix = "combined_";
    
}


TF1* getFitFunction(const float n_cu_init, const float n_f_init){
    static int call_counter = 0; // make sure each function is unique
    
    const float tau_cu [3] = { 163.5   ,  162.5   ,  164.5};
    const float tau_f  [3] = {2196.9811, 2196.9789, 2196.9833};
    
    char name [5];
    sprintf(name, "fit%d", call_counter++);
    printf("%s\n", name);
    TF1* func = new TF1(name, "[0]*exp(-x/[1]) + [2]*exp(-x/[3])", l_bound, u_bound);

    func->SetParName(0, "N_{cu}");
    func->SetParameter(0, n_cu_init);
    
    func->SetParName(1, "#tau_{cu}");
    func->SetParameter(1, tau_cu[0]);
    func->SetParLimits(1, tau_cu[1], tau_cu[1]);

    func->SetParName(0, "N_{f}");
    func->SetParameter(0, n_f_init);
    
    func->SetParName(1, "#tau_{f}");
    func->SetParameter(1, tau_f[0]);
    func->SetParLimits(1, tau_f[1], tau_f[1]);
    
    return func;
}

