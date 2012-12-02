"""
This is a skeleton drawing script. Copy it, substitute the relevant values
(e.g. slow or fast settings, real or simulated data) and then refine the 
drawing and display as required.
"""

from tdc_file import get_tdc_file_and_dict
from sim_file import get_sim_file_and_dict

from count_muons import calculate_derived_values

from fit_settings import fitting_settings_fast, fitting_parameters, settings_str

from list_utilities import create_sub_dicts_from_keys

from root_utilities import get_canvas_with_hists

from get_hists import get_hists_fitting_parameter_vs_setting, get_hists_file_val_vs_deg_dz,\
                        get_hists_fitting_parameter_vs_deg_dz

from ROOT import TGraphErrors, TMultiGraph, TLegend
from array import array

from time import sleep

_tdc_data_file_name = "music5_tdc_data.root"
_sim_data_file_name = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/MuSIC5/MuSIC5_detector/scripts/inclusive_dt_hists.root"

if __name__=="__main__":
    sleep_time = 360
    parameter = "muon_yields"
    fitting_settings_fast = fitting_settings_fast[0]
    settings = settings_str(**fitting_settings_fast)
    
    file_ptr, data_dict = get_sim_file_and_dict(_sim_data_file_name)
    file_ptr2, data_dict2 = get_tdc_file_and_dict(_tdc_data_file_name)
    dat = {'sim':data_dict, 'real':data_dict2} 
    res = {'sim':[], 'real':[]}
    for n,d in dat.items():
        calculate_derived_values(d, fitting_parameters, fitting_settings_fast)
        for id, id_dat in d.items():
            dz = id_dat['run_conditions']['deg_dz']
            to_add = [dz,] + list(id_dat['fits'][settings][parameter])
            res[n].append(to_add)
    
    x_sim    = array('f',[i[0] for i in res['sim']])
    x_sim_er = array('f',[0.01 for i in res['sim']])
    y_sim    = array('f',[i[1] for i in res['sim']])
    y_sim_er = array('f',[i[2] for i in res['sim']])  
      
    x_real    = array('f',[i[0] for i in res['real']])
    x_real_er = array('f',[0.01 for i in res['real']])
    y_real    = array('f',[i[1] for i in res['real']])
    y_real_er = array('f',[i[2] for i in res['real']])
    
    print x_sim
    print x_sim_er
    print y_sim
    print y_sim_er
    
    
    mg = TMultiGraph()
    # set title{title; xaxis; yaxis}
    mg.SetTitle("Comparison of simulated and real muon yields; "
                "Degrader thickness (mm); Muon Yield for 1#mu A proton current")
    
    sim = TGraphErrors(len(x_sim), x_sim, y_sim, x_sim_er, y_sim_er)
    sim.SetName("sim")
    sim.SetMarkerColor(4)
    # sim.SetMarkerSize(8)
    # sim.SetMarkerStyle(21)
    sim.SetDrawOption("AP")
    
    real = TGraphErrors(len(x_real), x_real, y_real, x_real_er, y_real_er)
    real.SetName("real")
    real.SetMarkerColor(2)
    # real.SetMarkerSize(8)
    # real.SetMarkerStyle(20)
    real.SetDrawOption("AP")
    # 
    # leg = TLegend(0.8,0.8,0.9,0.9)
    # leg.AddEntry(sim,"Simulated data")
    # leg.AddEntry(real,"Real data")
    
    mg.Add(sim)
    mg.Add(real)
    mg.Draw("A")
    # leg.Draw()
    
    
    sleep(30)
    