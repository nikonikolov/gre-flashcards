$(document).ready( function() {

  // ----------------- REPORT STATUS -----------------
  
  function reportError(el, msg) {
    $(el).css("color", "red");
    $(el).text(msg);
  }

  function reportSuccess(el, msg) {
    $(el).css("color", "green");
    $(el).text(msg);
  }

  function reportWarning(el, msg) {
    $(el).css("color", "#FF8C00");
    $(el).text(msg);
  }

  // ----------------- HANDLE REMOVAL -----------------
  
  function getQueryPath(word){
    var page = window.location.pathname;
    // console.log(page);
    var maybe_word = page.substring(page.lastIndexOf('/') + 1);
    if (maybe_word == word){
      page = page.slice(0, page.lastIndexOf('/'));
    }
    var deck = page.substring(page.lastIndexOf('/') + 1);

    return "/vocab/" + deck + "/_remove"
  }

  function getWord(){
    var word = $('.card-title').html();
    word = word.replace(/\s/g, '');
    return word;
  }

  function removeWord(){
    var wordname = getWord();
    var url = getQueryPath(wordname);

    $.getJSON($SCRIPT_ROOT + url, {
      word: wordname,
    }, function(resp) {
      reportSuccess("#rm-result", resp.result)
    });

  }

  function parseDecks() {
    var form = $('#decks-form');
    var form_decks = form.find(".deck");

    decks = []
    for (var i=0; i<form_decks.length; i++) {
      var d = $(form_decks[i]);
      var d_input = d.find(".deck-input").is(':checked');

      if (d_input){
        var d_name = d.find(".deck-name").html();
        decks.push(d_name);
      } 
    }
    return decks;
  }

  // ----------------- HANDLE ADDITION -----------------
  
  function appendWord(){
    var wordname = getWord();
    var decks = parseDecks();
    var data = {};
    data["word"] = wordname;
    data["decks"] = decks;

    $.ajax(
      {
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        url: "/_append",
        success: function (resp) {
          reportWarning("#add-result", resp["result"])
        },
        error: function(error) {
          console.log(error);
          reportError("Something went wrong!");
      }
    });

  }


  // ----------------- HANDLE MEANING -----------------

  function hideContent() {
    $('#meaning-block').hide();
    $('#know').hide();
    $('#notknow').hide();
  }

  function showContent() {
    $('#meaning-block').show();
    $('#know').show();
    $('#notknow').show();
  }

  function sendResponse(flag_val) {
    var page = window.location.pathname + "/_know";
    console.log(flag_val)

    $.getJSON($SCRIPT_ROOT + page, {
      // flag: flag_val,
      flag: flag_val,
    }, function(data) {
      // Redirect to the response page
      window.location.href = data.result;
    });
    return false;
  }


  // ----------------- START EXECUTION -----------------
  hideContent();

  $('#show-meaning').click( 
    function() {
      console.log("click")
      $('#show-meaning').hide();
      showContent();
    }
  );

  $('#know').bind('click', 
    function() {
      // sendResponse(true);
      sendResponse(1);
    }
  );

  $('#notknow').bind('click', 
    function() {
      console.log("notknow");
      // sendResponse(false);
      sendResponse(0);
    }
  );

  $('#add-btn').click( 
    function() {
      appendWord();
    }
  );

  $('#rm-btn').click( 
    function() {
      removeWord();
    }
  );

});
