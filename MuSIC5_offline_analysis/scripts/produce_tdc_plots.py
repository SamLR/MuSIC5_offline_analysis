"""
This script produces TDC plots from either the simulated or real MuSIC 5
data. 
"""

from tdc_file import get_tdc_file_and_dict
from sim_file import get_sim_file_and_dict
from count_muons import calculate_derived_values

from fit_settings import fitting_settings_slow, fitting_settings_fast, \
                         fitting_parameters

from root_utilities import make_hist, set_bin_val_er_label, \
                           get_canvas_with_hists

from time import sleep

_sim_data_file_name = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/MuSIC5_detector/scripts/dt_hists.root"
_tdc_data_file_name = "music5_tdc_data.root"

def get_hists_fitting_parameter_vs_setting(files_info, parameter):
    # setting strings could be culled from the files info but would 
    # come out in a less than useful order
    """
    Generate plots of the fitting parameter (e.g. '#Tau_{#mu_{Cu}}')
    against the settings used to generate the fit. 
    
    Produces a single canvas of one plot per channel; each
    channel's entry displays the values for all settings grouped by 
    file.
    """
    # simple wrapper for make hist with the required defaults
    hist_axis_titles = ('Fit settings', parameter)
    hists = {}
    
    for file_id in files_info:
        fits = files_info[file_id]['fits']
        n_settings = len(fits)
        
        for ch_id in files_info[file_id]['run_conditions']['ch_used']:
            hist_key = "%s+file_%s+ch_%s"%(parameter, str(file_id), ch_id)
            hists[hist_key] = make_hist(hist_key, 0, n_settings, hist_axis_titles)
            
            for bin, setting_str in enumerate(fits, 1):
            # bin 0 == underflow. bin number != x_axis value
                val, er  = fits[setting_str]['ch_dat'][ch_id][parameter]                
                
                if parameter=="chi2":
                    val = float(val)/er # express chi2 as chi2/NDF
                    er = 0.0
                
                set_bin_val_er_label(hists[hist_key], bin, val, er, setting_str)
    return hists


def get_hists_file_val_vs_setting(files_info, file_val):
    """
    Get a set of histograms of file values (i.e. muon yields, muon counts) 
    against settings
    """
    hist_axis_titles = ('Fit settings', file_val)
    hists = {}
    
    for file_id in files_info:
        fits = files_info[file_id]['fits']
        n_settings = len(fits)
        
        hist_key =  "%s+file_%s"%(file_val, str(file_id))
        hists[hist_key] = make_hist(hist_key, 0, n_settings, hist_axis_titles)
        
        for bin, setting_str in enumerate(fits, 1):
        # bin 0 == underflow. bin number != x_axis value
            val, er = fits[setting_str][file_val]
            set_bin_val_er_label(hists[hist_key], bin, val, er, setting_str)
    return hists
        


def get_hists_fitting_parameter_vs_deg_dz(files_info, parameter):
    """
    Get a set of histograms of parameter Vs degrader thickness
    """
    hist_axis_titles = ('Degrader thickness (mm)', parameter)
    hists = {}
    
    # dictionary ordering is not gaurenteed 
    deg_dzs = [(i,files_info[i]['run_conditions']['deg_dz']) for i in files_info]
    deg_dzs.sort(key = lambda x:x[1]) # sort by thickness
    
    for bin, (file_id, dz) in enumerate(deg_dzs, 1):
        for ch_id in files_info[file_id]['run_conditions']['ch_used']:
            for setting_str in files_info[file_id]['fit_settings']:
                
                hist_key = "%s+ch_%s+settings_%s"%(parameter, ch_id, setting_str)
                if hist_key not in hists: 
                    hists[hist_key] = make_hist(hist_key, 0, len(files_info), hist_axis_titles)
                
                val, er = files_info[file_id]['fits'][setting_str]['ch_dat'][ch_id][parameter]
            
                if parameter=="chi2":
                    val = float(val)/er # express chi2 as chi2/NDF
                    er = 0.0
                
                set_bin_val_er_label(hists[hist_key], bin, val, er, dz)
    return hists


def get_hists_file_val_vs_deg_dz(files_info, file_val):
    """
    Get a set of histograms of file vals Vs degrader thickness
    """
    hist_axis_titles =  ('Degrader thickness (mm)', file_val)
    hists = {}
    
    # dictionary ordering is not gaurenteed 
    deg_dzs = [(i,files_info[i]['run_conditions']['deg_dz']) for i in files_info]
    deg_dzs.sort(key = lambda x:x[1]) # sort by thickness
    
    for bin, (file_id, dz) in enumerate(deg_dzs, 1):
        for setting_str in files_info[file_id]['fit_settings']:
            hist_key =  "%s+settings_%s"%(file_val, setting_str)
            if hist_key not in hists: 
                hists[hist_key] = make_hist(hist_key, 0, len(files_info), hist_axis_titles)
            val, er = files_info[file_id]['fits'][setting_str][file_val]
            set_bin_val_er_label(hists[hist_key], bin, val, er, dz)
            
    return hists


if __name__=="__main__":
    slow = True # TODO make this a toggle
    tdc = True # TODO add select sim/tdc/both
    sim = True
    hist_type = 1
    sleep_time = 10
    parameter = "muon_yields"
    fit_settings = fitting_settings_slow if slow else fitting_settings_fast
    
    tdc_file = tdc_dict = sim_file = sim_dict = None
    
    if tdc:
        tdc_file, tdc_dict = get_tdc_file_and_dict(_tdc_data_file_name)
    if sim:
        sim_file, sim_dict = get_sim_file_and_dict(_sim_data_file_name) 
    
    dicts_to_process = {'tdc_dict':tdc_dict, 'sim_dict':sim_dict}
    dicts_to_process = {i:j for i,j in dicts_to_process.items() if (j!=None)}
    
    for settings in fit_settings:
        for data_set in dicts_to_process.values():
            calculate_derived_values(data_set, fitting_parameters, settings)
    # TODO add checking valid parameters
    # TODO make all keys lower case
    # TODO simplify fit parameter keys i.e. N_{B}->C_b etc
    hist_functions = (get_hists_fitting_parameter_vs_setting,
                      get_hists_file_val_vs_setting,
                      get_hists_fitting_parameter_vs_deg_dz,
                      get_hists_file_val_vs_deg_dz)
    
    hists = {}
    for data_type,data_set in dicts_to_process.items():
        hists[data_type] = hist_functions[hist_type](data_set, parameter)
    
    get_canvas_with_hists(hists)
    sleep(sleep_time)
    # either load or create pickle file of files_info(dat&sim)
    # based on arg either:
    #   param Vs setting 
    #   param Vs deg_dz
    #   file_val vs setting
    #   file_val vs deg_dz
    # split up as:
    # setting/file:{ch:hist}
    # ch:{setting/file:hist}
    # 