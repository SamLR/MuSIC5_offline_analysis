""" 
A simple class that represents a value and its error.
Will correctly calculate addition/subtraction/multiplication
/division of errors.
 
ValueWithError.py
scripts

Created by Sam Cook on 2013-05-06.
Copyright 2013 Sam Cook. All rights reserved.

"""

from math import sqrt

class ValueWithError(object):
  """
  Correctly handle a value and its associated error
  """
  def __init__(self, value, error, print_fmt="{: >8.1f} +/- {: <8.2f}"):
    super(ValueWithError, self).__init__()
    self.value = float(value)
    self.error = float(error)
    self.print_fmt = print_fmt
    # TODO Auto generate print_fmt 
  
  def __float__(self):
    """
    Overload the 'float' function so we get just the value
    """
    return self.value
  
  def __repr__(self):
    return "ValueWithError(value={:f},error={:f})".format(self.value, self.error)
    
  def __str__(self):
    return self.print_fmt.format(self.value, self.error)
    
  def __add__(self, b):
    def addValuesWithErrors(a, b):
      # helper function
      new_val = a.value + b.value
      new_er = (a.error**2 + b.error**2)**0.5
      return ValueWithError(new_val, new_er)
      
    if hasattr(b, "error") and hasattr(b, "value"):
      return addValuesWithErrors(self, b)
    else:
      # cast to ValueWithError
      tmp = ValueWithError(b, 0)
      return addValuesWithErrors(self, tmp)

  def __radd__(self, a):
    return self+a
  
  def __sub__(self, a): 
    return self + -1.0*a
    
  def __rsub__(self, a):
    return -1.0*self + a
    

  def __mul__(self, b):
    def multiplyValuesWithErrors(a,b):
      new_val = a.value*b.value
      frac_a = a.error/a.value
      frac_b = b.error/b.value
      new_er = new_val*sqrt(frac_a**2 + frac_b**2)
      return ValueWithError(new_val, new_er)
    
    if hasattr(b, "error") and hasattr(b, "value"):
      return multiplyValuesWithErrors(self, b)
    else:
      tmp = ValueWithError(b, 0)
      return multiplyValuesWithErrors(self, tmp)
    
  def __rmul__(self, a):
    return self * a
    
  def __div__(self, b):
    def divideValuesWithErrors(a,b):
      new_val = a.value/b.value
      frac_a = a.error/a.value
      frac_b = b.error/b.value
      new_er = new_val*sqrt(frac_a**2 + frac_b**2)
      return ValueWithError(new_val, new_er)
      
    if hasattr(b, "error") and hasattr(b, "value"):
      return divideValuesWithErrors(self, b)
    else:
      tmp = ValueWithError(b, 0)
      return divideValuesWithErrors(self, tmp)
    
  def __rdiv__(self, a):
    tmp = ValueWithError(a, 0)
    return tmp/self
    
class TestLogger(object): 
  """Simple logging decorator for the test funcions"""
  def __init__(self, func):
    self.func = func
    
  def __call__(self):
    print "Running: ", self.func.func_name
    self.func()
    print "Done. \n"

def _nearly_equal(a, b, n_places=7):
  """Because I don't want the whole unittestsuite"""
  return (round(a-b, n_places) == 0)

@TestLogger
def test_addition():
  a = ValueWithError(value=5, error=2)
  b = ValueWithError(value=10, error=2)
  c = a+b
  print "a = ", a, "\nb = ", b,"\na + b = ", c
  assert c.value==15.0
  assert _nearly_equal(c.error, sqrt(8)) # sqrt(2**2 + 2**2)
  d = a + 9
  print "a + 9 = ", d
  assert d.value==14.0
  assert d.error==2.0
  e = 9 + a
  print "9 + a = ", e
  assert e.value==14.0
  assert e.error==2.0
  
  
@TestLogger
def test_str():
  a = ValueWithError(value=5, error=2)
  print "a (basic print), ",a
  b = ValueWithError(value=3.14e9, error=2, print_fmt="{: >10.1f} | {: <7.1e}")
  print "b (with modified print_fmt), ",b
  
@TestLogger
def test_repr():
  # repr should: "if at all possible, this should look like a valid 
  # Python expression that could be used to recreate an object with 
  # the same value"
  a = ValueWithError(value=5, error=2)
  print "Should be able to eval this to get a again: ", repr(a)
  b = eval(repr(a))
  print "b = eval(repr(a)) is ", repr(b)
  # actually test we've recreated a
  assert b.value==a.value
  assert b.error==a.error
  
@TestLogger
def test_subtraction():
  a = ValueWithError(value=5, error=2)
  print "a = ", a
  b = ValueWithError(value=10, error=2)
  print "b = ", b
  c = a-b
  print "a - b = ", c
  assert c.value==-5.0
  assert _nearly_equal(c.error, sqrt(8)) 
  d = a - 9
  print "a - 9 = ", d
  assert d.value==-4.0
  # This should be exactly equal as the error is copied
  assert d.error==2.0
  e = 9 - a
  print "9 - a = ", e
  assert e.value==4.0
  assert e.error==2.0

@TestLogger
def test_multiplication():
  a = ValueWithError(10, 1)
  b = ValueWithError(20, 2)
  c = a*b
  print "a = ", a, "\nb = ", b, "\na*b =", c
  assert c.value==200.0
  assert _nearly_equal(c.error, 28.28427124)
  d = a*2
  print "a*2 = ", d
  assert d.value==20.0
  assert _nearly_equal(d.error, 2.0)
  d = 2*a
  print "2*a = ", d
  assert d.value==20.0
  assert _nearly_equal(d.error, 2.0)
  
@TestLogger
def test_division():
  a = ValueWithError(10, 2)
  b = ValueWithError(2, 0.5)
  c = a/b
  print "a = ", a, "\nb =  ", b, "\na/b=", c
  assert c.value==5.0
  assert _nearly_equal(c.error, 1.6007810593582121)
  d = a/2
  print "a/2 = ", d
  assert d.value==5.0
  assert d.error==1.0
  d = 2/a
  print "2/a = ", d
  assert d.value==0.2
  assert _nearly_equal (d.error,0.04)
  
  

@TestLogger
def test_float():
  a = ValueWithError(10, 2)
  print float(a)
  assert type(float(a))==float
def main():
  test_str()
  test_repr()
  test_addition()
  test_subtraction()
  test_multiplication()
  test_division()
  test_float()

if __name__=="__main__":
  main()
    