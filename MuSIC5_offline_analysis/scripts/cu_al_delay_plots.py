"""
Test of Geant4's muon decay code. Specifically the 
muon decay code and the delays there in. 

Rates seem to give the wrong lifetime for muonic
copper (163.5ns according to Suzki et al).  
"""

from random import random
from math import log
from ROOT import gStyle
from root_utilities import make_hist, make_canvas
from analysis_core import fit_histogram

def get_muon_decay_rate(Z, A):
  """
  Decay time on K-shell 
  N.C.Mukhopadhyay Phys. Rep. 30 (1977) 1.
  """
  Z = float(Z)
  rate = 1.0;
  if(Z > 1):
    x = Z*7.2973525698e-3 # fine structure constant
    rate -= 2.5 * x * x
    if( 0.5 > rate ):
      rate = 0.5
  return rate * 0.445164 / 1e3; 
  
def get_muon_capture_rate(Z, A):
# zeff, ListZExp and ListCaptureVel copied from G4StopElementSelector
  zeff = [ 1.00,  1.98,  2.95,  3.89,  4.80,  5.72,  6.61,  7.49,  8.32,  9.12,
           9.95, 10.69, 11.48, 12.22, 12.91, 13.64, 14.24, 14.89, 15.53, 16.15,
          16.75, 17.38, 18.04, 18.49, 19.06, 19.59, 20.10, 20.66, 21.12, 21.61,
          22.02, 22.43, 22.84, 23.24, 23.65, 24.06, 24.47, 24.85, 25.23, 25.61,
          25.99, 26.37, 26.69, 27.00, 27.32, 27.63, 27.95, 28.20, 28.42, 28.64,
          28.79, 29.03, 29.27, 29.51, 29.75, 29.99, 30.20, 30.36, 30.53, 30.69,
          30.85, 31.01, 31.18, 31.34, 31.48, 31.62, 31.76, 31.90, 32.05, 32.19,
          32.33, 32.47, 32.61, 32.76, 32.94, 33.11, 33.29, 33.46, 33.64, 33.81,
          34.21, 34.18, 34.00, 34.10, 34.21, 34.31, 34.42, 34.52, 34.63, 34.73,
          34.84, 34.94, 35.04, 35.15, 35.25, 35.36, 35.46, 35.57, 35.67, 35.78] 
  # Mu- capture data from B.B.Balashov, G.Ya.Korenman, P.A.Eramgan
  # Atomizdat, 1978. (Experimental capture velocities)
  # Data for Hydrogen from Phys. Rev. Lett. 99(2007)032002
  ListZExp = [ 1,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12,
              13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24,
              25, 26, 27, 28, 31, 32, 33, 34, 37, 38, 39,
              40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52,
              53, 55, 56, 57, 58, 59, 60, 62, 64, 65, 67,
              72, 73, 74, 80, 81, 82, 83, 90, 92, 93]
  ListCaptureVel = [ 0.000725,  0.0057,  0.010,  0.0258,  0.0371,  0.0644,
                     0.0974,    0.144,   0.250,  0.386,   0.479,   0.700, 
                     0.849,     1.119,   1.338,  1.40,    1.30,    1.98,  
                     2.45,      2.60,    3.19,   3.29,    3.91,    4.41,  
                     4.96,      5.74,    5.68,   5.53,    6.06,    5.69,  
                     6.89,      7.25,    7.89,   8.59,   10.40,    9.22,
                    10.01,     10.00,   10.88,  10.62,   11.37,   10.68,  
                    10.49,      9.06,   11.20,  10.98,   10.18,   10.71, 
                    11.44,     13.45,   12.32,  12.22,   12.09,   12.73,  
                    12.95,     13.03,   12.86,  13.13,   13.39,   12.74,  
                    13.78,     13.02,   13.26,  13.10,   14.00,   14.70]
  # ==  Effective charges from Ford and Wills Nucl Phys 35(1962)295.)
  # ==  Untabulated charges are interpolated.
  # ==  Mu capture lifetime (Goulard and Primakoff PRC10(1974)2034.
  i = Z - 1 
  b0a = -.03
  b0b = -.25
  b0c = 3.24
  t1 = 875.e-10
  r1 = zeff[i]
  zeff2 = r1 * r1
        
  # ^-4 -> ^-5 suggested by user
  xmu = zeff2 * 2.663e-5
  a2ze = 0.5 * A / Z
  r2 = 1.0 - xmu
  l = t1 * zeff2 * zeff2 * (r2 * r2) *  (1.0 - (1.0 - xmu) * .75704) * \
      (a2ze * b0a + 1.0 - (a2ze - 1.0) * b0b - (2.0 * (A - Z)  + abs(a2ze - 1.) ) * b0c / (A * 4.))
        
  for j in range(len(ListZExp)):
      if ListZExp[j] == i + 1 :
          l = ListCaptureVel[j]/1e3
          break
  return l

def get_delay(Z,A):
    total_rate = get_muon_capture_rate(Z,A) + get_muon_decay_rate(Z,A)
    return -log(random()) / total_rate # random in range [0,1.0]
    

def get_hist(Z, A, n_entries=1e6):
  name = "Z={Z} A={A}".format(Z=Z, A=A)
  axis_titles = ("Time (ns)", "Count")
  hist = make_hist(name, 0, 5000, axis_titles, 500)
  for i in xrange(int(n_entries)):
    hist.Fill(get_delay(Z,A))
  return hist

def main():
  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
  materials = {"Cu":{"Z":29,"A":63}, "Al":{"Z":13,"A":26}}
  
  for mat, element in materials.items(): 
    hist = get_hist(**element)
    can = make_canvas(mat)
    hist.Draw()
    initial_settings = (("N",    lambda x: 100, lambda x: 0.0 , lambda x: 1e6),
                        ("#tau", lambda x: 100, lambda x: 0.0 , lambda x: 5000))
    fit_histogram(hist, "[0]*exp(-x/[1])", initial_settings, mat,)
    can.Update()
    # can.SaveAs("images/"+mat+"_g4_generated.png")
    # can.SaveAs("images/"+mat+"_g4_generated.svg")
  

if __name__=="__main__":
  main()