# GRE Flashcards

Webapp for studying GRE Flashcards

## Running

```
cd gre-flashcards
./run.sh
```

Then go to page http://localhost:5000

Use `ctrl+shift+r` for refreshing in order to bypass the browser cache


## Changing the JSON structure


### Python side changes

1. Make the necessary changes in `txt2json.py`
2. Run the script to write the new database

```
cd pyscripts
python txt2json.py
```

3. The above step will write the database in `original-data/json/`. The database
is composed of 4 big lists
- `all.json`
- `advanced.json`
- `basic.json`
- `high-freq.json`

To split the database run

```
cd pyscripts
python split_from_disk.py
```

This will read the current split of the default lists (i.e. the ones mentioned 
above) from the `data/` folder and overwrite the database in `data/` with the
new JSON structure. It will also overwrite `data/all.json` with the new JSON
structure.

**CAUTION: YOU NEED TO MAKE CHANGES TO `split_from_disk.py` SO THAT YOU KEEP 
WORDS THAT YOU HAVE ADDED TO `data/all.json`. YOU ALSO NEED TO UNCOMMENT AND 
FINISH WRITING THE CODE IN THAT FILE SO THAT ANY CHANGES YOU HAVE MADE IN THE
MEANINGS OF THE DEFAULT WORDS WILL BE REFLECTED IN THE NEW STRUCTURE**

### HTML side changes

1. Modify `word.html` in order to change the word display template
2. Modify `addword.html` in order to add/remove the relevant fields for the word
meaning
3. Modify `modify.html` in order to add/remove the relevant fields for the word
meaning


### JS side changes

1. No need to modify anything in `word.js`
2. No need to modify anything in `addword.js` or `modify.js`
2. DO MODIFY `parseMeanings()` in `common.js`



