#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TCanvas.h"

struct branch{
    Int_t n_hits;
    UInt_t tdc[500];
};

unsigned int convert_to_time(unsigned int val);
unsigned int convert_to_ch(unsigned int val);
bool is_good(unsigned int val);

void test(){
    TFile* file = new TFile("../../../MuSIC_data_0.5Cu/run00459.root", "READ");
    TTree* tree = (TTree*)file->Get("Trigger");
    // TH1F* hist = new TH1F("h", "h", 2000000, -1e6, 1e6);
    // TH1F* hist2 = new TH1F("h2", "h2", 2000000, -1e6, 1e6);
    // TH1F* hist = new TH1F("h", "h", 20000, -1e6, 1e6);
    // TH1F* hist2 = new TH1F("h2", "h2", 20000, -1e6, 1e6);
    TH1F* hist2 = new TH1F("h2", "h2", 30000, 0, 3e6);
    // TH1F* hist3 = new TH1F("h3", "h3", 10000000, 0, 2e6);

    branch b;
    tree->SetBranchAddress("TDC0", &b);
    
    unsigned int er_count = 0;
    unsigned int max_multi = 50000;
    unsigned int multi_hit_count[max_multi];
    for(unsigned int i = 0; i < max_multi; ++i) {
        multi_hit_count[i] = 0;
    }
    const int channel = 13; // D1 = 9
    const unsigned int n_entries = tree->GetEntries();
    // const unsigned int n_entries = 200;
    for(unsigned int entry = 0; entry < n_entries; ++entry) {
        tree->GetEntry(entry);
        int electron_hits[500]; // good hits on channel 9
        int raw_hits[500]; // good hits on channel 9
        int tdc0 = -666;
        unsigned int e_hit = 0;
        for(int hit = 0; hit < static_cast<int>(b.n_hits); ++hit) {
            unsigned int val = static_cast<unsigned int>(b.tdc[hit]);
            unsigned int ch = convert_to_ch(val);
            if (ch == 0 && is_good(val)){
                // hist3->Fill(convert_to_time(val));
                if (tdc0 != -666){
                    printf("Double hit on ch 0!\n");
                    ++er_count;
                    tdc0 = convert_to_time(val);
                } else {
                    tdc0 = convert_to_time(val);
                } 
            } else if (ch==channel && is_good(val)) {
                int t_hit = static_cast<int>(convert_to_time(val));
                hist2->Fill(t_hit);
                // raw_hits[e_hit] = t_hit;
                // electron_hits[e_hit++] = t_hit - tdc0;
            }
        }
        
        if (e_hit > 1 && e_hit < max_multi) {
            ++multi_hit_count[e_hit];
        } else if (e_hit > max_multi){
            printf("pretty sure this is impossible %i\n", e_hit);
        }
        
        // Fill the hist with hits
        for(unsigned int hit = 0; hit < e_hit; ++hit) {
            // hist2->Fill(raw_hits[hit]);
        //     hist->Fill(electron_hits[hit]);
        }
    }
    unsigned int all_multi = 0;
    for(unsigned int i = 0; i < max_multi; ++i) {
        if (multi_hit_count[i] > 0) {
            printf("%i: %i\n", i, multi_hit_count[i]);
            all_multi += multi_hit_count[i];
        }
    }
    printf("multi hits:%i  double tdc0's:%i\n", all_multi, er_count);
    // printf("max 1:%.0f 2:%.0f\n",hist->GetMaximum(), hist2->GetMaximum());
    // hist->Draw();
    // hist2->SetLineColor(kRed);
    // hist2->Draw("SAMES");
    hist2->Draw();
    // TCanvas* can = new TCanvas("c2", "c2");
    // can->cd();
    // hist3->Draw("E");
    
}

unsigned int convert_to_time(unsigned int val){
    unsigned int const tdc_data_mask  = 0x1fffff;
    return val & tdc_data_mask;
}

unsigned int convert_to_ch(unsigned int val){
    unsigned int const tdc_channel_mask = 0x03e00000;
    return (val & tdc_channel_mask) >> 21;
}

bool is_good(unsigned int val){
    unsigned int const tdc_data_type_mask = 0xf8000000;
    unsigned int const tdc_measurement    = 0x00000000;
    return (val & tdc_data_type_mask) == tdc_measurement;
}