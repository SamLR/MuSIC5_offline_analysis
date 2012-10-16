from ROOT import TFile
from root_utilities import get_branch, get_struct

file_prefix = "/Users/samcook/code/MuSIC/offline_analysis_music5/MuSIC_data_0.5Cu/run"
file_suffix = ".root"
file_ids    = ("448", "00451", "00452", "00455", "00458", "00459") 

# annoyingly run 448 has a different format scaler tree to the others....
data_fmt                   = ('struct_fmt',            'branch_name','tree_name')
_normal_sclr_branch_struct = ('int n; int scaler[8];', 'SCLR',       'Scaler')
_448_sclr_branch_struct    = ('int scaler [8];',       'Scaler',     'ts')

_normal_sclr_branch_struct = dict(zip(data_fmt, _normal_sclr_branch_struct))             
_448_sclr_branch_struct    = dict(zip(data_fmt, _448_sclr_branch_struct))             

files_info = {i:_normal_sclr_branch_struct for i in file_ids[1:]}
files_info[file_ids[0]] = _448_sclr_branch_struct

def get_tfile_tree_and_branch(file_name, struct_fmt, branch_name, tree_name, **kwargs):
    tfile = TFile(file_name,"READ")
    tree  = tfile.Get(tree_name)
    struct = get_struct(struct_fmt, branch_name)
    branch = get_branch(tree, branch_name, struct)
    
    return tfile, tree, branch

