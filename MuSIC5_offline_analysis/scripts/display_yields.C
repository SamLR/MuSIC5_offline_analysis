void display_yields() {
    const int n = 6;
    const float x[n]    = {0.0, 0.5, 0.5, 1.0, 5.0, 5.0};
    const float x_er[n] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    const float y[n]    = {6.160, 7.301, 7.767, 8.012, 8.524, 8.899};
    const float y_er[n] = {0.02, 0.07, 0.04,  0.03,  0.04, 0.06};
    
    TGraphErrors* graph = new TGraphErrors(n,x,y,x_er,y_er);
    const TString name = "Muon yields for 1#muA proton current";
    graph->SetTitle(name);
    graph->GetXaxis()->SetLimits(-1.0,6.0);
    
    const TString x_name = "Aluminium degrader thickness (mm)";
    const TString y_name = "Yield (x10^{7}muons/s)";
    
    graph->GetXaxis()->SetTitle(x_name);
    graph->GetYaxis()->SetTitle(y_name);
    graph->Draw("AP");
}


