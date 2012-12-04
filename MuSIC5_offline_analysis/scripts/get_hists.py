from root_utilities import make_hist, set_bin_val_er_label


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
