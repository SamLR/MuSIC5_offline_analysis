void display_yields() {
    const int n = 6;
    const float x[n]    = {0.0, 0.5, 0.5, 1.0, 5.0, 5.0};
    const float x_er[n] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    const float y[n]    = {6.31, 7.50, 8.73, 12.15, 10.91, 17.55};
    const float y_er[n] = {0.02, 0.07, 0.04,  0.05,  0.06,  0.01};
    
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
