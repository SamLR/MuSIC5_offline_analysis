"""
Calculate the dead time for each run by dividing the number of triggers
counted by the scaler by the number of possible triggers.
"""

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


def get_dead_time_from_file(file_data, file_root):
    name = file_prefix + file_root + file_suffix
    print "Opening file: %5s, tree: %s" % (file_root, file_data['tree_name'])
    # need tfile to keep it in scope
    tfile, tree, branch = get_tfile_tree_and_branch(name, **file_data)
    # we need the last entry
    n_entries = tree.GetEntries()
    tree.GetEntry(n_entries - 1)
    
    u_not_d_not_veto = branch['scaler'][1]
    u_not_d          = branch['scaler'][2]
    
    dead_time    = float(u_not_d_not_veto)/float(u_not_d)
    
    return {'u_not_d_not_veto':u_not_d_not_veto, 'u_not_d':u_not_d, 
            'dead_time':dead_time}


def print_pretty_results(dead_time_dicts):
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US')
    locale.format("%d", 1255000, grouping=True)
    print "%s | %s | %s | %s"%("file", "dead time", "(U && !D)", "(U && !D && !Veto)")
    for i in dead_time_dicts:
        dt = 100*dead_time_dicts[i]['dead_time']
        u_nd = dead_time_dicts[i]['u_not_d']
        u_nd_nveto = dead_time_dicts[i]['u_not_d_not_veto']
        print "%4i | %7.1f %% | %9i | %18i"%(int(i), dt, u_nd, u_nd_nveto)


def main():
    res = {}
    for file_id, file_data in files_info.items():
        res[file_id] = get_dead_time_from_file(file_data, file_id)
    print '\n'
    print_pretty_results(res)

if __name__=="__main__":
    main()