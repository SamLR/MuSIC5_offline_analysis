"""

Calculate the ratio of mu+ to mu- in data and simulation of MuSIC5

General Alg:
   * read in simulation
   * finds mu in U
   * e in D
   * classify e by vertex in Cu or not
   * count abundancies of both
   * read in data
   * plot histograms
   * fit
   * read out Nc & Nf
   * Plot ratio of Nc:Nf compared to (sim) 
     Nc:Nf (mu-) and Nc:Nf (mu+) for degraderZ



Created on 2013-04-18 by Sam Cook

"""

from ROOT import TFile, TF1, gStyle
from time import sleep
from inspect import getsource

from root_utilities import make_hist, make_canvas


# ===================
# = Global settings =
# ===================
FAST=False
bin_width = 100
func_fmt = "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])"
target_mat = "Cu"
#                      Name        initial val                           lower              upper bounds
fitting_parameters =(("N_{b}",            lambda x: float(x.GetMaximum()/50.0), lambda x: 0.0      , lambda x: x.GetMaximum()**2 ),
                     ("N_"+target_mat,    lambda x: float(x.GetMaximum()),      lambda x: 0.0      , lambda x: x.GetMaximum()**2 ),
                     ("#tau_"+target_mat, lambda x: 163.5,                      lambda x: 162.5    , lambda x: 164.2             ),
                     ("N_{f}",            lambda x: float(x.GetMaximum()/2.0),  lambda x: 0.0      , lambda x: x.GetMaximum()**2 ),
                     ("#tau_{f}",         lambda x: 2196.9811,                  lambda x: 2196.9789, lambda x: 2196.9833         ))
# file_fmt = 
file_fmt = "../../../converted_data/run00{}_converted.root" if target_mat=="Cu" else "../../../converted_Mg_data/run00{}_converted.root"
# ================
# = Misc gubbins =
# ================
# Useful little function to get nice looking print out
def pretty_val_and_er(param, val_places="10.1", er_places="10.2"):
  # return u"{%s[0]: >%se} \xb1 {%s[1]: <%se} "%(param, val_places, param, er_places)
  return u"{%s[0]: >%sf} \xb1 {%s[1]: <%sf} "%(param, val_places, param, er_places)
  
# Decorator class for logging entry/exit of functions
class EntryLogger(object):
  """Logs entries to a function"""
  def __init__(self, f):
    self.func = f
  
  def __call__(self, *args, **kwargs):
    print "Entering: {}".format(self.func.__name__)
    res =  self.func(*args, **kwargs)
    print "Exiting {}".format(self.func.__name__)
    return res
# =========================
# = Process the G4BL file =
# =========================
@EntryLogger
def process_g4bl_file(file_name):
  file = TFile(file_name, "READ")
  tree = file.Get("t")
  n_mu_neg  = int(tree.GetEntries("PDGid==13"))
  er_mu_neg = float(n_mu_neg)**0.5
  n_mu_pos  = int(tree.GetEntries("PDGid==-13"))
  er_mu_pos = float(n_mu_pos)**0.5
  ratio     = float(n_mu_neg)/n_mu_pos
  er_ratio  = ratio*((er_mu_pos/n_mu_pos)**2 + (er_mu_neg/n_mu_neg)**2)**0.5
  return {"mu-":(n_mu_neg, er_mu_neg), "mu+":(n_mu_pos, er_mu_pos), "ratio":(ratio, er_ratio)}

# =================================
# = Process data file (top level) =
# =================================
@EntryLogger
def process_data_file(file_id, channels, save_name=""):
  tree = get_tree_in_file(file_id)
  print "Tree has: {} entries".format(tree.GetEntries())
  hists = get_ch_dt_hists(tree, channels)
  can = fit_dbl_exp(hists, file_id)
  if save_name: 
    can.SaveAs(save_name+".svg")
    can.SaveAs(save_name+".png")
  integrals = get_all_integrals(hists)
  print_results(hists, file_id, integrals)
  return integrals

