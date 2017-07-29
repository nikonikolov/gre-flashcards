import json
import os
import requests
import shutil
import urllib2

"""
JSON structure is as follows

  {
    "word_name": 
      [
        // Meaning 1
        {
          "type":       "noun/verb/adjective/adverb",
          "meaning":    "en explanation",
          "meaning_bg": "bg meaning",
          "example":    "example usage",
        },

        // Meaning 2
        {
          "type":       "noun/verb/adjective/adverb",
          "meaning":    "en explanation",
          "meaning_bg": "bg meaning",
          "example":    "example usage",
        }

      ], 

    "word_name": 
      [
        ...                    
      ], 
  }


"""

SRC_DATA_DIR = "../original-data/json/"
DEST_DATA_DIR = "../data/"

WORD_LISTS = ["high-freq-" + str(i) for i in range(1,7)] + ["advanced-" + str(i) for i in range(1,8)] + ["basic-" + str(i) for i in range(1,8)]


def write_json(f, flashcards):
  with open(os.path.join(DEST_DATA_DIR, f + '.json'), 'w') as outfile:
    json.dump(flashcards, outfile, indent=4, sort_keys=True)


def json_from_file(dirname, filename):
  file_path = os.path.join(dirname, filename)
  with open(file_path, 'r') as f:
    data = json.load(f)
  return data


def main():
  data = json_from_file(SRC_DATA_DIR, "all.json")

  for list_name in WORD_LISTS:
    split_data = json_from_file(DEST_DATA_DIR, list_name + ".json")

    for w in split_data:
      split_data[w] = data[w]

    write_json(list_name, split_data)
    print("DONE with %s" % (list_name))



if (__name__=="__main__"):
  main()

