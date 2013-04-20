"""
This is a skeleton drawing script. Copy it, substitute the relevant values
(e.g. slow or fast settings, real or simulated data) and then refine the 
drawing and display as required.
"""

from tdc_file import get_tdc_file_and_dict
from sim_file import get_sim_file_and_dict

from count_muons import calculate_derived_values

from fit_settings import fitting_settings_fast, fitting_settings_slow, fitting_parameters

from list_utilities import create_sub_dicts_from_keys

from root_utilities import make_canvas

from get_hists import get_hists_fitting_parameter_vs_setting, get_hists_file_val_vs_deg_dz,\
                        get_hists_fitting_parameter_vs_deg_dz

from ROOT import gStyle

from time import sleep



_tdc_data_file_name = "music5_tdc_data.root"
_sim_data_file_name = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/MuSIC5_detector/scripts/inclusive_dt_hists.root"

if __name__=="__main__":
    gStyle.SetOptStat(1002200)
    gStyle.SetOptFit()
    sleep_time = 360
    fit_settings =  fitting_settings_fast 
    fit_settings[0]['fit_opt'] = "QRS"
    
    file_ptr, data_dict = get_sim_file_and_dict(_sim_data_file_name)
    file_ptr2, data_dict2 = get_tdc_file_and_dict(_tdc_data_file_name)
    data_dict.update(data_dict2)
    for settings in fit_settings:
        settings.update({'save_hist':True})
        calculate_derived_values(data_dict, fitting_parameters, settings)
    
    # print data_dict
    hists = {"sim":data_dict['Air_0mm']['fits']['lo_100_hi_20000_bins_50']['ch_dat']['na']['hist'],
             "dat":data_dict[448]['fits']['lo_100_hi_20000_bins_50']['ch_dat']['D1']['hist']}
    
    titles = {"sim":"Simulated data with 50ns bins, fit range 0.1-20#mu s, no degrader",
              "dat":"Run 448, ch D1, data with 50ns bins, fit range 0.1-20#mu s, no degrader"}
    
    c = make_canvas("example_hists",n_x=2,resize=True)
    for pad,(key, hist) in enumerate(hists.items(),1): 
        c.cd(pad)
        hist.SetTitle(titles[key])
        # make the axis readable
        hist.GetXaxis().SetTitle("Time (ns)")
        hist.GetXaxis().SetLabelSize(0.02)
        hist.GetYaxis().SetLabelSize(0.02)
        hist.GetYaxis().SetTitleOffset(1.2)
        hist.Draw()
    c.SaveAs("images/example_fits_data_and_sim.svg")
    # -------------------
    c2 = make_canvas("low_freq_noise",resize=True)
    c2.cd()
    run = 448
    ch="D1"
    bins = 30
    low = 0
    high = 20
    close_up = data_dict[run]['hists'][ch].Clone("Zoom")
    close_up.SetTitle("Run "+str(445)+", ch "+ch+" , data with "+str(bins)+
                    "ns bins, showing region "+str(low)+"-"+str(high)+"#mu s")
    close_up.Rebin(bins)
    close_up.GetXaxis().SetRangeUser(low*1000,high*1000)
    close_up.Draw("E")
    c2.SaveAs("images/example_noise.svg")
    # -------------------    
    c3 = make_canvas("hi_freq_noise",resize=True)
    c3.cd()
    bins = 100
    low = 0
    high = 20
    close_up2 = data_dict[run]['hists'][ch].Clone("Zoom2")
    close_up2.SetTitle("Run "+str(445)+", ch "+ch+" , data with "+str(bins)+
                    "ns bins, showing region "+str(low)+"-"+str(high)+"#mu s")
    close_up2.Rebin(bins)
    close_up2.GetXaxis().SetRangeUser(low*1000,high*1000)
    close_up2.Draw("E")
    c3.SaveAs("images/example_smoothing.svg")

    # -------------------
    c4 = make_canvas("low_freq_noise",resize=True)
    c4.cd()
    run = 448
    ch="D1"
    bins = 30
    low = 15
    high = 20
    close_up = data_dict[run]['hists'][ch].Clone("Zoom")
    close_up.SetTitle("Run "+str(445)+", ch "+ch+" , data with "+str(bins)+
                    "ns bins, showing region "+str(low)+"-"+str(high)+"#mu s")
    close_up.Rebin(bins)
    close_up.GetXaxis().SetRangeUser(low*1000,high*1000)
    close_up.Draw("E")
    c4.SaveAs("images/example_noise_zoom.svg")
    sleep(sleep_time)
    