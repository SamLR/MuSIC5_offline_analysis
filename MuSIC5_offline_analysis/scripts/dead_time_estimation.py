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
    
    # U&&!D including & excluding veto and error
    exc_veto = float(branch['scaler'][1]), (float(branch['scaler'][1]))**0.5
    inc_veto = float(branch['scaler'][2]), (float(branch['scaler'][2]))**0.5
    
    
    dead_time    = exc_veto[0]/inc_veto[0]
    sq_frac = lambda x: (x[1]/x[0])**0.5 # (dA/A) ^ 2
    dead_time_er = dead_time * ((sq_frac(inc_veto) + sq_frac(exc_veto))**0.5)
    
    
    return {'u_not_d_not_veto':exc_veto, 'u_not_d':inc_veto, 
            'dead_time':(dead_time,dead_time_er)}


def print_pretty_results(dead_time_dicts):
    import locale
    locale.setlocale(locale.LC_ALL, 'en_US')
    locale.format("%d", 1255000, grouping=True)
    print "%4s | %13s | %16s | %18s"%("file", "dead time (%)", "(U && !D)", "(U && !D && !Veto)")
    ord_keys = list(dead_time_dicts.keys())
    ord_keys.sort()
    for i in ord_keys:
        dt            = 100*dead_time_dicts[i]['dead_time'][0]
        dt_er         = 100*dead_time_dicts[i]['dead_time'][1]
        u_nd          = int(dead_time_dicts[i]['u_not_d'][0])
        u_nd_er       = int(dead_time_dicts[i]['u_not_d'][1])
        u_nd_nveto    = int(dead_time_dicts[i]['u_not_d_not_veto'][0])
        u_nd_nveto_er = int(dead_time_dicts[i]['u_not_d_not_veto'][1])
        # print "%4i | %7.1f %% | %9i | %18i"%(int(i), dt, u_nd, u_nd_nveto)
        print u"%4i | % 6.1f \xb1 %.1f | %9i \xb1 %i | %7i \xb1 %i"\
                %(int(i), dt, dt_er, u_nd, u_nd_er, u_nd_nveto, u_nd_nveto_er)


def main():
    res = {}
    for file_id, file_data in files_info.items():
        res[int(file_id)] = get_dead_time_from_file(file_data, file_id)
    print '\n'
    print_pretty_results(res)

if __name__=="__main__":
    main()