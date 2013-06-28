"""
Compare the calculated number of copper/free stopped-muons
with the count. This is lazy and just pulls the data out of 
the text files.
"""

txt_dir="output_txt/"
arbitary_count_file=txt_dir+"/simulation_counts_and_integrals_loose_cu_10ns_bins.txt"

def main():
  get_counts()

if __name__=="__main__":
  main()