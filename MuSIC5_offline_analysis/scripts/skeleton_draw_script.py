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

from root_utilities import get_canvas_with_hists

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
    # parameter = "#tau_{#mu_{Cu}}"
    fit_settings =  fitting_settings_fast 
    
    file_ptr, data_dict = get_sim_file_and_dict(_sim_data_file_name)
    file_ptr2, data_dict2 = get_tdc_file_and_dict(_tdc_data_file_name)
    data_dict.update(data_dict2)
    for settings in fit_settings:
        settings.update({'save_hist':True})
        calculate_derived_values(data_dict, fitting_parameters, settings)
    # hists = {}
    #     for setup, data in data_dict.items():    
    #         for settings, fit_res in data['fits'].items():
    #             for ch in data['run_conditions']['ch_used']:
    #                 key = str(setup)+"+"+str(settings)+"+"+str(ch)
    #                 hists[key] = fit_res['ch_dat'][ch]['hist']
    #                 
    
    # hists = get_hists_fitting_parameter_vs_deg_dz(data_dict, parameter)
    # hists = get_hists_fitting_parameter_vs_setting(data_dict, parameter)
    hists = get_hists_file_val_vs_deg_dz(data_dict, parameter)
    
    # hists = get_hists_file_val_vs_deg_dz(data_dict, parameter)
    
    # ch_id_hists = create_sub_dicts_from_keys(hists,
                    # keysplit_function=lambda x: (x.split('+')[1], x.split('+')[2]) )
    # def quick_split(x):
    #     # expect x ~ muon_rates+settings_lo_X_hi_Y_bins_Z
    #     bits = (x[20:]).split('_') # get just 'lo_%i_hi_%i_bins_%i'
    #     return bits[5], bits[1]
    
    # def quick_split(x):
    #     bits = x.split('x')
        
        
    # lo_bins_split_hists = create_sub_dicts_from_keys(hists,
    #                 keysplit_function=quick_split)
                    
    can = get_canvas_with_hists(hists)
    # can = get_canvas_with_hists(ch_id_hists)
    # can = get_canvas_with_hists(lo_bins_split_hists)
    sleep(sleep_time)
    