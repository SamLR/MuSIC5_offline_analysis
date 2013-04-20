#include "TH1F.h"
#include "TCanvas.h"
#include "TROOT.h"
#include "TPaveStats.h"
#include "TLegend.h"

void edit_stats_box(TCanvas* can, const TH1* hist, const int options=1002201,
    const double x1 = 0.55, const double x2 = 0.70, 
    const double y1 = 0.10, const double y2 = 0.37
){
    can->Update(); // required to get access to the stats box
    TPaveStats* stats_box = (TPaveStats*) hist->FindObject("stats");
    stats_box->SetOptStat(options);
    stats_box->SetX1NDC(x1);
    stats_box->SetX2NDC(x2);
    stats_box->SetY1NDC(y1);
    stats_box->SetY2NDC(y2);
}

void draw_pretty_two_hists(TH1* backHist, TH1* frontHist, const TString title,
    const TString backTitle,
    const TString frontTitle,
    // if no location is given nothing is saved
    const TString img_save_location = "",
    const TString options = "",
    // these defaults will arrange the stats & legend in the top left corner
    // stats box should show: name, mean, RMS & integral (incl errors)
    // const int& stats_opt = 1002201, 
    const int stats_opt = 1, 
    const double frontX1 = 0.65, const double frontX2 = 0.9 ,
    const double frontY1 = 0.75, const double frontY2 = 0.9 ,
    const double backX1 = 0.65,  const double backX2 = 0.9 ,
    const double backY1 = 0.59,  const double backY2 = 0.74,
    const double legX1 = 0.44,   const double legX2 = 0.64 ,
    const double legY1 = 0.75,   const double legY2 = 0.9
) {
    TCanvas* can = new TCanvas(title, title);
    backHist->SetTitle(title);
    backHist->Draw(options);
    // can->Update();
    edit_stats_box(can, backHist,  stats_opt, backX1,  backX2,  backY1,  backY2);

    frontHist->SetLineColor(2);
    frontHist->Draw((options + "SAMES"));
    // can->Update();
    edit_stats_box(can, frontHist, stats_opt, frontX1, frontX2, frontY1, frontY2);

        // create a legend for extra info
    TLegend* leg = new TLegend(legX1, legY1, legX2, legY2);
    leg->AddEntry(frontHist, frontTitle);
    leg->AddEntry(backHist, backTitle); // add the two histrograms to the legend
    leg->SetFillColor(0);
    leg->Draw();

    if(img_save_location!="") {
        can->SaveAs(img_save_location);
    }
}

// the stupidly long variable name is to try and stop namespace collisions @ global
const int __useful_default_colour_selection [] =  {1, 2, 4, 3, 6, 7, 8, 9};
void draw_pretty_hists(const int& n_hists, TH1F** hist_array,   
    const TString title,         // title for the entire plot
    const TString* leg_entries,  // titles for each legend entry
    const TString img_save_location ="",
    const int stats_opt=0, // 1002201 <- name, mean±er, rms±er & integral
    const TString draw_opt = "",
    const int colours [n_hists] = __useful_default_colour_selection
) {
    TCanvas* can = NULL;
    if (img_save_location == ""){
        can = new TCanvas(title, title); // if it's not being saved make it small
    } else {
        can = new TCanvas(title, title,1436,856); // otherwise as big as possible, please! 
    }
    // set up the legend
    const float x1 = (stats_opt) ? 0.60:0.70; // figure out where to put it 
    const float x2 = (stats_opt) ? 0.80:0.90;
    const float y1 = 0.9 - 0.04*n_hists; 
    const float y2 = 0.90;
    TLegend* leg = new TLegend(x1, y1, x2, y2);
    // find the largest histogram (otherwise y range will be too small)
    int max = -1;     
    int first_hist = 0; // want to draw largest hist first               
    
    for(int hist = 0; hist < n_hists; ++hist) {
        const int current_max = hist_array[hist]->GetMaximum();
        if(current_max > max){
            max = current_max;
            first_hist = hist;
        }
    }
    
    if (stats_opt) {
        can->SetRightMargin((1.0 - x2)); // make space on the right hand side for the stats boxes
    } else {
        hist_array[first_hist]->SetStats(false);// switch off stats for the first
    }

    hist_array[first_hist]->Draw();
    
    for(int hist = 0; hist < n_hists; ++hist) {
        hist_array[hist]->SetLineWidth(2);// otherwise the lines are tiny
        hist_array[hist]->SetLineColor(colours[hist]); // mmmm colour!
                                             
        // match the appropriate histogram to its title
        leg->AddEntry(hist_array[hist], leg_entries[hist]); 
        
        // enable stats box drawing if required
        const TString tmp_draw_opt = (stats_opt) ? "sameS"+draw_opt : "same"+draw_opt;
        
        if (hist != first_hist) hist_array[hist]->Draw(tmp_draw_opt);
        
        if (stats_opt){
            // make sure that the name of on the stats box matches the legend entry
            hist_array[hist]->SetName(leg_entries[hist]); 
            // histogram has to have been drawn before you can modify stats box        
            // position the stats boxes so that they're all visible on the right hand side
            const float y1_stat = (0.81/n_hists)*hist + 0.1;
            const float y2_stat = (0.81/n_hists)*(hist+1) + 0.09; 
            const float x1_stat = x2+0.01; 
            const float x2_stat = 0.99; 
            // tidy up the stats box
            edit_stats_box(can, hist_array[hist], stats_opt, x1_stat, x2_stat, y1_stat, y2_stat);
        } 
    }    

    // hack to set the title of the histogram (yet have a different entry for 
    // the first hist in the legend, if desired)
    hist_array[first_hist]->SetTitle(title);
    
    // make sure the y extent is enough to show everything
    leg->SetFillColor(0); // don't want grey backgrounds
    leg->Draw();
    
    if (img_save_location != "") can->SaveAs(img_save_location);
}

void draw_pretty_hist(TH1* hist, const TString title = "",
    const TString img_save_location ="",
    const TString options = "",
    const int stat_opt=1002201,
    const double x1 = 0.70, const double x2 = 0.90, 
    const double y1 = 0.70, const double y2 = 0.90
) {
    TCanvas* can = NULL;
    TString title_t;
    if(title == "") {
        title_t =hist->GetTitle();
    } else {
        title_t = title;
    }
    if (img_save_location == ""){
        can = new TCanvas(title_t, title_t); // if it's not being saved make it small
    } else {
        can = new TCanvas(title_t, title_t,1436,856); // otherwise as big as possible, please! 
    }
    hist->SetTitle(title_t);
    hist->Draw(options);
    edit_stats_box(can, hist,stat_opt, x1, x2, y1, y2);
    can->Update();
    if (img_save_location != "" )can->SaveAs(img_save_location);
}

void create_boxy_legend(const TString legend_header, const int n_boxes, 
    const TString const* box_names, const int box_colors[n_boxes],
    const float x1 = 0.15, const float x2 = 0.45, 
    const float y1 = 0.60, const float y2 = 0.90  
){
    TLegend* leg = new TLegend(x1,y1,x2,y2);
    leg->SetHeader(legend_header);
    leg->SetFillColor(0);
    // TBox* boxes[n_boxes] = new TBox*[n_boxes]; //allocate the memory
    TBox* boxes[n_boxes];
    for(int i = 0; i < n_boxes; ++i) {
        boxes[i] = new TBox(0.0, 0.0, 0.0, 0.0);
        boxes[i]->SetFillColor(box_colors[i]);
        leg->AddEntry(boxes[i], box_names[i],"F");
    }
    leg->Draw();
}
