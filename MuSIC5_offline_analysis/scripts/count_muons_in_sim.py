# 
# Ultimately this will emulate the 'count_muons.py' script
# but operating on the simulated data rather than the 
# real data
# 

from config_sim_data import *

from ROOT import TFile, TH1F, gStyle

from fitting import fit_hist

from utilities import make_canvas, wait_to_quit, make_hist,\
                      set_bin_val_er_label, printTraverse


# def get_data_dict(file_name):
#     """
#     Opens the 
#     """
#     in_tfile = TFile(file_name, "READ")
#     res = {}
#     for key in in_tfile.GetListOfKeys():
#         # name looks like "Muon_momentum_with_Aluminium_0.5mm"
#         hist = key.ReadObj()
#         name_bits = (hist.GetName()).split("_")
#         dict_key = "%s_%s"%(name_bits[3],name_bits[4])
#         
#         # use the [:-2] to trim the 'mm' from the thickness
#         res[dict_key] = {'thickness':float(name_bits[4][:-2]), 'material':name_bits[3], 'hist':hist}
#     return res, in_tfile

def get_data_dict(file_name):
    """
    Opens the TFile containing the dt plots for simulated data
    and returns a dict with the same structure as the real data.
    """
    # TODO Add autogeneration of the appropriate file if needed
    in_tfile = TFile(file_name, "READ")
    res = {}
    for key in in_tfile.GetListOfKeys():
        # name looks like "Muon_momentum_with_Aluminium_0.5mm"
        hist = key.ReadObj()
        junk1, junk2, junk3, deg_mat, deg_dz = (hist.GetName()).split("_")
        dict_key = "%s_%s"%(deg_mat, deg_dz)

        # use the [:-2] to trim the 'mm' from the thickness
        res[dict_key] = {'thickness':float(name_bits[4][:-2]), 'material':name_bits[3], 'hist':hist}
        return res, in_tfile
    

def get_muon_yield_per_amp(file_info):
    """Convert number of muons & error to a yield per A proton current"""
    n_mu, n_mu_er = file_info['fits']['total_muons']
    x = detector_efficiency* file_info['acceptance'] * file_info['time'] * file_info['current'] *nA
    mu_yield = float(n_mu) / x
    mu_yield_er = float(n_mu_er) / x
    return mu_yield, mu_yield_er

def settings_str(fit_lo, fit_hi, bin_width):
    return "lo_%i_hi_%i_bins_%i"%(fit_lo, fit_hi, bin_width)

def main():
    # open file
    # for all settings? (skip this initially)
    #   for all hists:
    #       parse set up (deg thickness)
    #       fit it
    #       gather results
    #       draw fits 
    #   draw hists of fit results
    
    gStyle.SetOptFit()
    gStyle.SetOptStat(0)
    
    hist_dict, in_file = get_data_dict(sim_data_file_name)
    if draw: canvases = {}
    
    for fit_lo, fit_hi, bin_width, in settings:
        setting_str = settings_str(fit_lo, fit_hi, bin_width)
        
        for key, data in hist_dict.items():
            print "*"*40, "\n", key, "\n"
            hist = data['hist']
            fit_results = fit_hist(hist, fit_lo, fit_hi, bin_width, initial_fit_params, save_hist)
        
            if save_hist and draw: 
                canvases[key] = make_canvas(key, maximised=True)
                fit_results['hist'].Draw()
                # save_location = "images/fitted_simulation_data_"+key+".svg"
                # canvases[key].SaveAs(save_location)
            
            hist_dict[key][setting_str]= {'fitting_results':fit_results}
        
    # tau_hists = {}    
    # for key in hist_dict:
    #     tau_hists[key] = make_hist(key, 0, len(settings), "setting", "#tau_{#mu_{all}}")
    #     for bin, (fit_lo, fit_hi, bin_width) in enumerate(settings,1):
    #         setting_str = "lo_%i_hi_%i_bins_%i"%(fit_lo, fit_hi, bin_width)
    #         val, er = hist_dict[key][setting_str]['fitting_results']['fit_param']['#tau_{#mu_{All}}']
    #         if val < 0: val = 0
    #         set_bin_val_er_label(tau_hists[key], bin, val, er, setting_str)
    
    # can = make_canvas("sim_tau_all", maximised=True);
    # draw_opt = "P"
    # for number, hist in enumerate(tau_hists.values(),1):
    #     hist.SetLineColor(number)
    #     hist.Draw(draw_opt)
    #     draw_opt="PSAME"
    
    printTraverse(hist_dict)
    
    # setting_strs = [settings_str(*i) for i in settings]
    # fmt_str = u"%26s " + u" %.2e \xb1 %.0e "*len(hist_dict.keys())
    # head_fmt = "%26s " + " %16s "*len(hist_dict.keys())
    # print head_fmt%(('settings',)+tuple(hist_dict.keys()))
    # for set_str in setting_strs:
    #     vals = [set_str,]
    #     for id in hist_dict:
    #         print hist_dict[id]
    #         mu_yield, mu_yield_er = hist_dict[id]['fits'][set_str]['muon_yields']
    #         vals.append(mu_yield)
    #         vals.append(mu_yield_er)
    #     print fmt_str%tuple(vals)
        
    # wait_to_quit()

if __name__=="__main__":
    main()