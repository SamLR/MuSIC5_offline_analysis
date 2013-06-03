"""
Calculate the dead time for each run by dividing the number of triggers
counted by the scaler by the number of possible triggers.
"""

from root_utilities import get_tree_from_file
from ValueWithError import ValueWithError

file_name_fmt = "/Users/scook/code/MuSIC/offline_analysis_music5/MuSIC_data_0.5Cu/run{run_id}.root"
run_ids = (448, 451, 452, 455, 458, 459)

def assign_leaf(tree, branch_name, leaf_name):
  """
  This is mostly a hack to make the leaves behave like
  native attributes of the tree.
  """
  tree.branch = tree.GetBranch(branch_name)
  # Add the leaves to their dictionaries
  tree.scaler_leaf = tree.branch.GetLeaf(leaf_name)
  # Add accessor functions, TDC needs an array index. 
  tree.scaler = lambda x: float(tree.scaler_leaf.GetValue(x))

def get_dead_time_from_file(run_id):
  if run_id == 448:
    tree_name, branch_name, leaf_name = "ts", "Scaler", "scaler"
  else:
    run_id = "00{}".format(run_id)
    tree_name, branch_name, leaf_name = "Scaler", "SCLR", "SCLR"
  print_fmt ="Opening file with id:{}, tree:{}, branch:{}, leaf:{}"
  print print_fmt.format(run_id, tree_name, branch_name, leaf_name)
  
  file_name = file_name_fmt.format(run_id=run_id)
  tree = get_tree_from_file(tree_name, file_name)
  assign_leaf(tree, branch_name, leaf_name)
  
  # we need the last entry
  n_entries = tree.GetEntries()
  tree.GetEntry(n_entries - 1)
  
  # U&&!D including & excluding veto and error
  res = {'u_not_d_not_veto':ValueWithError(tree.scaler(1)), 'u_not_d':ValueWithError(tree.scaler(2))}
  for i in res.values():
    i.print_fmt=u"{: >9.0f} +/- {: <4.0f}"
  res['dead_time'] = res['u_not_d_not_veto']/res['u_not_d']
  res['dead_time'].print_fmt = u"{: >5.2f} +/- {: <5.3f}"
  return res


def get_pretty_results(dead_time_dicts):
  res = u"{:^3s} | {:^15s} | {:^18s} | {:^17s}\n".format("Run", "dead time (%)", "(U && !D)", "(U && !D && !Veto)")
  ord_keys = [int(run_id) for run_id in dead_time_dicts.keys()]
  ord_keys.sort()
  entry_fmt=u"{run_id} | {dead_time_per} | {u_not_d} | {u_not_d_not_veto}\n"
  for i in ord_keys:
    dead_time_per   = 100*dead_time_dicts[i]['dead_time'] # make it a percent
    dead_time_per.print_fmt = dead_time_dicts[i]['dead_time'].print_fmt
    res += entry_fmt.format(run_id=run_id, dead_time_per=dead_time_per, **dead_time_dicts[i])
  return res

def get_dead_times_for_run_ids(run_ids):
  return {r:get_dead_time_from_file(r) for r in run_ids}

def main():
  res = get_dead_times_for_run_ids(run_ids)
  print get_pretty_results(res)
  print "*"*80
  print res

if __name__=="__main__":
  main()