# =================
# = Load the Tree =
# =================
@EntryLogger
def get_tree_in_file(file_id):
  file_name = file_fmt.format(file_id)
  
  file = TFile(file_name, "READ")
  tree = file.Get("Trigger")
  
  tree.file = file
  tree.file_id = file_id
  return tree


# ==========================================================
# = Create the dt histograms for each channel in each tree =
# ==========================================================
@EntryLogger
def get_ch_dt_hists(tree, channels):
  assign_leaves(tree, channels)
  hists = make_ch_hists(tree, channels)
  for event_id, event in enumerate(tree):
    if (event_id>200000 and FAST): 
      print "EARLY BREAK!"
      break
    if (event_id%1000000 == 0): 
      print event_id
    for ch in channels:
      for hit in range(int(tree.nHIT[ch]() )):
        hists[ch].Fill( tree.TDC[ch](hit) )
  return hists

def assign_leaves(tree, channels):
  """
  This is mostly a hack to make the leaves behave like
  native attributes of the tree.
  """
  tree.branch    = {}
  tree.TDC_leaf  = {}
  tree.TDC       = {}
  tree.nHIT_leaf = {}
  tree.nHIT      = {}
  # Assign everything
  for ch in channels:
    tree.branch[ch] = tree.GetBranch(ch)
    # Add the leaves to their dictionaries
    tree.nHIT_leaf[ch] = tree.branch[ch].GetLeaf("nHITS")
    tree.TDC_leaf[ch]  = tree.branch[ch].GetLeaf("TDC")
    # Add accessor functions, TDC needs an array index. 
    tree.nHIT[ch]      = tree.nHIT_leaf[ch].GetValue
    tree.TDC[ch]       = tree.TDC_leaf[ch].GetValue
    

def make_ch_hists(tree, channels):
  res = {}
  n_bins = int(40000.0/bin_width)
  hist_args = {"mins":-20000, "maxs":20000, "bins":n_bins, "titles":("TDC - TDC0 (ns)", "Count")}
  for ch in channels:
    name = "dt_file:{}_ch:{}".format(tree.file_id, ch)
    res[ch] = make_hist(name, **hist_args)
    res[ch].file_id = tree.file_id
    res[ch].ch = ch
  return res


# ===========================================
# = Fit the double exponentials to the hist =
# ===========================================
@EntryLogger
def fit_dbl_exp(hists, file_id):
  canvas = make_canvas(str(file_id), n_x=3, n_y=2, resize=True)
  for pad_id, (ch, hist) in enumerate(hists.items(), 1):
    pad = canvas.cd(pad_id)
    func_name = "func_file:{}_ch:_{}".format(hist.file_id, ch)
    func = get_func(hist, func_name)
    fit_res = hist.Fit(func,"MERS")#"MERNS")
    hist.param = get_parameters(func)
    # hist.covar_matrix = fit_res.GetCovarianceMatrix()
    pad.Update()
  canvas.Update()
  return canvas

def get_func(hist, name):

  func = TF1(name, func_fmt, 50, 20000)
                       
  for parN, (name, initial, lower_limit, upper_limit) in enumerate(fitting_parameters):
    func.SetParName(parN, name)
    func.SetParameter(parN, initial(hist))
    func.SetParLimits(parN, lower_limit(hist), upper_limit(hist))
    
  return func

def clean_par_name(string, char_to_del="{}#"):
  for char in char_to_del:
    name = name.replace(char, "")
  return name

def get_parameters(func):
  res = {}
  for par_id in range(func.GetNpar()):
    par_name = func.GetParName(par_id)
    par_name = clean_par_name(par_name)
    res[par_name] = (func.GetParameter(par_id), func.GetParError(par_id))
  return res
  
