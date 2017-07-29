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
  with open(file_path, 'rw') as f:
    data = json.load(f)
    if word in data:
      data[word] += meaning
    else:
      data[word] = meaning
    write_file_obj(data, f)


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
      return "Word Not Found"
  
  else:
    return render_template('word.html', word_list=listname, word=word, meaning=meaning)


def get_and_read_lman(listname):
  lman = listmans[str(listname)]
  lman.read_data()
  return lman


# --------------------------- FLASK ---------------------------

@app.route('/')
def home():
  wordlists = get_word_lists()
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
    return "List Learned"
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
  return render_template('addword.html', num=1)




# --------------------------- MAIN ---------------------------
listmans = { l: WordList(l) for l in get_word_lists()}

if (__name__=="__main__"):
  app.run()

