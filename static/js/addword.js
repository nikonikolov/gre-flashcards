
$(document).ready( function() {
  // Scroll to top at reload
  $(this).scrollTop(0);

  // Include script
  $.getScript("/static/js/common.js", function(){});


  // ----------------- START EXECUTION -----------------

  var clone_count = 1;


  $('#newm-btn').click( 
    function() {
      clone_count++;
      $("#m1").clone().attr('id', "m" + clone_count).appendTo("#meanings");  
      removeClonedInputs("#m" + clone_count);
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


  $('#submit-btn').click( 
    function() {

      // Get the form data in JSON
      data = packWordJSON();
      if (decksEmpty("#result", data["decks"])) return;

      // Submit the data to Flask
      $.ajax(
        {
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify(data),
          dataType: 'json',
          url: '/addword/_submit',
          success: function (resp) {
            var status = resp["status"];
            if (status != "Success"){
              reportError("#result", status);
            }
            else{
              reportSuccess("#result", "Successfully added " + resp["word"] + "!");
            }
          },
          error: function(error) {
            console.log(error);
            reportError("#result", "Something went wrong!");
        }
      });

    }
  );


});