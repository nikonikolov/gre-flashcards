import json
import os

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
          "note":       "This word has other definitions but this is the most important one for the GRE" or "",
          "syn":        "",
          "ant":        "",
        },

        // Meaning 2
        {
          "type":       "noun/verb/adjective/adverb",
          "meaning":    "en explanation",
          "meaning_bg": "bg meaning",
          "example":    "example usage",
          "note":       "This word has other definitions but this is the most important one for the GRE" or "",
          "syn":        "",
          "ant":        "",
        }

      ], 

    "word_name": 
      [
        ...                    
      ], 
  }


"""

SOURCE_DATA_DIR = "../original-data/txt/"
DEST_DATA_DIR = "../original-data/json/"

WORD_TYPES = ["noun", "adjective", "verb", "adverb"]
NOTE_SRT = "This word has other definitions but this is the most important one for the GRE"


def get_flashcards_list(lines):
  """
    lines: a list of lines of the file stripped of \n 
    return: a dictionary of words
  """
  word_dict = {}

  word = None

  # Traverse the whole file
  for l in lines:
 
    # See if this line is a word
    new_word, new_meaning = detect_word(l)
  
    # New word not detected yet => Complete the string for the example
    if new_word is None:
      example = complete_example(l, example)

    # New word is detected and this is not first run of the loop
    elif word is not None:
      # Complete the current word meaning
      # meaning[-1]["example"] = example
      
      example, note = process_example(example)
      meaning[-1]["example"] = example
      meaning[-1]["note"] = note

      # Update word

      # New meaning for the same word
      if word == new_word:
        meaning.append(new_meaning[-1])

      # Entirely new word
      else:
        # Write the current word to the global dictionary
        word_dict[word] = meaning

        word, meaning = new_word, new_meaning

      # Reset the example string
      example = ""

    # First run of the loop
    else:
      word, meaning = new_word, new_meaning
      example = ""

  return word_dict


def complete_example(line, example):
  if example == "":
    example += line
  elif example[-1] != " ":
    example += (" " + line)

  return example


def process_example(example):
  note_pos = example.find(NOTE_SRT)
  if note_pos > 0:
    return example[:(note_pos-1)], NOTE_SRT
  else:
    return example, ""


def process_type(t):
  if t == "adjective":
    return "adj."
  if t == "adverb":
    return "adv."
  return t


def detect_word(line):
  """
  line: a line in database.txt, stripped of \n
  Return:
    word - str of the word
    [meaning] - a list of 1 dictionary with the meaning of the word
  """
  
  for t in WORD_TYPES:
    search_str = " (" + t + "): "
    found = line.find(search_str)
    if found > 0:
      word = line[:found]

      meaning = {}
      meaning["type"] = process_type(t)
      def_start = found + len(search_str)
      meaning["meaning"] = line[def_start:]
      meaning["meaning_bg"] = ""
      meaning["syn"] = ""
      meaning["ant"] = ""

      return word, [meaning]

  return None, None


def preprocess_file(f):
  with open(os.path.join(SOURCE_DATA_DIR, f + ".txt"), 'r') as f:
    lines = f.readlines()
  lines = [ l.strip('\n') for l in lines if l != ('\n')]
  return lines


def write_json(f, flashcards):
  with open(os.path.join(DEST_DATA_DIR, f + '.json'), 'w') as outfile:
    # json.dump(flashcards, outfile)
    json.dump(flashcards, outfile, indent=4, sort_keys=True)


def main():
  filenames = ["advanced", "basic", "high-freq"]
  all_words = {}
  for f in filenames:
    lines = preprocess_file(f)
    flashcards = get_flashcards_list(lines)
    write_json(f, flashcards)
    all_words.update(flashcards)
    print(len(flashcards))
  write_json("all", all_words)
  print(len(all_words))


if (__name__=="__main__"):
  main()

