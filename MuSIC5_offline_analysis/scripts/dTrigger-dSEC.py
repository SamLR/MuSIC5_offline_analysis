"""
Plots dTrigger/dSEC Vs time, as requested by Sato-san

Tue Apr 16 22:59:10 JST 2013

By Sam Cook
"""

# Standard library
from array import array
from time import sleep
# pyRoot
from ROOT import TFile, TTree, TGraph
# my own crap
from root_utilities import make_canvas
from sclr_branch_func import files_info


filefmt = "../../../MuSIC_data_0.5Cu/run{0}.root"

def load_tree_and_file(file_id, file_info):
  filename = filefmt.format(file_id)
  file = TFile(filename, "READ")
  tree = file.Get(file_info['tree_name'])
  tree.file_id = file_id
  tree.branch_name = file_info['branch_name']
  return tree, file
  

def _get_sec(tree):
  return getattr(tree, tree.branch_name)[0]

def _get_trigger(tree):
  return getattr(tree, tree.branch_name)[1]

def _get_time(tree):
  return getattr(tree, tree.branch_name)[7]


def get_dtrigger_dsec(tree, n_divisions):
  # SEC is entry 0, trigger is 1, time is 7

  step = int(tree.GetEntries()/n_divisions)
  # res = {}
  res = []

  tree.GetEntry(0)
  prev_sec, prev_trig = _get_sec(tree), _get_trigger(tree)
  
  for entry in range(step, tree.GetEntries(), step):
    tree.GetEntry(entry)
    sec, trig, = _get_sec(tree), _get_trigger(tree)
    time = _get_time(tree)
    # res [time] = float(trig - prev_trig)/(sec - prev_sec))  
    res.append( (time, float(trig - prev_trig)/(sec - prev_sec)) ) 
    prev_sec, prev_trig = sec, trig
    
  
  return res
  
def get_plot(file_id, data):
  name = "Normalised trigger rate, run: %i"%int(file_id)
  # we don't currently calculate errors so use a TGraph
    
  x = array('d', [i[0] for i in data])
  y = array('d', [i[1] for i in data])
  # x    = array('f', [i[0] for i in data])
  # x_er = array('f', [i[1] for i in data])
  # y    = array('f', [i[2] for i in data])
  # y_er = array('f', [i[3] for i in data])
  
  res = TGraph(len(x), x, y)
  res.Draw("ALP")
  # res = TGraphErrors(len(x), x, y, x_er, y_er)
  res.SetTitle(name)
  res.GetXaxis().SetTitle("Time (ns)")
  res.GetYaxis().SetTitle("Normalised trigger rate")
  
  # res.SetMinimum(0)
  return res
  
  
def draw_pretty_plots(rates):
  canvas = make_canvas("Trigger Rate", 3,2, True)
  # attach all the plots to the canvas to keep them in scope
  canvas.plots = []
  for pad_id, (file_id, data) in enumerate(rates.items(), 1):
    canvas.cd(pad_id)
    canvas.plots.append(get_plot(file_id, data))
    canvas.plots[-1].Draw("ALP")
    canvas.Update()
  # Don't let the canvas go out of scope
  return canvas

def main():
  rates = {}
  # 
  n_divisions = 10
  print "Calculating rates"
  
  for file_id, file_struct in files_info.items():
    tree, file = load_tree_and_file(file_id, file_struct)
    rates [file_id] = get_dtrigger_dsec(tree, n_divisions)
    
    file.Close()
  
  print "Drawing"
  canvas = draw_pretty_plots(rates)
  print "Sleeping"
  sleep(30)
  

if __name__=="__main__":
  main()
  
