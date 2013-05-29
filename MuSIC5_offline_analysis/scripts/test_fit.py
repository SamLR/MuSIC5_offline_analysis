from basic_integral import fit_histogram, get_integrals_from_histogram_for_keys,\
                           save_hist_with_fit, get_fit_func_and_settings_for_muon_type
from root_utilities import make_hist
import random
from math import exp
def make_hist(tau, error_on_tau, n_entries = 1e8, l_bound=0, u_bound=20000, *args, **kwargs):
  """
  Generate a random exponential histogram. If error_on_taus 
  are specified for the tau and scale these are used 
  to produce these values correctly.
  """
  def get_random_exp_value():
    random_tau = random.gaus(tau, error_on_tau)
    
    while (True):
      r1 = random.uniform(l_bound, u_bound)
      r2 = random.random()
      if exp(-r2/random_tau) < exp(-r1/random_tau):
        return r1
      else:
        continue
      
  hist = make_hist(name, mins=(l_bound,), maxs=(u_bound,), **kwargs)
  for entry in xrange(n_entries):
    hist.Fill(get_random_exp_value(tau,error_on_tau))
  return hist


def main():
  hist = make_hist(tau, error_on_tau)

if __name__=="__main__":
  main()