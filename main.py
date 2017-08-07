import json
import os

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from listman import ListMan

DATA_DIR = "data"

app = Flask(__name__)

DEFAULT_LISTS = ["basic", "high-freq", "advanced"]


# =============================================================================
# =========================== DATABASE MANIPULATION ===========================
# =============================================================================

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


def append_word_to_file(word, meaning, filename):
  """
    @brief: Read filename and append word to its contents
    word: str
    meaning: list of meanings for the word
    @return True if success, False if word is already in the list
  """
  file_path = os.path.join(DATA_DIR, filename)
  with open(file_path, 'r') as f:
    data = json.load(f)

  if word in data:
    return False

  data[word] = meaning
  write_file(data, filename)
  return True


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


def _is_list_custom(listname):
  for dl in DEFAULT_LISTS:
    if listname.startswith(dl) or listname == "all":
      return False 
  return True


def get_custom_lists():
  """
  @return: list of names of the custom-created word lists - without any file paths or extensions
  """
  return [l for l in get_word_lists() if _is_list_custom(l)]


def get_default_lists():
  """
  @return: list of names of the custom-created word lists - without any file paths or extensions
  """
  return [l for l in get_word_lists() if not _is_list_custom(l)]

  # all_lists = get_word_lists()

  # def is_default(listname):
  #   for dl in DEFAULT_LISTS:
  #     if listname.startswith(dl) or listname == "all":
  #       return False 
  #   return True

  # return [l for l in all_lists if not get_custom_lists.is_default(l)]


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
  append_word_to_file(word, meaning, "all.json")
  for d in decks:
    # Append to the file
    append_word_to_file(word, meaning, d + ".json")
    # Append to the ListMan if data already in memory
    lman = g_listmans[d]
    lman.append_word(word, meaning)


def add_deck(deck):
  global g_all_decks
  global g_custom_decks
  global g_listmans

  if deck in g_all_decks:
    return False
  write_file({}, deck + ".json")
  
  g_all_decks    = get_word_lists()
  g_custom_decks = get_custom_lists()
  g_listmans[deck] = ListMan(deck)

  return True


def remove_word_from_list(word, deck):
  data = json_from_file(deck + ".json")
  try:
    del data[word]
    write_file(data, deck + ".json")
  except KeyError:
    return


def append_word_to_lists(word, meaning, decks):
  """
  @brief: Append word only to the lists that don't contain it already
  @return: Response msg
  """
  success, fail = [], []
  for d in decks:
    status = append_word_to_file(word, meaning, d + ".json")
    if status:
      lman = g_listmans[d]
      lman.append_word(word, meaning)
      success.append(d)
    else:
      fail.append(d)
  
  msg = ""
  if success:
    msg += "Appended word to lists:" 
    for d in success:
      msg += (" " + d )
    msg += "!"
  if fail:
    msg += " Failed to append word to lists:" 
    for d in fail:
      msg += (" " + d )
    msg += ", because it already exists there!"
  return msg


def _modify_word_in_list(word, meaning, deck):
  """
  @brief: modify the word if it appears in deck
  """
  data = json_from_file(deck + ".json")
  if word in data:
    data[word] = meaning
    write_file(data, deck + ".json")


def modify_word(word, meaning, active_decks):
  for deck in g_all_decks:
    lman = g_listmans[deck]
    if deck in active_decks or deck in g_default_decks:
      _modify_word_in_list(word, meaning, deck)
      lman.modify_word(word, meaning)
    else:
      remove_word_from_list(word, deck)
      lman.remove_word(word)


# ===========================================================================
# =========================== COMMON FUNCTIONALIY ===========================
# ===========================================================================

def is_word_in_list(word, listname):
  data = json_from_file(listname + ".json")
  return word in data


def get_custom_lists_of_word(word):
  return [d for d in g_custom_decks if is_word_in_list(word, d)]


def get_word_meaning(word):
  """
  @brief: Get the meaning of a word. NOTE: Assumes the word exists
  """
  data = json_from_file("all.json")
  return data[word]


def get_key_matches(query):
  if query == "":
    return []
  words = json_from_file("all.json")
  # return sorted([k for k,v in words.items() if query in k])
  return [k for k,v in words.items() if k.startswith(query)]


def get_and_read_lman(listname):
  lman = g_listmans[str(listname)]
  lman.read_data()
  return lman


def is_list_custom(listname):
  return listname in g_custom_decks


