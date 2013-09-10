"""
Reads tables from a file
"""

def read_table(file_name, delim="|", comment="#"):
  """
  Read the contents of a table.
  """
  res = []
  with open(file_name, "r") as table_file:
    for line in table_file:
      table_row = remove_comments(line, comment)
      if not table_row: continue
      res.append(table_row.split(delim))
  return res

def remove_comments(text, comment):
  if comment not in text:
    # No comment
    return text
  elif text.startswith(comment):
    # whole line comment
    return ""
  else:
    info, comment = text.split(comment)
    return info


def test_remove_comments():
  tests_results=(("No comments in this", "No comments in this"),
                 ("# Only comments in this", ""),
                 ("Some # comments in this", "Some "),
                 ("#", ""),
                 ("   ", "   "),
                 ("", ""),
                 ("   # ", "   "),)
  for test, expected in tests_results:
    res = remove_comments(test, "#")
    print "Trying: '{}', expecting: '{}', got: '{}'".format(test, expected, res)
    assert res == expected

def main():
  # test_remove_comments()
  res = read_table("mppc_data.txt")
  for r in res:
    print r

if __name__=="__main__":
  main()