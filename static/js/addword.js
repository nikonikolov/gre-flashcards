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

  var clone_count = 1;


  $('#newm-btn').click( 
    function() {
      clone_count++;
      $("#m1").clone().attr('id', "m" + clone_count).appendTo("#meanings");  
      $("#m" + clone_count).validator('update');
    }
  );


  $('#rmm-btn').click( 
    function() {
      if(clone_count == 1) return;
      $("#m" + clone_count).remove();  
      clone_count--;
    }
  );

  $('#reset-btn').click( 
    function() {
      $("#result").text("");
    }
  );

  function parseForm(form_data) {
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


  $('#submit-btn').click( 
    function() {

      var form = $('#word-form');
      var form_data = form.find(".new-meaning");

      var word = form.find("#word").val();
      var meaning = parseForm(form_data);
    
      // Pack the word in JSON    
      var data = {};
      data[word] = meaning;

      // Submit the data to Flask
      $.ajax(
        {
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify(data),
          dataType: 'json',
          url: '/addword/_submit',
          success: function (w) {
            $('#reset-btn').trigger('click');
            $("#result").css("color", "green");
            $("#result").text("Successfully added " + w + "!");
          },
          error: function(error) {
            console.log(error);
            $("#result").css("color", "red");
            $("#result").text("Something went wrong!");
        }
      });


      // $.getJSON($SCRIPT_ROOT + page, {
      //   // flag: flag_val,
      //   flag: flag_val,
      // }, function(data) {
      //   // Redirect to the response page
      //   window.location.href = data.result;
      // });
      // return false;

      // console.log(meanings.length);
      // console.log(word);
      // console.log(meaning);

      // form[0].reset();
      // form.trigger("reset");
      // $('#word-form').trigger("reset");
      // document.getElementById('word-form').reset();
      // $('form').trigger("reset");

    }
  );



});