$(document).ready( function() {

  // page = window.location.pathname;
  // console.log(page);
  // page = page.slice(0, page.lastIndexOf('/'));
  // console.log(page);

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

});
