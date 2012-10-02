# 
# Ultimately this will emulate the 'count_muons.py' script
# but operating on the simulated data rather than the 
# real data
# 

from config_sim_data import *

from ROOT import TFile, TH1F, gStyle

from fitting import fit_hist

from utilities import make_canvas, wait_to_quit


def get_data_dict(file_name):
    """
    Opens the 
    """
    in_tfile = TFile(file_name, "READ")
    res = {}
    for key in in_tfile.GetListOfKeys():
        # name looks like "Muon_momentum_with_Aluminium_0.5mm"
        hist = key.ReadObj()
        name_bits = (hist.GetName()).split("_")
        dict_key = "%s_%s"%(name_bits[3],name_bits[4])
        
        # use the [:-2] to trim the 'mm' from the thickness
        res[dict_key] = {'thickness':float(name_bits[4][:-2]), 'material':name_bits[3], 'hist':hist}
    return res, in_tfile

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
    for key, data in hist_dict.items():
        print "*"*40, "\n", key, "\n"
        hist = data['hist']
        fit_results = fit_hist(hist, fit_lo, fit_hi, bin_width, initial_fit_params, save_hist)
        
        if save_hist and draw: 
            canvases[key] = make_canvas(key, maximised=True)
            fit_results['hist'].Draw()
            save_location = "images/fitted_simulation_data_"+key+".svg"
            canvases[key].SaveAs(save_location)
            
        hist_dict[key]['fitting_results'] = fit_results
        
        
        
    wait_to_quit()

if __name__=="__main__":
    main()