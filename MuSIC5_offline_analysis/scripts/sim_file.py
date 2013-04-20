# 
# Ultimately this will emulate the 'count_muons.py' script
# but operating on the simulated data rather than the 
# real data
# 

from config_sim_data import sim_run_conditions

from ROOT import TFile, TH1F, gStyle, gROOT

from fitting import fit_hist

from root_utilities import make_canvas, make_hist, set_bin_val_er_label

from general_utilities import wait_to_quit

from list_utilities import printTraverse
                      
import os.path

def get_sim_file_and_dict(file_name,  recreate=False):
    """
    Opens the TFile containing the dt plots for simulated data
    and returns a dict with the same structure as the real data.
    """
    # TODO Add autogeneration of the appropriate file if needed
    
    in_tfile = TFile(file_name, "READ")
    res = {}
    for key in in_tfile.GetListOfKeys():
        hist = key.ReadObj()
        # name looks like "parent-daughter_dts_for_Aluminium_0.5mm", j = junk
        j1, j2, j3, deg_mat, deg_dz = (hist.GetName()).split("_")
        
        if deg_mat.lower() == "air": deg_dz = "0mm"
        dict_key = "%s_%s"%(deg_mat, deg_dz)
        
        # Create the 'run_conditions' dictionary & update with the sim values
        # use the [:-2] to trim the 'mm' from the thickness
        hist_conditions = {'deg_dz':float(deg_dz[:-2]), 'material':deg_mat}
        hist_conditions.update(sim_run_conditions)
        # print hist_conditions['acceptance']
        hist_conditions['acceptance'] = hist_conditions['acceptance'](hist.Integral())
        # print hist_conditions['acceptance']
        res[dict_key] = {'run_conditions': hist_conditions,
                        'hists':{sim_run_conditions['ch_used'][0]:hist}}
                        # hists: {ch_id: hist, ch_id2:hist2....}
    return in_tfile, res
    


# def get_muon_yield_per_amp(file_info):
#     """Convert number of muons & error to a yield per A proton current"""
#     n_mu, n_mu_er = file_info['fits']['total_muons']
#     x = detector_efficiency* file_info['acceptance'] * file_info['time'] * file_info['current'] *nA
#     mu_yield = float(n_mu) / x
#     mu_yield_er = float(n_mu_er) / x
#     return mu_yield, mu_yield_er


def main():
    # open file
    # for all settings? (skip this initially)
    #   for all hists:
    #       parse set up (deg thickness)
    #       fit it
    #       gather results
    #       draw fits 
    #   draw hists of fit results
    
    get_sim_file_and_dict(config.sim_data_file_name, True)
    # if config.draw: canvases = {}
    #     printTraverse (hist_dict)
    #     for fit_lo, fit_hi, bin_width, in config.settings:
    #         setting_str = settings_str(fit_lo, fit_hi, bin_width)
    #         
    #         for key, data in hist_dict.items():
    #             print "*"*40, "\n", key, "\n"
    #             hist = data['hist']
    #             fit_results = fit_hist(hist, fit_lo, fit_hi, bin_width, initial_fit_params)
    #             
    #             hist_dict[key][setting_str]= {'fitting_results':fit_results}
#         
#     # tau_hists = {}    
#     # for key in hist_dict:
#     #     tau_hists[key] = make_hist(key, 0, len(settings), "setting", "#tau_{#mu_{all}}")
#     #     for bin, (fit_lo, fit_hi, bin_width) in enumerate(settings,1):
#     #         setting_str = "lo_%i_hi_%i_bins_%i"%(fit_lo, fit_hi, bin_width)
#     #         val, er = hist_dict[key][setting_str]['fitting_results']['fit_param']['#tau_{#mu_{All}}']
#     #         if val < 0: val = 0
#     #         set_bin_val_er_label(tau_hists[key], bin, val, er, setting_str)
#     
#     # can = make_canvas("sim_tau_all", maximised=True);
#     # draw_opt = "P"
#     # for number, hist in enumerate(tau_hists.values(),1):
#     #     hist.SetLineColor(number)
#     #     hist.Draw(draw_opt)
#     #     draw_opt="PSAME"
#     
#     printTraverse(hist_dict)
#     
#     # setting_strs = [settings_str(*i) for i in settings]
#     # fmt_str = u"%26s " + u" %.2e \xb1 %.0e "*len(hist_dict.keys())
#     # head_fmt = "%26s " + " %16s "*len(hist_dict.keys())
#     # print head_fmt%(('settings',)+tuple(hist_dict.keys()))
#     # for set_str in setting_strs:
#     #     vals = [set_str,]
#     #     for id in hist_dict:
#     #         print hist_dict[id]
#     #         mu_yield, mu_yield_er = hist_dict[id]['fits'][set_str]['muon_yields']
#     #         vals.append(mu_yield)
#     #         vals.append(mu_yield_er)
#     #     print fmt_str%tuple(vals)
#         
#     # wait_to_quit()

if __name__=="__main__":
    main()