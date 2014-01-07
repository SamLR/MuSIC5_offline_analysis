"""
Measure the gain stability over time by comparing the number of triggers
counted.
"""

# from sclr_branch_func import * 
from root_utilities import make_canvas, make_hist, get_tree_from_file
from ROOT import TGraphErrors, TGaxis, gStyle, TF1
from array import array
from math import log

# mmmm pollute that global namespace!
time_er = 0.500
val_and_er = lambda x,y,x_er, y_er: (x-y, (x-y)*(x_er**2 + y_er**2)**0.5)

file_prefix = "../../../MuSIC_data_0.5Cu/run"
file_suffix = ".root"
file_ids    = ("448", "00451", "00452", "00455", "00458", "00459") 

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
    
    # work in kcounts
    rate = ab/(cd*1000)
    # rate_er = rate * ( (ab_er/ab)**2 + (cd_er/cd)) ** 0.5
    # The error on the rate is the sqrt of the difference. i.e. the error on this count
    rate_er = (ab**0.5)/(cd*1000)
    return rate, rate_er

def load_branch(tree, file_id):
  # we only need to load one branch
  if file_id == "448":
    branch_name,  leaf_name = "Scaler", "scaler" 
  else:
    branch_name = leaf_name = "SCLR"
  
  tree.branch = tree.GetBranch(branch_name)
  tree.leaf = tree.branch.GetLeaf(leaf_name)
  # Force evaluation at call, convert time to seconds
  tree.time = lambda : (tree.leaf.GetValue(7)/1000)
  # want the number of potential triggers
  tree.triggers = lambda : tree.leaf.GetValue(2) 
  # tree.triggers = lambda : tree.leaf.GetValue(1)

def get_gain_stability_dict(tree):
    # open file
    # step through entries
    # for each entry find (U&&!D - U&&!D_previous)/dt
    # NB scaler[2] == U&&!D
    #    scaler[7] == time
    n_entries = tree.GetEntries()
    prev_triggers = prev_triggers_er = prev_time = 0.0
    res = {} # get a dict of time:gain pairs
    
    # range ([start,] stop, [step])
    # for entry in range(int(n_entries/10), n_entries, int(n_entries/10)):
    # for entry in range(1, n_entries, 20):
    # print "here we go"
    # for entry in range(0, 4):
    for entry in range(n_entries/100, n_entries, n_entries/100):
        tree.GetEntry(entry)
        # print tree.triggers(), tree.time()
        # continue
        n_triggers, time = tree.triggers(), tree.time()
        n_triggers_er = n_triggers**0.5
        rate, rate_er = _calc_rate_and_er(n_triggers, prev_triggers, 
                                          time, prev_time,
                                          n_triggers_er, prev_triggers_er,
                                          time_er, time_er)
        
        n, n_er = val_and_er(n_triggers, prev_triggers, n_triggers_er, prev_triggers_er)
        res[(time,0)] = (rate, rate_er, n_triggers)
        # tree.GetEntry(entry+1)
        # prev_triggers, prev_time = tree.triggers(), tree.time()
        prev_triggers, prev_time = n_triggers, time
        prev_triggers_er = prev_triggers**0.5
    return res


def get_gain_stability_hist_for_file(data, file_id):
    name = "Trigger rate, run: %i"%int(file_id)
    # use a TGraphErrors instead
    # res = make_hist(name, mins=mins, maxs=maxs, bins=bins, titles=titles, dim=2)
    x = array('f', [(i[0]) for i in data.keys()])
    y = array('f', [i[0] for i in data.values()])
    x_er = array('f', [0 for i in data.keys()])
    y_er = array('f', [i[1] for i in data.values()])
    
    res = TGraphErrors(len(x), x, y, x_er, y_er)
    res.SetTitle(name)
    res.GetXaxis().SetTitle("Time (s)")
    res.GetYaxis().SetTitle("Trigger Rate (x10^{3} count/s)")
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
    # res = make_hist(name, xmin, xmax, titles, xbins)
    res = make_hist(name, 0, xmax, titles, xbins)
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

