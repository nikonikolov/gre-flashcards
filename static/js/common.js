
/* JSON structure is as follows

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


 */


// ----------------- REPORT STATUS -----------------

function reportSuccess(el, msg, reset) {
  if (typeof(reset)==='undefined') reset = true;

  if (reset) { 
    $('#reset-btn').trigger('click');
  }
  
  $(el).css("color", "green");
  $(el).text(msg);
}


function reportError(el, msg) {
  $(el).css("color", "red");
  $(el).text(msg);
}


function reportWarning(el, msg) {
  $(el).css("color", "#FF8C00");
  $(el).text(msg);
}


// ----------------- PARSE FORM -----------------

function parseWord() {
  return $("#word").val();
}


function parseMeanings() {
  var form = $('#word-form');
  var form_data  = form.find(".new-meaning");

  var meaning = [];

  // Parse the form
  for (var i=0; i<form_data.length; i++) {
    var m = $(form_data[i]);
    var def = {};
    def["type"]       = m.find(".word-type").val()[0];
    def["meaning"]    = m.find(".word-meaning").val();
    def["meaning_bg"] = m.find(".word-meaning-bg").val();
    def["example"]    = m.find(".word-example").val();
    meaning.push(def);
  }

  return meaning;
}


function parseDecks() {
  var form = $('#word-form');
  var form_decks = form.find(".deck");
  
  decks = []
  for (var i=0; i<form_decks.length; i++) {
    var d = $(form_decks[i]);
    var d_input = d.find(".deck-input").is(':checked');

    if (d_input){
      var d_name = d.find(".deck-name").html();
      decks.push(d_name);
    } 
    // console.log(d_input);
    // console.log(d_name);
  }

  // if (decks.length < 1 && check_decks){
  //   reportError(report_el, "Error: You must select at least one list to add the word to!")
  //   return;
  // }

  return decks;
}


function packWordJSON() {
  // Parse the form
  var word    = parseWord();
  var meaning = parseMeanings();
  var decks   = parseDecks();

  // Pack the word in JSON    
  var data = {};
  data["word"] = word;
  data["meaning"] = meaning;
  data["decks"] = decks;
  return data;
}


function decksEmpty(report_el, decks){
  if (decks.length < 1){
    reportError(report_el, "Error: You must select at least one list to add the word to!")
    return true;
  }
  return false;
}

// ----------------- MANIPULATE FORM -----------------


function removeClonedInputs(elm){
  /*
  @brief: Remove the inputs when an entry in a form is cloned
   */
  $(elm).find("input[type=text]").attr("value", "");
  $(elm).find("input[type=checkbox]").removeAttr("checked");
  $(elm).find("option").removeAttr("selected");
  $(elm).find("textarea").html("");

  // $('#word-form').find("input[type=text]").attr("value", "");
  // $('#word-form').find("input[type=checkbox]").removeAttr("checked");
  // $('#word-form').find("option").removeAttr("selected");
  // $('#word-form').find("textarea").html("");
}



