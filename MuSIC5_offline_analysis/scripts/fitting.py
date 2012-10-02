from ROOT import TH1F, TF1

from utilities import set_param_and_error, get_param_and_error, rebin_bin_width, wait_to_quit

def fit_hist(orig_hist, fit_lo, fit_hi, bin_width, initial_fit_params, save_hist=False):
    name = orig_hist.GetName() + "_" + "lo_%i_hi_%i_bins_%i"%(fit_lo, fit_hi, bin_width)
    
    # local, rebinned copy of the hist
    hist = rebin_bin_width(orig_hist, bin_width, name) 
        
    # get the fitting function and fit it to the histogram
    fit_name = "fit_" + name
    fitting_func = get_fitting_func(fit_name, hist, fit_lo, fit_hi, initial_fit_params)
                                    
    # the covariance matrix can only be retrived from the fit result
    fit_res = hist.Fit(fitting_func, "RS") # fit in the function range
    covariance_matrix = fit_res.GetCovarianceMatrix()
    fit_param = get_fit_params(fitting_func)
    
    # get the integrals & errors
    counts = make_muon_counts_dict(fitting_func, covariance_matrix, fit_lo, fit_hi, bin_width)
    
    results = {'counts':counts, 'fit_param': fit_param}
    if save_hist: results['hist'] = hist
    return results


def get_fitting_func(name, hist, fit_lo, fit_hi, initial_fit_params):
    res = TF1(name, "[0] + [1]*exp(-x/[2]) + [3]*exp(-x/[4])", fit_lo, fit_hi)
    for param_number, val in enumerate(initial_fit_params):
        res.SetParName(param_number, val[0])
        param_val = val[1](hist)
        if len(val) == 3:
            limit_lo, limit_hi = param_val - val[2], param_val + val[2] 
            res.SetParameter(param_number, param_val)
            res.SetParLimits(param_number, limit_lo, limit_hi)
        else:
            res.SetParameter(param_number, param_val)
    return res


def get_fit_params(fit_func):
    res = {}
    n_par = fit_func.GetNpar()
    for i in range(n_par):
        par  = fit_func.GetParameter(i)
        name = fit_func.GetParName(i)
        er   = fit_func.GetParError(i)
        res[name] = (par, er)
    res['chi2'] = (fit_func.GetChisquare(), fit_func.GetNDF())
    return res


def make_muon_counts_dict(fitting_func, covariance_matrix, fit_lo, fit_hi, bin_width=0):
    n_bkgnd = fitting_func.GetParameter(0) * (fit_hi-fit_lo) # background is modeled as flat
    bin_width = 1 if bin_width == 0 else bin_width # dodge div0 errors (bin width 0 == no rebin)
    
    # create and intialise the parameters for the copper portion of the exponential
    cu_mapping = ((1,0), (2,1))
    n_cu, n_cu_er = calc_integral_from_exp_fit(cu_mapping, fitting_func, \
                            covariance_matrix, fit_lo, fit_hi)                            
    n_cu, n_cu_er = n_cu/bin_width, n_cu_er/bin_width
    
    # now intialise the slow portion
    mu_mapping = ((3,0), (4,1))
    n_mu, n_mu_er = calc_integral_from_exp_fit(mu_mapping, fitting_func, \
                            covariance_matrix, fit_lo, fit_hi)
    n_mu, n_mu_er = n_mu/bin_width, n_mu_er/bin_width
    
    return {"n_bkgnd":(n_bkgnd, 0), "n_mu_cu":(n_cu, n_cu_er), "n_mu_slow":(n_mu, n_mu_er),}


def calc_integral_from_exp_fit(param_mapping, fitting_func, covariance_matrix, fit_lo, fit_hi):
    func = TF1("tmp", "[0]*exp(-x/[1])", fit_lo, fit_hi)    
    
    copy_param_and_er(param_mapping, fitting_func, func)
    
    # get the integral and then calculate the error on it
    count = func.Integral(fit_lo, fit_hi)
    sub_matrix_vals = (param_mapping[0][0], param_mapping[1][0],\
                       param_mapping[0][0], param_mapping[1][0])
    sub_matrix = covariance_matrix.GetSub(*sub_matrix_vals)
    
    er = func.IntegralError(fit_lo, fit_hi, \
                func.GetParameters(), sub_matrix.GetMatrixArray())
    return count, er


def copy_param_and_er(param_mapping, func_src, func_dest):
    for src, dest in param_mapping:
        par, er = get_param_and_error(src, func_src)
        set_param_and_error(dest, par, er, func_dest)




