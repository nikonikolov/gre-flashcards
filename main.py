import json
import os

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from wordlist import WordList

DATA_DIR = "data"

app = Flask(__name__)

DEFAULT_LISTS = ["basic", "high-freq", "advanced"]


# --------------------------- DATABASE MANIPULATION ---------------------------

def write_file(data, filename):
  """
    data: dict that will replace the whole contents of the file
  """
  file_path = os.path.join(DATA_DIR, filename)
  with open(file_path, 'w') as f:
    json.dump(data, f, indent=4, sort_keys=True)


def write_file_obj(data, f):
  """
    data: dict that will replace the whole contents of the file
    f: python object corresponding to an open file
  """
  json.dump(data, f, indent=4, sort_keys=True)


def append_word(word, meaning, filename):
  """
    @brief: Read filename and append word to its contents
    word: str
    meaning: list of meanings for the word
  """
  file_path = os.path.join(DATA_DIR, filename)
  with open(file_path, 'r') as f:
    data = json.load(f)

  if word in data:
    data[word] += meaning
  else:
    data[word] = meaning
  write_file(data, filename)


def json_from_file(filename):
  file_path = os.path.join(DATA_DIR, filename)
  with open(file_path, 'r') as f:
    data = json.load(f)
  return data


def get_word_lists():
  """
  @return: list of names of the word lists - without any file paths or extensions
  """
  word_lists = os.listdir(DATA_DIR)
  return sorted([os.path.splitext(i)[0] for i in word_lists])


def get_custom_lists():
  """
  @return: list of names of the custom-created word lists - without any file paths or extensions
  """
  all_lists = get_word_lists()
  custom_lists = []

  def is_custom(listname):
    for dl in DEFAULT_LISTS:
      if listname.startswith(dl) or listname == "all":
        return False 
    return True

  return [l for l in all_lists if is_custom(l)]


def is_word_new(word):
  """
  @return True if word is new, false otherwise
  """
  all_words = json_from_file("all.json")
  return False if word in all_words else True


def add_new_word(word, meaning, decks):
  """
  @brief: Add a completely new word to all lists in decks and automatically to all.json
  @decks: List of str - the decks to add the word to
  """
  append_word(word, meaning, "all.json")
  for d in decks:
    append_word(word, meaning, d + ".json")


def get_key_matches(query):
  if query == "":
    return []
  words = json_from_file("all.json")
  # return sorted([k for k,v in words.items() if query in k])
  return [k for k,v in words.items() if k.startswith(query)]


def add_deck(deck):
  global g_all_decks
  global g_custom_decks
  global g_listmans

  if deck in g_all_decks:
    return False
  write_file({}, deck + ".json")
  
  g_all_decks    = get_word_lists()
  g_custom_decks = get_custom_lists()
  g_listmans[deck] = WordList(deck)

  return True



# --------------------------- COMMON FUNCTIONALIY ---------------------------

def show_word(word, listname, meaning=None):
  word = str(word)
  listname = str(listname)

  if meaning is None:
    data = json_from_file(listname + ".json")
    if word in data:
      meaning = data[word]
      return render_template('word.html', word_list=listname, word=word, meaning=meaning)
    else:
      return render_template('msg.html', msg="Word Not Found")
  
  else:
    return render_template('word.html', word_list=listname, word=word, meaning=meaning)


def get_and_read_lman(listname):
  lman = g_listmans[str(listname)]
  lman.read_data()
  return lman


# --------------------------- FLASK ---------------------------

@app.route('/')
def home():
  wordlists = g_all_decks
  return render_template('wordlists.html', wordlists=wordlists)


@app.route('/vocab/<listname>')
def list_next_word(listname):
  """
  @brief: Displays the next word from a list
  """
  lman = get_and_read_lman(listname)
  word, meaning = lman.get_next_word()
  if word is None:
    lman.clear_memory()
    return render_template('msg.html', msg="List Learned")
  return show_word(word, listname, meaning=meaning)


@app.route('/vocab/<listname>/_know')
def list_know(listname):
  """
  @brief: Handles GET request after know/don't know button is clicked in word meaning
  """
  flag = bool(request.args.get('flag', 0, type=int))
  lman = get_and_read_lman(listname)
  lman.word_known(flag)
  return jsonify(result= "/vocab/" + str(listname))


@app.route('/words/<word>')
def query_word(word):
  return show_word(word, "all")


@app.route('/words/<listname>/<word>')
def query_from_list(word, listname):
  return show_word(word, listname)


@app.route('/addword')
def addword():
  return render_template('addword.html', num_meanings=1, decks=g_custom_decks)


@app.route('/addword/_submit', methods=['POST'])
def process_addword_form():
  """
  @brief: Handle form submission for adding word
  """
  data = request.get_json()
  word    = data["word"]
  meaning = data["meaning"]
  decks   = data["decks"]

  resp = {"word": word}
  if not is_word_new(word):
    resp["status"] = "Error: The word " + word + " is already in your lists. Please modify it if you need to"
  else:
    resp["status"] = "Success"
    add_new_word(word, meaning, decks)

  return jsonify(resp)


@app.route('/search')
def search():
  return render_template('search.html')


@app.route('/search/_query', methods=['GET'])
def search_query():
  query = request.args.get('query', "", type=str)
  matches = get_key_matches(query)
  return jsonify(matches)


@app.route('/addlist')
def addlist():
  return render_template('addlist.html', decks=g_custom_decks)


@app.route('/addlist/_submit', methods=['GET'])
def addlist_process_form():
  """
  @brief: Handle form submission for adding a list
  """
  deck = request.args.get('deck', "", type=str)

  resp = {"deck": deck}
  if add_deck(deck):
    resp["status"] = "Success"
  else:
    resp["status"] = "Error: The list " + deck + " already exists"
    
  return jsonify(resp)



# --------------------------- MAIN ---------------------------
g_all_decks    = get_word_lists()
g_custom_decks = get_custom_lists()
g_listmans = { l: WordList(l) for l in g_all_decks}


if (__name__=="__main__"):
  app.run()

