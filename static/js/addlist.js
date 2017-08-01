$(document).ready( function() {
  // Scroll to top at reload
  $(this).scrollTop(0);

  $('#reset-btn').hide();

  function reportError(msg) {
    $("#result").css("color", "red");
    $("#result").text(msg);
  }

  function reportSuccess(msg) {
    $('#reset-btn').trigger('click');
    $("#result").css("color", "green");
    $("#result").text(msg);
  }


  $('#submit-btn').click( 
    function() {
      var listname = $("#deck").val();

      $.getJSON($SCRIPT_ROOT + "/addlist/_submit", {
        deck: listname,
      }, function(resp) {
        var status = resp["status"];
        if (status != "Success"){
          reportError(status);
        }
        else{
          reportSuccess("Successfully added the list " + resp["deck"] + "!")
        }
      });
    }
  ); 

});




