"""
This is a skeleton drawing script. Copy it, substitute the relevant values
(e.g. slow or fast settings, real or simulated data) and then refine the 
drawing and display as required.
"""

from tdc_file import get_tdc_file_and_dict
from sim_file import get_sim_file_and_dict

from count_muons import calculate_derived_values

from fit_settings import fitting_settings_fast, fitting_parameters

from list_utilities import create_sub_dicts_from_keys

from root_utilities import make_canvas

from get_hists import get_hists_fitting_parameter_vs_setting, get_hists_file_val_vs_deg_dz,\
                        get_hists_fitting_parameter_vs_deg_dz

from time import sleep

_tdc_data_file_name = "music5_tdc_data.root"
_sim_data_file_name = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/MuSIC5_detector/scripts/inclusive_dt_hists.root"

if __name__=="__main__":
    sleep_time = 360
    parameter = "muon_yields"
    # parameter = "muons_per_p"
    # parameter = "#tau_{#mu_{All}}"
    # parameter = "#tau_{f}"
    fit_settings =  fitting_settings_fast
    
    file_ptr, data_dict = get_sim_file_and_dict(_sim_data_file_name)
    file_ptr2, data_dict2 = get_tdc_file_and_dict(_tdc_data_file_name)
    data_dict.update(data_dict2)
    for settings in fit_settings:
        settings.update({'save_hist':True})
        calculate_derived_values(data_dict, fitting_parameters, settings)
    
    hists = get_hists_file_val_vs_deg_dz(data_dict, parameter)
    
    can = make_canvas('yields', resize=True)
    hists = hists['muon_yields+settings_lo_100_hi_20000_bins_50']
    hists.SetTitle("Calculated muon yields for a 1#mu A proton beam at MuSIC")
    hists.GetYaxis().SetTitle("Muon Yield (muons/s)")
    hists.Draw()
    can.SaveAs("images/muon_yields.svg")
    sleep(sleep_time)
    