# =======================
# = Calculate Nc and Nf =
# =======================
@EntryLogger
def get_all_integrals(hists):
  total_ints = {"f":[0.0, 0.0], target_mat:[0.0, 0.0]}
  for hist in hists.values():
    for mu_type in total_ints:
      # count_and_er = get_integral_of_sub_fit(hist, mu_type)
      scale = [float(val) for val in hist.param["N_"+mu_type]]
      tau   = [float(val) for val in hist.param["tau_"+mu_type]]
      integral, int_er = get_integral_and_error_on_exp(scale, tau)
      hist.param[mu_type] = integral, int_er
      total_ints[mu_type][0] += integral
      if integral == 0: 
        print "WARNING: integral = 0"
        total_ints[mu_type][1] += 0.0 # this shouldn't really happen
      else:
        total_ints[mu_type][1] += (int_er/integral)**2
        
  # Correctly calculate the errors
  for key in total_ints:
    total_ints[key][1] = total_ints[key][0] * total_ints[key][1]**0.5
  
  total_ints["R"] = get_ratio(total_ints[target_mat], total_ints["f"])
  return total_ints

def get_ratio(numerator_and_er, denom_and_er):
  ratio = numerator_and_er[0]/denom_and_er[0]
  d_numerate = (numerator_and_er[1]/numerator_and_er[0])**2
  d_denominator = (denom_and_er[1]/denom_and_er[0])**2
  
  ratio_er = ratio * (d_numerate + d_denominator) **0.5
  return ratio, ratio_er


def get_integral_and_error_on_exp(scale_and_er, tau_and_er, start=50, stop=20000):
  from math import exp
  def exp_integral(scale, tau, start, stop):
    return scale*tau*(exp(-float(start)/tau) - exp(-float(stop)/tau))
  integral = exp_integral(scale_and_er[0], tau_and_er[0], start, stop)

  d_scale = (scale_and_er[1]/scale_and_er[0]) ** 2
  d_tau   = (tau_and_er[1]/tau_and_er[0]) ** 2
  return integral/bin_width, (integral*(d_scale + d_tau)**0.5)/bin_width
  
  # func = get_tmp_func(scale_and_er, tau_and_er, start, stop)
  # integral = func.Integral(start, stop)
  # d_scale = (scale_and_er[1]/scale_and_er[0]) ** 2
  # d_tau   = (tau_and_er[1]/tau_and_er[0]) ** 2
  # return integral, integral*(d_scale + d_tau)**0.5

def get_tmp_func(scale, tau, start, stop):
  res = TF1("tmp_func", "[0]*exp(-x/[1])", start, stop)
  set_param_and_error(res, 0, *scale)
  set_param_and_error(res, 1, *tau)
  return res

def set_param_and_error(func, param, val, er):
  func.SetParameter(param, val)
  func.SetParError (param, er)
# ==================
# = Pretty Printer =
# ==================
def print_results(hists, file_id, integrals):
  data_list = list(map(lambda x:clean_par_name(x[0]), fitting_parameters)) + [target_mat,] + ["f",]
  # Get the format string and add the channel at the start
  table_header, data_fmt = get_table_header_and_fmt_string(data_list, u"ch ", u"{ch} ")
  print table_header
  for ch, hist in hists.items():
    print data_fmt.format(ch=ch, **hist.param)
  print

def get_table_header_and_fmt_string(data_list, header=u"", data_fmt=u"", div=u"| ", val_places="9.1", er_places="7.1"):
  header_width = int(val_places[0])+int(er_places[0])+3
  for item in data_list:
    header   += div + u"{:^%is} "%header_width
    data_fmt += div + pretty_val_and_er(item, val_places, er_places)
  header = header.format(*data_list)
  return header, data_fmt
  
