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

$(document).ready( function() {
  // Scroll to top at reload
  $(this).scrollTop(0);


  $('#submit-form').click( function() {
    // console.log("click");

    var form = $('#word-form');

    var word = form.find("#word").val();
    var defs_json = [];

    var defs_form = form.children(".new-meaning");

    for (var i=0; i<defs_form.length; i++) {
      var m = $(defs_form[i]);
      console.log(m);
      var def = [];
      def["type"]       = m.find(".word-type").val()[0];
      def["meaning"]    = m.find(".word-meaning").val();
      def["meaning_bg"] = m.find(".word-meaning-bg").val();
      def["example"]    = m.find(".word-example").val();
      defs_json.push(def);
    }
    
    // console.log(meanings.length);
    // console.log(word);
    // console.log(defs_json);

    // form[0].reset();
    // form.trigger("reset");
    // $('#word-form').trigger("reset");
    // document.getElementById('word-form').reset();
    // $('form').trigger("reset");

  });



});