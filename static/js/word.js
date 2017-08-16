$(document).ready( function() {
  // Scroll to top at reload
  $(this).scrollTop(0);

  // Include script
  $.getScript("/static/js/common.js", function(){});


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
      reportSuccess("#rm-result", resp.result, false)
    });

  }


  // ----------------- HANDLE ADDITION -----------------
  
  function appendWord(){
    var data = {};
    data["word"] = getWord();
    data["decks"] = parseDecks();
    if (decksEmpty("#add-result", data["decks"])) return;

    $.ajax(
      {
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        url: "/_append",
        success: function (resp) {
          var result = resp["result"];
          var status = resp["status"];
          if (status === "success") 
            reportSuccess("#add-result", result);
          else
            reportWarning("#add-result", result);
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

  function makeWordBold(){
    var meanings  = $('#meaning-block').find(".card-meaning");
    var word = $("#word").html();
    word = word.substring(0, word.length-1);
    var re = new RegExp("(" + word + "\\w*)", 'gi');

    for (var i=0; i<meanings.length; i++) {
      var m = $(meanings[i]);
      el = m.find(".card-meaning-example");
      // el.html( el.html().replace(re, "<b>$1</b>") );
      el.html( el.html().replace(re, "<b>$&</b>") );
    }
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
  makeWordBold();
  $("#options").hide();

  $('#show-meaning').click( 
    function() {
      $('#show-meaning').hide();
      showContent();
      $("#notknow").focus();
    }
  );

  $('#know').bind('click', 
    function() {
      sendResponse(1);
    }
  );

  $('#know').keypress(function(e){
    //Enter key pressed
    if(e.which == 13){
      sendResponse(1);
    }
  });

  $('#notknow').bind('click', 
    function() {
      sendResponse(0);
    }
  );

  $('#notknow').keypress(function(e){
    //Enter key pressed
    if(e.which == 13){
      sendResponse(0);
    }
  });


  $('#add-btn').click( 
    function() {
      appendWord();
    }
  );

  $('#rm-btn').click( 
    function() {
      removeWord();
      sendResponse(true);
    }
  );

  $('#mod-btn').click( 
    function() {
      window.open("/modify/" + getWord(), "_blank")
      // window.location.href = "/modify/" + getWord();
    }
  );


  $('#opt-btn').click( 
    function() {
      $("#opt-btn").hide();
      $("#options").show();
    }
  );


});