# =================
# = Main function =
# =================
def main():
  degraders = (0.0, 0.5, 1.0, 5.0)
  # degraders = (2.5, 5, 7.5, 15)
  # data_files = {2.5:(468,), 5:(466,), 7.5:(464,), 15:(508,)}
    # 
                
  # data_files = {0.5: (451,),} # FAST  
  # channels = ("D1",)  # FAST
  channels = ("D1", "D2", "D3", "D4", "D5")
  data_files = file_stats = {}
  
  if target_mat == "Cu":
    file_stats = {448:{ 'time': 9221, 'current':0.0153375  , 'acceptance':0.087},
                  451:{ 'time': 1001, 'current':0.0154625  , 'acceptance':0.077},
                  452:{ 'time': 4944, 'current':0.013132143, 'acceptance':0.077},
                  455:{ 'time': 6307, 'current':0.013321429, 'acceptance':0.069},
                  458:{ 'time': 5144, 'current':0.013625   , 'acceptance':0.045},
                  459:{ 'time': 2452, 'current':0.012383929, 'acceptance':0.045},}
    data_files = {0.0: (448, ), 0.5: (451, 452), 1.0: (455, ), 5.0: (458, 459)}
  else:
    file_stats = {464: {'time': 5884,  'current':0.4096, 'acceptance':0.087},
                  466: {'time': 7220,  'current':0.3477, 'acceptance':0.087},
                  468: {'time': 13460, 'current':0.3220, 'acceptance':0.087},
                  508: {'time': 4129,  'current':0.3   , 'acceptance':0.087}}
    data_files = {2.5:(468,), 5:(466,), 7.5:(464,), 15:(508,)}
                
  g4bl_file = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/"+\
              "MuSIC5/g4blout/from_hep_1Bn/"+\
              "g4bl_out_36_rotation_30435841_particles.root"
  sim_n_mu = process_g4bl_file(g4bl_file) # FAST
  
  
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
  
  integrals = {}
  for degZ, file_roots in data_files.items():
    for file_id in file_roots:
      print file_id
      img_name = u"images/fit_data_file_{}_bin_width_{}_{}".format(file_id, bin_width, target_mat) if not FAST else ""
      file_ints  = process_data_file(file_id, channels, img_name)
      integrals[file_id] = file_ints
    if FAST: break
      
      
  print "="*80
  print "Settings:"
  print "\tBin width", bin_width
  print "\tFunc format", func_fmt
  print "\tInitial fit settings:"
  print getsource(fitting_parameters[0][1]) # will print the whole thing
  print "\tFile info", 
  for i,j in file_stats.items(): print i, j
  print "="*80
  print "G4BL predicts: "
  for key in  ("mu-", "mu+", "ratio"):
    print "\t{:^5s}: ".format(key),
    print pretty_val_and_er(key, "8.2", "8.2").format(**sim_n_mu)
  
  print "Data says: "
  data_header, data_fmt = get_table_header_and_fmt_string( (target_mat, "f", "R"),\
  # data_header, data_fmt = get_table_header_and_fmt_string( ("Cu", "f", "R"),\
                          header=u"Run ", data_fmt=u"{file_id} ", val_places="11.3", er_places="11.3")
  print data_header
  for file_id, int_and_er in integrals.items():
    print data_fmt.format(file_id=file_id, **int_and_er)
  
  print "\nAs normalised rates: (integral)/(time (s)*current (nA)*acceptance)"
  print "Mg data for 15mm is missing proton current (assumed as 0.3nA), acceptances need to be calculated"
  
  data_header, data_fmt = get_table_header_and_fmt_string( ("rate_target", "rate_f"), header=u"Run ", data_fmt=u"{file_id} ")
  print data_header
  for file_id, integral in integrals.items():
    # print integral
    rate_target, rate_f = [0,0], [0,0]
    rate_target[0] = float(integral[target_mat][0])/(file_stats[file_id]['time']*file_stats[file_id]['current']*file_stats[file_id]['acceptance'])
    rate_target[1] = float(integral[target_mat][1])/(file_stats[file_id]['time']*file_stats[file_id]['current']*file_stats[file_id]['acceptance'])
    rate_f[0] = float(integral["f"][0])/(file_stats[file_id]['time']*file_stats[file_id]['current']*file_stats[file_id]['acceptance'])
    rate_f[1] = float(integral["f"][1])/(file_stats[file_id]['time']*file_stats[file_id]['current']*file_stats[file_id]['acceptance'])
    print data_fmt.format( file_id=file_id, rate_target=rate_target, rate_f=rate_f)

if __name__=="__main__":
  main()
  
  
  
  

