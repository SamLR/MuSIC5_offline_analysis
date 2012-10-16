"""
Calculate the dead time for each run by dividing the number of triggers
counted by the scaler by the number of possible triggers.
"""

from sclr_branch_func import * 

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
    ord_keys = list(dead_time_dicts.keys())
    ord_keys.sort()
    for i in ord_keys:
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