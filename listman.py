import json
import os
import random

DATA_DIR = "data"

# --------------------------- WORD LIST CLASS ---------------------------

class ListMan:

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
    self.ignore_know = False  # ignore the next know signal


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
    self.ignore_know = False  # ignore the next know signal


  def in_memory():
    """
    @return: True if words are in memory, false otherwise
    """
    return self.read


  def get_next_word(self):
    """
    @return: tuple of the word (str) and its meaning (list)
    """

    # print("idx: %d, len: %d" % (self.word_idx, len(self.words)))
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
    @brief:   Checks if any unknown words are left, writes them to self.words and shuffles
    @return:  False if any unknown words are left, True otherwise
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
    if self.ignore_know:
      self.ignore_know = False
      return

    if not flag:
      # word = self.words[self.word_idx]
      # Check if word is still in the list or it has been removed
      # if word in self.data: 
      self.unknown.append(self.words[self.word_idx])
    self.word_idx += 1


  def reset(self):
    random.shuffle(self.words)
    self.unknown  = []        # list of unknown words
    self.word_idx = 0         # idx of the currently displayed word
    self.ignore_know = False  # idx of the currently displayed word


  def remove_word(self, word):
    """
    @brief: Remove word from the list, if it is in RAM
    """
    if not self.read:
      return
    try:
      del self.data[word]
    except KeyError:
      pass
    try:
      self.words.remove(word)
    except ValueError:
      pass
    try:
      self.words.remove(word)
    except ValueError:
      pass

    self.ignore_know = True

  def append_word(self, word, meaning):
    """
    @brief: Append word to this list
    @return: True on success, False if word is already in the list
    """
    if not self.read:
      return True
    if word in self.data:
      return False
    self.data[word] = meaning
    self.words.append(word)

    return True


