"""
  data_analysis_core.py
  scripts
  
  Created by Sam Cook on 2013-05-28.
"""

from root_utilities import make_hist

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
    
def make_ch_hists(tree, channels, l_bound=-20000, u_bound=20000, bins=400, titles=("TDC - TDC0 (ns)", "Count")):
  res = {}
  for ch in channels:
    name = "dt_file:{}_ch:{}".format(tree.file_id, ch)
    res[ch] = make_hist(name, mins=l_bound, maxs=u_bound, bins=bins, titles=titles)
    res[ch].file_id = tree.file_id
    res[ch].ch = ch
  return res