def move_stats_box(tgraph, point1, point2):
    stats_box = tgraph.GetListOfFunctions().FindObject("stats")
    stats_box.SetX1NDC(point1[0])
    stats_box.SetY1NDC(point1[1])
    stats_box.SetX2NDC(point2[0])
    stats_box.SetY2NDC(point2[1])

def set_axis_offset_size_color(axis,offset,size,color):
    axis.SetLabelColor(color)
    axis.SetLabelSize(size)
    axis.SetTitleColor(color)
    axis.SetTitleSize(size)
    axis.SetTitleOffset(offset)


def draw_gain_and_count_hist(gain_hist, count_hist, canvas, pad_id, color=4,font_size=0.035, title_offset=1.3):
    pad = canvas.cd(pad_id)
    gain_hist.SetMaximum(2.3)
    set_axis_offset_size_color(gain_hist.GetXaxis(),title_offset,font_size, 1)
    set_axis_offset_size_color(gain_hist.GetYaxis(),title_offset,font_size, 1)
    gain_hist.Draw("AP")
    pad.Update()
    move_stats_box(gain_hist,(0.55,0.75),(0.9,0.9))
    
    # rightmax = count_hist.GetMaximum() * 1.3
    # rightmin = count_hist.GetMinimum()
    # scale    = pad.GetUymax()/rightmax
    # count_hist.SetLineColor(color)
    # count_hist.Scale(scale)
    # count_hist.Draw("SAME")
    # tgaxis_args = (pad.GetUxmax(), pad.GetUymin(), 
    #                pad.GetUxmax(), pad.GetUymax(), 
    #                rightmin, rightmax, 110,"+L")
    # hist_axis = make_pretty_axis(tgaxis_args,color,font_size,title_offset)
    # hist_axis.Draw()
    # # need to keep hist_axis in scope so 
    # # attach it as an attribute to the canvas
    # setattr(canvas,'axis_'+str(pad_id),hist_axis)
    canvas.Update()


def main():
    gStyle.SetOptFit()
    res = {'data':{}}
    for f_id in file_ids:
        print "Processing", f_id
        filename = file_prefix + f_id + file_suffix
        treename = "ts" if f_id == "448" else "Scaler"
        
        tree = get_tree_from_file(treename, filename)
        print tree.filename, tree
        load_branch(tree, f_id)
        # tfile, tree, branch = get_tfile_tree_and_branch(name, **file_data)
        key = int(f_id)
        res['data'][key] = get_gain_stability_dict(tree)
        # tfile.Close()
    
    canvas = make_canvas("Gain Stability", 3,2, True)
    # add the histograms to the dictionary
    res.update({'gain_hist':{}, 'count_hist':{}})
    for pad_id, (file_id, data) in enumerate(res['data'].items(), 1):
        gain_hist  = get_gain_stability_hist_for_file(data, file_id)
        count_hist = get_trigger_count_hist_for_file(data, file_id)
        
        full_range = max(data.keys())[0] - min(data.keys())[0]
        # Fit the central 80%
        fit_min = full_range * 0.05
        fit_max = full_range * 0.95
        print fit_min, fit_max
        
        # gain_hist.Fit("pol0") # attempt to fit the gain with a flat function
        gain_hist.Fit("pol0", "", "", fit_min, fit_max) # attempt to fit the gain with a flat function
        
        draw_gain_and_count_hist(gain_hist, count_hist, canvas, pad_id)
        
        res['gain_hist'][file_id] = gain_hist
        res['count_hist'][file_id] = count_hist
    
    canvas.SaveAs("images/gain_stability.svg")
    canvas.SaveAs("images/gain_stability.eps")
    
    print "sleep now!"
    
    from time import sleep
    sleep (20)
    

if __name__=="__main__":
    main()

  