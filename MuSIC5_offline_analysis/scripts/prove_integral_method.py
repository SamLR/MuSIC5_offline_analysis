#!/usr/bin/python

"""
Compare the calculated number of copper/free stopped-muons
with the count. This is lazy and just pulls the data out of 
the text files.
"""

from ValueWithError import ValueWithError

txt_dir="output_txt/Archive/"
arbitary_count_file=txt_dir+"simulation_counts_and_integrals_tight_10ns_bins.txt"
# arbitary_count_file=txt_dir+"simulation_counts_and_integrals_loose_cu_10ns_bins.txt"
# file = "output_txt/analysis_tight/rates_and_integrals.txt"
# file = "output_txt/analysis_loose_f/rates_and_integrals.txt"
file = "output_txt/analysis_g4bl_sin_exec_d4_d5_tight/rates_and_integrals.txt"

def increment_or_create(dictionary, key, value):
  if key in dictionary:
    dictionary[key] += value
  else:
    dictionary[key] = value

def add_to_results(dictionary, key, value_with_error_string):
  val = value_with_error_string.split("+/-")
  val = ValueWithError(*val)
  increment_or_create(dictionary, key, val)

def get_counts(file_name):
  with open(file_name,"r") as in_file:
    in_file.readline() # kill header lines
    in_file.readline()
    res = {}
    for line in in_file:
      mat, dz, cu_count, f_count, _, _,_ = line.split("|")
      mat, dz, cu_count, f_count = [s.strip() for s in (mat, dz, cu_count, f_count)]
      key = dz if mat != "Ai" else "0"
      
      if key not in res: res[key] = {}
      add_to_results(res[key], 'f_count', f_count)
      if cu_count != "na":
        add_to_results(res[key], 'cu_count', cu_count)
  return res
      


def get_integral(file_name):
  with open(file_name,"r") as in_file:
    still_rates = True
    while still_rates:
      # skip all the rate info
      line = in_file.readline()
      if "*" in line:
        still_rates = False
    # now read in the integral data
    res = {}
    for line in in_file:
      data_type, key, _, cu_int, f_int, _ = line.split('|')
      # use the 'dz' rather than data_type for key as dz has mm striped already
      if data_type.strip() in ("1mm", "5mm", "0.5"): # sims are id'd Xmm where x is dz
        key, cu_int, f_int = [s.strip() for s in (key, cu_int, f_int)]
        if key not in res: res[key] = {}
        add_to_results(res[key], "cu_int", cu_int)
        add_to_results(res[key], "f_int",  f_int)
  return res

def get_table(counts, ints):
  fmt = "{:3} | {:2} | {:^21} | {:^21} | {:^21}"
  res = [fmt.format("dz","t", "int", "count", "ratio (int/count)"),]
  for dz in ints: 
    for target in ("f", "cu"):
      int_key, count_key = target+"_int", target+"_count"
      i, c = ints[dz][int_key], counts[dz][count_key]
      ratio = i/c
      res.append(fmt.format(dz, target, i, c, ratio))
  return "\n".join(res)

def main():
  counts = get_counts(arbitary_count_file)
  ints = get_integral(file)
  print get_table(counts, ints)

if __name__=="__main__":
  main()