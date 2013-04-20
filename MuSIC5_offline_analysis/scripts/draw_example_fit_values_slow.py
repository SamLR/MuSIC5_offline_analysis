"""
This is a skeleton drawing script. Copy it, substitute the relevant values
(e.g. slow or fast settings, real or simulated data) and then refine the 
drawing and display as required.
"""

from tdc_file import get_tdc_file_and_dict
from sim_file import get_sim_file_and_dict

from count_muons import calculate_derived_values

from fit_settings import fitting_settings_slow, fitting_parameters

from list_utilities import create_sub_dicts_from_keys

from root_utilities import make_canvas

from get_hists import get_hists_fitting_parameter_vs_setting, get_hists_file_val_vs_deg_dz,\
                        get_hists_fitting_parameter_vs_deg_dz

from time import sleep
from ROOT import gStyle, TLegend

_tdc_data_file_name = "music5_tdc_data.root"
_sim_data_file_name = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/MuSIC5_detector/scripts/inclusive_dt_hists.root"

if __name__=="__main__":
    gStyle.SetOptStat(1101)
    sleep_time = 360
    parameter = ("N_{b}", "N_{c}","#tau_{c}", "N_{f}", "#tau_{f}")
    selection = ("file_448+ch_D1", "file_Air_0mm+ch_na")
    
    fit_settings =  fitting_settings_slow
    
    file_ptr, data_dict = get_sim_file_and_dict(_sim_data_file_name)
    file_ptr2, data_dict2 = get_tdc_file_and_dict(_tdc_data_file_name)
    data_dict.update(data_dict2)
    
    for settings in fit_settings:
        settings.update({'save_hist':True})
        calculate_derived_values(data_dict, fitting_parameters, settings)
    
    hists = {}
    for param in parameter:
        hists [param] = get_hists_fitting_parameter_vs_setting(data_dict, param)
    
    
    hists_to_draw = {}
    for param, hist_dict in hists.items():
        hists_to_draw[param]={}
        for hist_key, hist in hist_dict.items():
            for sel in selection:
                if sel in hist_key:
                    hists_to_draw[param][hist_key] = hist
    
    can = make_canvas('c1',3,2, resize=True)
    pad_number = 0
    for param in hists_to_draw:
        pad_number+=1
        pad = can.cd(pad_number)
        pad.SetRightMargin(0.2)
        pad.SetBottomMargin(0.15)
        run = 451
        ch = "D1"
        # dat_hist = hists_to_draw[param][param+"+file_448+ch_D1"]
        dat_hist = hists_to_draw[param][param+("+file_%i+ch_%s"%(run,ch))]
        # sim_hist = hists_to_draw[param][param+"+file_Air_0mm+ch_na"]
        sim_hist = hists_to_draw[param][param+"+file_Aluminium_0.5mm+ch_na"]
        
        get_min = lambda x:x.GetMinimum()
        get_max = lambda x:x.GetMaximum()
        
        y_min = get_min(dat_hist) if get_min(dat_hist) < get_min(sim_hist) else get_min(sim_hist)
        y_max = get_max(dat_hist) if get_max(dat_hist) > get_max(sim_hist) else get_max(sim_hist)
        
        y_min = 0.9 * y_min if y_min > 0 else 1.1*y_min
        y_max = 1.1 * y_max
        
        # will draw data first so make sure its scale is large enough
        dat_hist.SetMinimum(y_min)
        dat_hist.SetMaximum(y_max)
        
        dat_hist.SetTitle(param + " for various fit settings and no degrader")
        
        dat_hist.SetName("Run %i, %s"%(run,ch))
        # dat_hist.GetXaxis().SetLabelSize(0.03);
        dat_hist.GetYaxis().SetLabelSize(0.03);
        dat_hist.GetYaxis().SetTitleOffset(1.05);
        dat_hist.GetXaxis().SetTitle("");
        dat_hist.SetLineColor(1)
        dat_hist.Draw("S")
        
        sim_hist.SetName("Simulation")
        # sim_hist.GetXaxis().SetLabelSize(0.03);
        sim_hist.GetYaxis().SetLabelSize(0.03);
        dat_hist.GetYaxis().SetTitleOffset(1.05);
        sim_hist.GetXaxis().SetTitle("");
        sim_hist.SetLineColor(2)
        sim_hist.Draw("SAMES") # make sure the stats box is drawn
        
        X1, Y1, X2, Y2 = 0.81, 0.76, 0.99, 0.9
        
        # set this late for the legend but to maintain the total title as well
        # make the legend
        legend = TLegend(X1, Y1, X2, Y2)
        legend.AddEntry(dat_hist, dat_hist.GetName())
        legend.AddEntry(sim_hist, sim_hist.GetName())
        legend.SetFillColor(0)
        legend.Draw()
        pad.Update()
        
        # move stats boxes about
        dat_stats_box = dat_hist.FindObject("stats")
        dat_stats_box.SetX1NDC(X1)
        dat_stats_box.SetX2NDC(X2)
        Y1, Y2 = Y1 - 0.15, Y2 - 0.15
        dat_stats_box.SetY2NDC(Y2)
        dat_stats_box.SetY1NDC(Y1)

        sim_stats_box = sim_hist.FindObject("stats")
        sim_stats_box.SetX1NDC(X1)
        sim_stats_box.SetX2NDC(X2)
        Y1, Y2 = Y1 - 0.15, Y2 - 0.15
        sim_stats_box.SetY2NDC(Y2)
        sim_stats_box.SetY1NDC(Y1)
        
        can.ForceUpdate()
        setattr(can,'legend'+param,legend) # make sure legend stays in scope
        
    can.Update()    
    can.SaveAs("images/sim_vs_data_parameter_WRT_settings_slow.svg")
    sleep(sleep_time)
    