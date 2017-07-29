import json
import os

# DATA_DIR = "../original-data/json/"
DATA_DIR = "../data/"


def json_from_file(filename):
  file_path = os.path.join(DATA_DIR, filename)
  with open(file_path, 'r') as f:
    data = json.load(f)
  return data


def main():
  word_lists = sorted(os.listdir(DATA_DIR))

  for l in word_lists:
    data = json_from_file(l)
    print("LIST %s: %d" % (l, len(data)))
  print("DONE")


if (__name__=="__main__"):
  main()

