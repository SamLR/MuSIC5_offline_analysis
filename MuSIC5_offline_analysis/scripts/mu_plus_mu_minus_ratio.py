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

from ROOT import TFile, TF1
from time import sleep
from inspect import getsource

from root_utilities import make_hist, make_canvas


# ===================
# = Global settings =
# ===================
# bin_width = 10
bin_width = 100
# bin_width = 30
# func_fmt = "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4]) + [5]*sin([6]*x)"
func_fmt = "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])"
#                      Name        initial val                           lower              upper bounds
fitting_parameters =(("N_{b}",    lambda x: float(x.GetMaximum()/50.0), lambda x: 0.0   , lambda x: x.GetMaximum()**2 ),
                     ("N_{c}",    lambda x: float(x.GetMaximum()),      lambda x: 0.0   , lambda x: x.GetMaximum()**2 ),
                     # ("#tau_{c}", lambda x: 163.5,                      lambda x: 162.5 , lambda x: 164.2             ),
                     ("#tau_{c}", lambda x: 163.5,                      lambda x: 50.0  , lambda x: 1000.0            ),
                     ("N_{f}",    lambda x: float(x.GetMaximum()/2.0),  lambda x: 0.0   , lambda x: x.GetMaximum()**2 ),
                     ("#tau_{f}", lambda x: 2200.0,                     lambda x: 1000.0, lambda x: 20000.0           ))
                     # ("#theta",   lambda x: 20.0,                       lambda x: 0.0   , lambda x: 20000.0           ),
                     # ("N_{sin}",  lambda x: float(x.GetMaximum()/100.0),lambda x: 0.0   , lambda x: 20000.0           ))

# ================
# = Misc gubbins =
# ================
# Useful little function to get nice looking print out
def pretty_val_and_er(param, val_places="7.1", er_places="7.1"):
  return u"{%s[0]: >%se} \xb1 {%s[1]: <%se} "%(param, val_places, param, er_places)
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
def process_data_file(file_id, channels):
  tree = get_tree_in_file(file_id)
  print "Tree has: {} entries".format(tree.GetEntries())
  hists = get_ch_dt_hists(tree, channels)
  can = fit_dbl_exp(hists, file_id)
  integrals = get_all_integrals(hists)
  print_results(hists, file_id, integrals)
  return can, integrals

# =================
# = Load the Tree =
# =================
@EntryLogger
def get_tree_in_file(file_id):
  file_fmt = "../../../converted_data/run00{}_converted.root"
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
    # if (event_id>2000): # FAST
    #   print "EARLY BREAK!"
    #   break
    if (event_id%1000000 == 0): 
      print event_id
    else:
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
    func = get_func(hist, ch)
    fit_res = hist.Fit(func,"MERS")#"MERNS")
    hist.param = get_parameters(func)
    hist.covar_matrix = fit_res.GetCovarianceMatrix()
    pad.Update()
  canvas.Update()
  return canvas

def get_func(hist, ch):
  name = "func_file:{}_ch:_{}".format(hist.file_id, ch)

  func = TF1(name, func_fmt, 50, 20000)
                       
  for parN, (name, initial, lower_limit, upper_limit) in enumerate(fitting_parameters):
    func.SetParName(parN, name)
    func.SetParameter(parN, initial(hist))
    func.SetParLimits(parN, lower_limit(hist), upper_limit(hist))
    
  return func

def clean_par_name(name):
  name = name.replace("}", "")
  name = name.replace("{", "")
  name = name.replace("#", "")
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
  total_ints = {"c":[0.0, 0.0], "f":[0.0, 0.0], "R":[0.0, 0.0]}
  for hist in hists.values():
    for mu_type in ("c", "f"):
      count_and_er = get_integral_and_er_for_muon_type(hist, mu_type)
      hist.param[mu_type] = count_and_er
      total_ints[mu_type][0] += count_and_er[0]
      total_ints[mu_type][1] += (count_and_er[1]/count_and_er[0])**2
  # Correctly calculate the errors
  for mu_type in ("c", "f"):
    total_ints[mu_type][1] = total_ints[mu_type][0] * total_ints[mu_type][1]**0.5
  
  total_ints["R"][0] = total_ints["c"][0]/total_ints["f"][0]
  dc_c = (total_ints["c"][1]/total_ints["c"][0])**2
  df_f = (total_ints["f"][1]/total_ints["f"][0])**2
  total_ints["R"][1] = total_ints["R"][0]*(dc_c + df_f)**0.5
  return total_ints

