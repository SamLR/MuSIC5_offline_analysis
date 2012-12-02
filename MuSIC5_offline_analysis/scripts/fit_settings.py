__setting_names = ("fit_lo", "fit_hi", "bin_width")

__window_starts_slow = (50, 75, 100, 125, 150)  
__window_stops_slow  = (20000,)
__bin_widths_slow      = (50, 100, 200)

__fitting_settings_slow = [(i,j,k) for i in __window_starts_slow 
                                   for j in __window_stops_slow 
                                   for k in __bin_widths_slow]

fitting_settings_slow = [dict(zip(__setting_names, i)) for i in __fitting_settings_slow]
                            
__window_starts_fast = (100,)#(50,)      
__window_stops_fast  = (20000,)    
__bin_widths_fast      = (50,)

__fitting_settings_fast = [(i,j,k) for i in __window_starts_fast 
                                   for j in __window_stops_fast 
                                   for k in __bin_widths_fast]

fitting_settings_fast = [dict(zip(__setting_names, i)) for i in __fitting_settings_fast]

fitting_parameters =(("N_{B}",           lambda hist: float(hist.GetMaximum())/10),               
                     ("N_{#mu_{Cu}}",    lambda hist: float(hist.GetMaximum())),
                     ("#tau_{#mu_{Cu}}", lambda hist: 163.5, 1), # PDG value is  1 
                     ("N_{#mu_{All}}",   lambda hist: float(hist.GetMaximum())/2),
                     ("#tau_{#mu_{All}}",lambda hist: 2000))   

def settings_str(fit_lo, fit_hi, bin_width, **kargs):
    return "lo_%i_hi_%i_bins_%i"%(fit_lo, fit_hi, bin_width)

if __name__=="__main__":
    print "### This is a config file ###"
    print "Current slow fitting parameters are:"
    print "\tWindow lbound ", __window_starts_slow
    print "\tWindow ubound ", __window_stops_slow
    print "\tBin widths    ", __bin_widths_slow
    print "Current fast fitting parameters are:"
    print "\tWindow lbound ", __window_starts_fast
    print "\tWindow ubound ", __window_stops_fast
    print "\tBin widths    ", __bin_widths_fast
    print "Current initial fitting parameters:"
    with open("fit_settings.py") as in_file:
        skip_line = True
        for line in in_file:
            if line.startswith('fitting_parameters'):
                line = line.split('=')[1]
                line.strip()
                print '\t',line,
                skip_line = False
            elif skip_line:
                continue
            else:
                line = line.strip()
                print "\t",line
                if line[-2:] == '))':
                    skip_line = True
            
    