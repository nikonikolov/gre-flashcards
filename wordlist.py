import json
import os
import random

DATA_DIR = "data"

# --------------------------- WORD LIST CLASS ---------------------------

class WordList:

  def __init__(self, filename):
    self.listname = filename
    # self.listidx  = int(filename[-1])

    self.filename = filename + ".json"
    self.filepath = os.path.join(DATA_DIR, self.filename)

    self.data     = None      # dict of words and meanings
    self.words    = None      # list of words
    self.unknown  = []        # list of unknown words
    self.word_idx = 0         # idx of the currently displayed word
    self.read     = False     # True if the list is in RAM, false otherwise


  def read_data(self):
    if self.read:
      return

    with open(self.filepath, 'r') as f:
      self.data = json.load(f)
    self.words  = list(self.data.keys())
    self.read   = True
    self.reset()


  def force_read(self):
    with open(self.filepath, 'r') as f:
      self.data = json.load(f)
    self.words  = list(self.data.keys)
    self.read   = True
    self.reset()


  def clear_memory(self):
    """
    @brief: Clear the memory needed to store the list
    """
    self.data     = None      # dict of words and meanings
    self.words    = None      # list of words
    self.unknown  = []        # list of unknown words
    self.word_idx = 0         # idx of the currently displayed word
    self.read     = False


  def in_memory():
    """
    @return: True if words are in memory, false otherwise
    """
    return self.read


  def get_next_word(self):
    """
    @return: tuple of the word (str) and its meaning (list)
    """

    print("idx: %d, len: %d" % (self.word_idx, len(self.words)))
    try:
      word = self.words[self.word_idx]
    except IndexError:
      # We have run out of words - check if there are still words you don't know
      if self.out_of_words():
        return None, None
      word = self.words[self.word_idx]
    
    return word, self.data[word]


  def out_of_words(self):
    """
    @brief:   Checks if any uknown words are left, writes them to self.words and shuffles
    @return:  False if any uknown words are left, True otherwise
    """
    if len(self.unknown) > 0:
      self.words    = self.unknown
      self.unknown  = []
      self.word_idx = 0
      random.shuffle(self.words)
      return False
    else:
      return True


  def word_known(self, flag):
    """
    @brief: Puts the current word in the unknown list if necessary and advances self.word_idx
    @param flag: True if current word is known, false otherwise
    """
    if not flag:
      self.unknown.append(self.words[self.word_idx])
    self.word_idx += 1


  def reset(self):
    random.shuffle(self.words)
    self.unknown  = []        # list of unknown words
    self.word_idx = 0         # idx of the currently displayed word

