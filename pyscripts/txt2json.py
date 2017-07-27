import json

SOURCE_DATA_DIR = "../original_data/"
DEST_DATA_DIR = "../original_data_json/"

# How to deal with words which have two meanings
def get_flashcards_list(lines):
  word_list = []

  word = None

  for l in lines:
    # See if this line is a word
    new_word = detect_word(l)
  
    if new_word is None:
      example = complete_example(l, example)

    elif word is not None:
      # Complete the current word meaning
      m_entry = word["meanings_list"][-1] 
      m_entry["example"] = example
      # word["example"] = example

      # Update word

      # New meaning for the same word
      if new_word["word"] == word["word"]:
        new_meaning = new_word["meanings_list"][-1]
        word["meanings_list"].append(new_meaning)    

      # Entirely new word
      else:
        # Write the current word to the global dictionary
        word_list.append(word)

        word = new_word

      # Reset the example string
      example = ""

    else:
      word = new_word
      example = ""

  return word_list

def complete_example(line, example):
  if example == "":
    example += line
  elif example[-1] != " ":
    example += (" " + line)

  return example

# Fix the thing about second meaning and key
def detect_word(line):
  """
  line: a line in database.txt, stripped of \n
  """

  word_types = ["noun", "adjective", "verb", "adverb"]
  
  for t in word_types:
    search_str = " (" + t + "): "
    found = line.find(search_str)
    if found > 0:
      word = {}
      word["word"] = line[:found]

      meaning = {}
      meaning["type"] = t
      def_start = found + len(search_str)
      meaning["meaning"] = line[def_start:]
      meaning["meaning_bg"] = ""

      word["meanings_list"] = []
      word["meanings_list"].append(meaning)

      # key = line[:found]
      # word["type"] = t
      # def_start = found + len(t)
      # word["meaning"] = line[def_start:]

      return word
      # return key, word

  return None


def preprocess_file(f):
  with open(SOURCE_DATA_DIR + f + ".txt", 'r') as f:
    lines = f.readlines()
  lines = [ l.strip('\n') for l in lines if l != ('\n')]
  return lines


def write_json(f, flashcards):
  with open(DEST_DATA_DIR + f + '.json', 'w') as outfile:
    json.dump(flashcards, outfile)


def main():
  filenames = ["advanced", "basic", "high-freq"]
  for f in filenames:
    lines = preprocess_file(f)
    flashcards = get_flashcards_list(lines)
    write_json(f, flashcards)

if (__name__=="__main__"):
  main()

