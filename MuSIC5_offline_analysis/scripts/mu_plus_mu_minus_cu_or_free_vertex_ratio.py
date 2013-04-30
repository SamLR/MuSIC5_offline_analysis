"""
mu_plus_mu_minus_cu_or_free_vertex_ratio.py

Tabulates the ratio of stopped (decaying) muons (positive
or negative) as well as their decay vertices.

Created by Sam Cook on 2013-04-20.

"""

from ROOT import TFile, gStyle
from root_utilities import make_hist, make_canvas

# from mu_plus_mu_minus_ratio import get_func, clean_par_name, get_parameters, func_fmt,\
from mu_plus_mu_minus_ratio import get_func, clean_par_name, get_parameters,\
                                   fitting_parameters, bin_width, get_tmp_func, \
                                   get_integral_and_error_on_exp, set_param_and_error, \
                                   get_table_header_and_fmt_string, get_ratio

from time import sleep


# func_fmt = "[1]*exp(-x/[2])"
# #                      Name        initial val                           lower              upper bounds
# fitting_parameters =(("N_{f}",    lambda x: float(x.GetMaximum()/2.0),  lambda x: 0.0   , lambda x: x.GetMaximum()**2 ),
#                      ("#tau_{f}", lambda x: 2200.0,                     lambda x: 1900.0 , lambda x: 25000.0           ))

data_dir = "../../../../simulation/MuSIC_5_detector_sim/MuSIC5/output/mu+_mu_ratio/"
target_mat = "Cu"
# ===============
# = Load things =
# ===============
def get_tree(degrader, mu_charge, initial_muons):
  file_name = "{0}{1}_{2}_{3}.root".format(data_dir, mu_charge, degrader, initial_muons)
  file = TFile(file_name, "READ")
  tree = file.Get("truth")
  # Record some metadata (mmm attribute abuse!)
  tree.file_name = file_name
  tree.mu_charge = mu_charge
  tree.degrader  = degrader
  tree.initial_muons = initial_muons
  
  tree.file = file
  return tree
  
# ======================
# = Process the tree =
# ======================
def process_tree(tree, img_name=""):
  tree.muon_counts = loop_over_entries(tree)
  canvas = fit_and_draw_hist(tree.hist)
  if img_name:
    canvas.SaveAs(img_name+".svg")
    canvas.SaveAs(img_name+".png")
  tree.integrals = get_integrals(tree.hist)
  

# ==================
# = Loop over the tree  =
# ==================
def loop_over_entries(tree):
  res = {target_mat:0, "f":0}
  hist = get_hist(tree)
  for entry in tree:
    c, f = get_cu_and_free_decay_counts(entry)
    res[target_mat] += c
    res["f"] += f
    fill_hist(hist, entry)
  tree.hist = hist
  # calculate the errors
  res = {i:(res[i], res[i]**0.5) for i in res}
  return res

def get_hist(tree):
  n_bins = int(40000/bin_width)
  hist_args = {"mins":-20000, "maxs":20000, "bins":n_bins, "titles":("TDC - TDC0 (ns)", "Count")}
  name = "{0} {1}s at a {2}".format(tree.initial_muons, tree.mu_charge, tree.degrader)
  hist = make_hist(name, **hist_args)
  hist.mu_charge = tree.mu_charge
  hist.degrader  = tree.degrader
  hist.initial_muons = tree.initial_muons
  
  return hist

def get_cu_and_free_decay_counts(entry):
  c_count = f_count = 0
  u_muon_ids = []
  d_electron_origins = {} # origin == parent ID & vertex
  # Find all the muons and electrons in the counters
  for hit in range(entry.nhit):
    if not entry.first_step[hit]: # limit double counts
      continue
    
    elif is_upstream_muon(entry, hit):
      u_muon_ids.append( entry.trkid[hit] )
    
    elif is_downstream_electron(entry, hit):
      d_electron_origins[entry.parentid[hit]] = entry.vertex_vol[hit]
      
  # Find all the electron/muon decay pairs and record the vertex
  for parent_id, parent_vertex in d_electron_origins.items():
    if parent_id not in u_muon_ids:
      continue
    
    elif parent_vertex == 2:
      c_count += 1
  
    else:
      f_count += 1
  return c_count, f_count

