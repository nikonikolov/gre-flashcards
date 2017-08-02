
$(document).ready( function() {
  // Scroll to top at reload
  $(this).scrollTop(0);

  // Include script
  $.getScript("/static/js/common.js", function(){});


  // ----------------- HANDLE MEANINGS -----------------

  function count_meanings(){
    var form = $('#word-form');
    var form_data  = form.find(".new-meaning");
    return form_data.length
  }

  // ----------------- START EXECUTION -----------------

  var clone_count = count_meanings();


  $('#newm-btn').click( 
    function() {
      $("#m0").clone().attr('id', "m" + clone_count).appendTo("#meanings");
      removeClonedInputs("#m" + clone_count);
      $("#m" + clone_count).validator('update');
      clone_count++;
    }
  );


  $('#rmm-btn').click( 
    function() {
      if(clone_count == 1) return;
      clone_count--;
      $("#m" + clone_count).remove();  
    }
  );


  $('#reset-btn').click( 
    function() {
      window.location.href = "/";
      // history.back();
      // clearForm();
      // $("#result").text("");
    }
  );


  $('#submit-btn').click( 
    function() {

      // Get the form data in JSON
      data = packWordJSON(false);

      // Submit the data to Flask
      $.ajax(
        {
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify(data),
          dataType: 'json',
          url: '/mod/_submit',
          success: function (resp) {
            reportSuccess("#result", resp.result, true);
          },
          error: function(error) {
            console.log(error);
            reportError("#result","Something went wrong!");
        }
      });


    }
  );

});