def show_word(word, listname, know_button, meaning=None, number=None):
  word = str(word)
  listname = str(listname)

  # In this case the function was called by manually querying a path in the browser 
  if meaning is None:
    data = json_from_file(listname + ".json")
    if word in data:
      meaning = data[word]
      return render_template('word.html', word_list=listname, word=word, meaning=meaning, decks=g_custom_decks, rm_active=is_list_custom(listname), know_button=False, number=number)
    else:
      return render_template('msg.html', msg="Word Not Found")
  
  # In this case the function was called to display a new word in a deck
  else:
    return render_template('word.html', word_list=listname, word=word, meaning=meaning, decks=g_custom_decks, rm_active=is_list_custom(listname), know_button=True, number=number)



# =============================================================
# =========================== FLASK ===========================
# =============================================================


# --------------------------- DECKS ---------------------------
@app.route('/')
def home():
  wordlists = g_all_decks
  return render_template('wordlists.html', wordlists=wordlists)


# --------------------------- DISPLAYING WORD ---------------------------
@app.route('/vocab/<listname>')
def list_next_word(listname):
  """
  @brief: Displays the next word from a list
  """
  lman = get_and_read_lman(listname)
  word, meaning, number = lman.get_next_word()
  if word is None:
    lman.clear_memory()
    return render_template('msg.html', msg="List Learned")
  return show_word(word, listname, know_button=True, meaning=meaning, number=number)


@app.route('/vocab/<listname>/_know')
def list_know(listname):
  """
  @brief: Handles GET request after know/don't know button is clicked in word meaning
  """
  flag = bool(request.args.get('flag', 0, type=int))
  lman = get_and_read_lman(listname)
  lman.word_known(flag)
  return jsonify(result= "/vocab/" + str(listname))


@app.route('/_append', methods=['POST'])
def list_append_word():
  """
  @brief: Handles appending a word which is currently displayed to custom lists
  """
  data = request.get_json()
  word = data["word"]
  msg = append_word_to_lists(word, get_word_meaning(word), data["decks"])
  return jsonify(result=msg)


@app.route('/vocab/<listname>/_remove')
def list_remove_word(listname):
  """
  @brief: Handles request to remove currently displayed word from the current list
  """
  listname = str(listname)
  word = request.args.get('word', "", type=str)
  lman = g_listmans[listname]
  lman.remove_word(word)
  remove_word_from_list(word, listname)
  return jsonify(result="Successfully removed word " + word + " from the list " + listname + "!")


# --------------------------- QUERY WORD ---------------------------
@app.route('/words/<word>')
def query_word(word):
  return show_word(word, "all", know_button=False)


@app.route('/words/<listname>/<word>')
def query_from_list(word, listname):
  return show_word(word, listname, know_button=False)


# --------------------------- ADD WORD ---------------------------
@app.route('/addword')
def addword():
  return render_template('addword.html', num_meanings=1, decks=g_custom_decks)


@app.route('/addword/_submit', methods=['POST'])
def addword_process_form():
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


# --------------------------- SEARCH ---------------------------
@app.route('/search')
def search():
  return render_template('search.html')


@app.route('/search/_query', methods=['GET'])
def search_query():
  query = request.args.get('query', "", type=str)
  matches = get_key_matches(query)
  return jsonify(matches)


# --------------------------- ADD LIST ---------------------------
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


# --------------------------- MODIFY WORD ---------------------------
@app.route('/modify/<word>')
def modify(word):
  meaning = get_word_meaning(word)
  active_decks = get_custom_lists_of_word(word)
  return render_template('modify.html', word=word, meaning=enumerate(meaning), active_decks=active_decks, decks=g_custom_decks)


@app.route('/mod/_submit', methods=['POST'])
def modify_process_form():
  """
  @brief: Handle form submission for modifying word
  """
  data = request.get_json()
  word    = data["word"]
  meaning = data["meaning"]
  decks   = data["decks"]
  # print(word)
  # print(decks)
  # print(meaning)

  modify_word(word, meaning, decks)
  resp = "Word " + word + " successfully modified!"
  return jsonify(result=resp)


# ============================================================
# =========================== MAIN ===========================
# ============================================================

g_all_decks    = get_word_lists()
g_custom_decks = get_custom_lists()
g_default_decks = get_default_lists()
g_listmans = { l: ListMan(l) for l in g_all_decks}

# print(g_all_decks)
# print(g_custom_decks)
# print(g_default_decks)

if (__name__=="__main__"):
  app.run()

