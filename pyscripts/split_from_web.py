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

BASE_URL = "https://gre.magoosh.com/flashcards/vocabulary/"

WORD_LISTS = ["advanced", "basic", "high-freq"]

MAGOOSH_LISTS = {
  "advanced": (["advanced-words-i", "advanced-words-ii"] + ["advanced-words-" + str(i) for i in range(3,8)]),
  "basic": (["basic-words-i", "basic-words-ii"] + ["basic-words-" + str(i) for i in range(3,8)]),
  "high-freq": (["high-frequency-words"] + ["common-words-" + str(i) for i in range(2,7)]),
}



def write_json(f, flashcards):
  with open(os.path.join(DEST_DATA_DIR, f + '.json'), 'w') as outfile:
    # json.dump(flashcards, outfile)
    json.dump(flashcards, outfile, indent=4, sort_keys=True)


def query_url(url):
  resp = requests.get(url)
  if resp.status_code == 200:
    return True
  else:
    return False
  # try:
  #   urllib2.urlopen(url)
  #   return True
  # except urllib2.HTTPError:    
  #   return False


def traverse_urls(word, list_name):
  """
  @brief: Traverse the urls of magoosh to find to which list number does the word belong
  word: str
  list_name: str - the name of the list - advanced/basic/high-freqoriginal-
  @return: the number of the list or None if word not found
  """

  url_lists = MAGOOSH_LISTS[list_name]
  for i, ul in enumerate(url_lists):
    url = BASE_URL + ul + "/" + str(word)
    if query_url(url):
      return (i)
  return None


def json_from_file(filename):
  file_path = os.path.join(SRC_DATA_DIR, filename)
  with open(file_path, 'r') as f:
    data = json.load(f)
  return data


def write_splits(list_name, splits):
  for i, data in enumerate(splits):
    write_json(list_name + "-" + str(i+1), data)



def main():

  for list_name in WORD_LISTS:
    data = json_from_file(list_name + ".json")
    splits = [{} for i in range(len(MAGOOSH_LISTS[list_name])) ]

    for w in data:
      # Get the exact list the word belongs to
      # list_idx = get_word_idx(w, list_name)traverse_urls()
      list_idx = traverse_urls(w, list_name)

      if list_idx is None:
        # Print message that the word is not found
        print("WORD %s NOT FOUND. LIST: %s" % (w, list_name))
      else:
        # Append word to the list
        splits[list_idx][w] = data[w]

    # Write the lists
    write_splits(list_name, splits)
    print("DONE with %s" % (list_name))

  print("DONE")



if (__name__=="__main__"):
  main()

