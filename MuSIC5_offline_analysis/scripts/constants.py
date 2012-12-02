detector_efficiency = 0.5 # FIXME  THIS IS A MADE UP NUMBER!  
nA = 1e-9                 # scale for nano; i.e. the used proton current
uA = 1e-6                 # scale for micro; i.e. the maximum proton current
e_charge = 1.60217e-19

if __name__=="__main__":
    print "The constants.py currently defines:\n"
    with open("constants.py") as this_file:
        for line in this_file:
            if '__name__' in line:
                print "\nEnd of constants"
                break
            elif not line.strip():
                continue
            else:
                line = line.strip()
                line = line.split('#') # ignore any comments
                print line[0]
                