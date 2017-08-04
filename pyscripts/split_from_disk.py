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

# def sync_meanings(new_meaning, new_json):
#   diff = len(new_meaning) - len(new_json)
  
#   # New meaning added manually
#   if diff > 0:
#     for _ in range(diff):
#       new_json.append(new_json[-1])
#   # A meaning deleted manually
#   elif diff < 0:
#     for _ in range(-diff):
#       # WHAT SHOULD I DO

#   return new_meaning, new_json


def main():
  data = json_from_file(SRC_DATA_DIR, "all.json")

  for list_name in WORD_LISTS:
    split_data = json_from_file(DEST_DATA_DIR, list_name + ".json")

    # ---------- Overwrite with the new structure ----------
    for w in split_data:
      split_data[w] = data[w]

    # ---------- Use the new structure, but keep modifications that have been made ----------
    # for w in split_data:
    #   # Check if the meaning count is the same and fix if not
    #   split_data[w], data[w] = sync_meanings(split_data[w], data[w])

    #   # For every meaning in the list
    #   for i, m in enumerate(split_data[w]):
    #     # For every key in m
    #     for key, v in m.iteritems():
    #       # Change the value of that key in the list of all
    #       data[w][i][key] = v

    #   # Overwrite the meaning with the new JSON structure
    #   split_data[w] = data[w]


    write_json(list_name, split_data)
    print("DONE with %s" % (list_name))

  # Overwrite the whole new database
  write_json("all", data)



if (__name__=="__main__"):
  main()

