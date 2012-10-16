"""
Measure the gain stability over time by comparing the number of triggers
counted.
"""

from sclr_branch_func import * 
from root_utilities import make_canvas, make_hist
from ROOT import TGraphErrors, TGaxis
from array import array
from math import log

# mmmm pollute that global namespace!
time_er = 500
val_and_er = lambda x,y,x_er, y_er: (x-y, (x_er**2 + y_er**2)**0.5)

def _calc_rate_and_er(a,b,c,d,a_er,b_er,c_er,d_er):
    """
    Calculates (a-b)/(c-d) and its error
    """
    # z = (a-b)/(c-d)
    # dz = z * sqrt( d_ab/a+b ** 2 + d_cd/c+d ** 2)
    # d_ab = sqrt(da**2 + db**2)
    # make sure everything's a float
    a,b,c,d,a_er,b_er,c_er,d_er = [float(i) for i in (a,b,c,d,a_er,b_er,c_er,d_er)]
    
    ab, ab_er = val_and_er(a,b, a_er, b_er)
    cd, cd_er = val_and_er(c,d,c_er, d_er)
    
    rate = ab/cd
    rate_er = rate * ( (ab_er/ab)**2 + (cd_er/cd)) ** 0.5
    return rate, rate_er
    


def get_gain_stability_dict(tree, branch):
    # open file
    # step through entries
    # for each entry find (U&&!D - U&&!D_previous)/dt
    # NB scaler[2] == U&&!D
    #    scaler[7] == time
    n_entries = tree.GetEntries()
    prev_triggers = prev_triggers_er = prev_time = 0.0
    res = {} # get a dict of time:gain pairs
    
    # range ([start,] stop, [step])
    for entry in range(int(n_entries/10), n_entries, int(n_entries/10)):
        tree.GetEntry(entry)
        
        n_triggers, time = branch['scaler'][2], branch['scaler'][7] 
        n_triggers_er = n_triggers**0.5
        rate, rate_er = _calc_rate_and_er(n_triggers, prev_triggers, 
                                          time, prev_time,
                                          n_triggers_er, prev_triggers_er,
                                          time_er, time_er)
        
        n, n_er = val_and_er(n_triggers, prev_triggers, n_triggers_er, prev_triggers_er)
        res[(time, 500)] = (rate, rate_er, n_triggers)
        tree.GetEntry(entry+1)
        prev_triggers, prev_time = branch['scaler'][2], branch['scaler'][7]
        prev_triggers_er = prev_triggers**0.5
    return res


def get_gain_stability_hist_for_file(data, file_id):
    name = "Gain stability, run: %i"%int(file_id)
    # use a TGraphErrors instead
    # res = make_hist(name, mins=mins, maxs=maxs, bins=bins, titles=titles, dim=2)
    x = array('f', [i[0] for i in data.keys()])
    y = array('f', [i[0] for i in data.values()])
    x_er = array('f', [i[1] for i in data.keys()])
    y_er = array('f', [i[1] for i in data.values()])
    
    res = TGraphErrors(len(x), x, y, x_er, y_er)
    res.SetTitle(name)
    res.GetXaxis().SetTitle("Time (ns)")
    res.GetYaxis().SetTitle("Trigger Rate")
    res.SetMinimum(0)
    
    return res


def get_trigger_count_hist_for_file(data, file_id):
    name = "Trigger count, run: %i"%int(file_id)
    # set the minimum x value as half the min time to try and get the bins aligned nicely
    xmin = float(min(data.keys(),key=lambda x:x[0])[0])/2
    # max will return the time,er pair with largest time; which is what we want
    xmax = max(data.keys(),key=lambda x:x[0])[0]
    # whilst the time divisions are not constant the errors are very small
    xbins = len(data)
    titles = ("Time (ns)", "Trigger Count")
    res = make_hist(name, xmin, xmax, titles, xbins)
    print '\n'
    times = data.keys()
    times.sort(key=lambda x:x[0])
    for bin, time in enumerate(times):
        val = data[time][2]
        res.Fill(time[0],val)
    return res


def print_dict_in_key_order(data, tab_char="..", sort_func=None, _tab=''):
    # print the results
    keys = list(data.keys())
    keys.sort(sort_func)
    for i in keys:
        print _tab, i
        if hasattr(data[i], 'keys'):
            print_dict_in_key_order(data[i], tab_char, sort_func, _tab+tab_char)
        else:
            print _tab+tab_char, data[i]


def print_times(in_data):
    for file_id, data in in_data.items():
        print file_id
        prev = 0
        times = [i[0] for i in data.keys()]
        times.sort()
        for time in times:
            print '\t', time-prev
            prev = time


def main():
    res = {'data':{}}
    for file_id, file_data in files_info.items():
        print "\n", file_id
        name = file_prefix + file_id + file_suffix
        tfile, tree, branch = get_tfile_tree_and_branch(name, **file_data)
        key = int(file_id)
        res['data'][key] = get_gain_stability_dict(tree, branch)
        tfile.Close()
    
    canvas = make_canvas("Gain Stability", 3,2, True)
    # add the histograms to the dictionary
    res.update({'gain_hist':{}, 'count_hist':{}})
    axis = []
    for pad_id, (file_id, data) in enumerate(res['data'].items(), 1):
        res['gain_hist'][file_id] = get_gain_stability_hist_for_file(data, file_id)
        res['count_hist'][file_id] = get_trigger_count_hist_for_file(data, file_id)
        pad = canvas.cd(pad_id)
        res['gain_hist'][file_id].Draw("AP")
        canvas.Update()
        
        rightmax = 1.1*res['count_hist'][file_id].GetMaximum()
        rightmin = res['count_hist'][file_id].GetMinimum() + 1
        scale = pad.GetUymax()/rightmax
        res['count_hist'][file_id].SetLineColor(2)
        res['count_hist'][file_id].Scale(scale)
        res['count_hist'][file_id].Draw("SAME")
            
        hist_axis = TGaxis(pad.GetUxmax(), pad.GetUymin(), 
                          pad.GetUxmax(), pad.GetUymax(), 
                          rightmin, rightmax, 110,"+L")
                          
        print res['count_hist'][file_id].GetBinContent(1), res['count_hist'][file_id].GetBinContent(9)
        hist_axis.SetLineColor(2)
        hist_axis.SetLabelColor(2)
        hist_axis.SetLabelSize(.035)
        hist_axis.SetTitle("Trigger count")
        hist_axis.SetTitleColor(2)
        hist_axis.SetTitleSize(.035)
        hist_axis.SetTitleOffset(1.2)
        hist_axis.Draw()
        axis.append(hist_axis)
        canvas.Update()
    
    canvas.SaveAs("images/gain_stability.svg")
    canvas.SaveAs("images/gain_stability.eps")
        
    from time import sleep
    sleep (10)
    

if __name__=="__main__":
    main()