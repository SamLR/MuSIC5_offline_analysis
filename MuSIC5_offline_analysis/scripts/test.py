from time import sleep
from ROOT import gStyle, TF1
from root_utilities import make_hist, make_canvas

def get_gaus(name):
  hist = make_hist(name)
  hist.FillRandom("gaus")
  return hist

def fit(name,hist):
  func = TF1(name, "[0]*exp(-x/[1])",-10,10)
  func.SetParameter(0,2000)
  func.SetParameter(1,1)
  hist.Fit(func, "MER")
  hist.func = func

def make_n_save(i):
  name = "test" + str(i)
  hist = get_gaus(name)
  can = make_canvas (name)
  hist.Draw()
  can.Update()
  fit(name, hist)
  hist.func.Draw("SAMES")
  can.Update()
  sleep(3)
  

def main():

  gStyle.SetOptStat(10)
  gStyle.SetOptFit(111)
  
  for i in xrange(3):
    make_n_save(i)

if __name__=="__main__":
  main()