def get_integral_and_er_for_muon_type(hist, mu_type):
  mu_type = mu_type.lower()
  
  scale = hist.param["N_c"]   if (mu_type == "c") else hist.param["N_f"]
  tau   = hist.param["tau_c"] if (mu_type == "c") else hist.param["tau_f"]
  # Root takes submatrix selections in an x1,x2,y1,y2 form (0,0)=N_b
  sub_matrix = (1,2,1,2) if (mu_type == "c") else (3,4,3,4)
  covar_sub  = hist.covar_matrix.GetSub(*sub_matrix)
  
  func = get_tmp_func(scale, tau)
  
  integral    = func.Integral(0, 20000)
  integral_er = func.IntegralError(0, 20000, func.GetParameters(), covar_sub.GetMatrixArray())
  return integral, integral_er

def get_tmp_func(scale, tau):
  res = TF1("tmp_func", "[0]*exp(-x/[1])", 0, 20000)
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
  data_list = list(map(lambda x:clean_par_name(x[0]), fitting_parameters)) + ["c",] + ["f",]
  # Get the format string and add the channel at the start
  table_header, data_fmt = get_table_header_and_fmt_string(data_list, u"ch ", u"{ch} ")
  print table_header
  for ch, hist in hists.items():
    print data_fmt.format(ch=ch, **hist.param)
  print

def get_table_header_and_fmt_string(data_list, header=u"", data_fmt=u"", div=u"| ", val_places="9.1", er_places="7.1"):
  header_width = int(val_places[0])+int(er_places[0])+3
  print header, val_places, er_places
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
  
  data_files = {0.0: (448, ),
                  0.5: (451, 452),
                  1.0: (455, ),
                  5.0: (458, 459)}
  # data_files = {0.5: (451,),} # FAST
  g4bl_file = "~/code/MuSIC/simulation/MuSIC_5_detector_sim/"+\
              "MuSIC5/g4blout/from_hep_1Bn/"+\
              "g4bl_out_36_rotation_30435841_particles.root"
  sim_n_mu = process_g4bl_file(g4bl_file) # FAST

  # channels = ("D1",)  # FAST
  channels = ("D1", "D2", "D3", "D4", "D5")
  canvases  = {}
  integrals = {}
  for degZ, file_roots in data_files.items():
    for file_id in file_roots:
      print file_id
      canvas, file_ints  = process_data_file(file_id, channels)
      img_name = "images/fit_data_file_{}_bin_width_{}".format(file_id, bin_width)
      canvas.SaveAs(img_name+".svg")
      canvas.SaveAs(img_name+".png")
      canvases[file_id]  = canvas
      integrals[file_id] = file_ints
      # return # FAST
      
  print "="*80
  print "Settings:"
  print "\tBin width", bin_width
  print "\tFunc format", func_fmt
  print "\tInitial fit settings:"
  print getsource(fitting_parameters[0][1]) # will print the whole thing
  
  print "="*80
  print "G4BL predicts: "
  for key in ("mu-", "mu+", "ratio"):
    print "\t{:^5s}: ".format(key),
    print pretty_val_and_er("0").format(sim_n_mu[key])
  
  print "Data says: "
  data_header, data_fmt = get_table_header_and_fmt_string( ("c", "f", "R"),\
                          header=u"Run ", data_fmt=u"{file_id} ", val_places="8.2", er_places="8.2")
  print data_header
  for file_id, integral in integrals.items():
    print data_fmt.format(file_id=file_id, **integral)

if __name__=="__main__":
  main()
  
  
  
  