def fill_hist(hist, entry):
  u_muon_times = {}
  d_electron_times = {} # origin == parent ID & vertex
  # Find all the muons and electrons in the counters
  for hit in range(entry.nhit):
    if not entry.first_step[hit]: # limit double counts
      continue
    
    elif is_upstream_muon(entry, hit):
      u_muon_times[entry.trkid[hit]] = entry.tof[hit]
    
    elif is_downstream_electron(entry, hit):
      d_electron_times[entry.parentid[hit]] = entry.tof[hit]
      
  # Find all the electron/muon decay pairs and record the vertex
  for parent_id, time in d_electron_times.items():
    if parent_id not in u_muon_times:
      continue
    
    else:
      dt = time-u_muon_times[parent_id]
      hist.Fill(dt)
      # if dt < 10:
     #    print u_muon_times
     #    print d_electron_times
  # print

def is_upstream_muon(entry, hit):
  is_muon     = (abs(entry.pdgid[hit]) == 13)
  is_upstream = (entry.counter[hit] == 1)
  return is_muon and is_upstream
  
  
def is_downstream_electron(entry, hit):
  is_electron   = (abs(entry.pdgid[hit]) == 11)
  is_downstream = (entry.counter[hit] == 3)
  return is_downstream and is_electron

# =====================
# = Fit the histogram =
# =====================
def fit_and_draw_hist(hist):
  canvas = make_canvas(hist.mu_charge + hist.degrader,resize=True)
  func = get_func(hist,hist.mu_charge + hist.degrader)
  fit_res = hist.Fit(func,"MERS")#"MERNS")
  hist.param = get_parameters(func)
  # hist.covar_matrix = fit_res.GetCovarianceMatrix()
  canvas.Update()
  return canvas
  
# ===============================
# = Now calculate the integrals =
# ===============================
def get_integrals(hist):
  res = {}
  for mu_type in (target_mat, "f"):
    scale = hist.param["N_"+mu_type]
    tau   = hist.param["tau_"+mu_type]
    count_and_er = get_integral_and_error_on_exp(scale, tau)
    hist.param[mu_type] = count_and_er
    res[mu_type] = count_and_er
  return res

def calculate_ratio_for_degrader(degrader_vals, count_type="count"):
  target_component = degrader_vals["mu-"][count_type][target_mat]
  
  free_component = [0.0, 0.0]
  for charge in degrader_vals:
    for fit_type in degrader_vals[charge][count_type]:
      if (fit_type == target_mat) and (charge == "mu-"): continue
      val, er = degrader_vals[charge][count_type][fit_type]
      free_component[0] += val
      free_component[1] += (er/val)**2
  
  return get_ratio(target_component, free_component)
      
  

def main():
  
  degraders = ("5mm_Air", "0.5mm_Aluminium", "1mm_Aluminium", "5mm_Aluminium")
  # degraders = ("5mm_Air",) # FAST
  mu_types   = (("mu+", 86710), ("mu-", 9009))
  # mu_types   = (("mu+", 86710),) # FAST
  
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
  
  process_res = {i:{} for i in degraders}
  for deg in degraders:
    for mu_charge, g4bl_count in mu_types:
      tree = get_tree(deg, mu_charge, g4bl_count)
      save_name = "images/sim_data_{}_{}".format(mu_charge, deg)
      # save_name = ""
      process_tree(tree, save_name)
      process_res[deg][mu_charge] = {"count":tree.muon_counts, "int":tree.integrals}

  ratios = {i:{target_mat:[0.0, 0.0], "free":[0.0, 0.0]} for i in degraders}
  data_list = ("count_target", "count_f", "int_target", "int_f", "int_ratio", "count_ratio")
  table_header, table_fmt = get_table_header_and_fmt_string(data_list, \
            header=u"Degrader | charge ", data_fmt=u"{deg: ^8} | {charge: ^6} ", val_places="9.1", er_places="9.2")

  
  print table_header
  for deg in process_res:
    for charge in process_res[deg]:
      counts = process_res[deg][charge]["count"]
      ints   = process_res[deg][charge]["int"]
      print table_fmt.format(deg = deg[:8], charge = charge, 
                             count_target = counts[target_mat], count_f = counts["f"],
                             int_target   = ints[target_mat],   int_f   = ints["f"],
                             int_ratio    = get_ratio(ints[target_mat], ints["f"]),
                             count_ratio  = get_ratio(counts[target_mat], counts["f"]) )
  
  print "Inclusive ratios"
  print "{: ^17s} | {: ^20s}".format("Degrader", "Ratio")
  for deg in process_res:
    # print u"\t\t Ratio {: >6.3f}".format(float(ratios[deg][0])/ratios[deg][1])
    print u"{: ^17s} | {: >9.4f}\xb1{: <9.5f}".format(deg, *calculate_ratio_for_degrader(process_res[deg]))

if __name__=="__main__":
  main()