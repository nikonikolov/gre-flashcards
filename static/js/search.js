$(document).ready( function() {
  // Scroll to top at reload
  $(this).scrollTop(0);


  function appendResults(data){
    if (data.length > 0){
      $('#search-results').append("<option selected=\"selected\">" + data[0] +"</option>");
    }
    
    for (var i=1; i<data.length; i++) {
      $('#search-results').append("<option>" + data[i] +"</option>");
    }
  }


  function removeList(){
      $('#search-results').empty();
  }


  $('#word').on( 'input', 
    function() {
      var word = $("#word").val();

      $.getJSON($SCRIPT_ROOT + "/search/_query", {
        query: word,
      }, function(data) {
        removeList();
        appendResults(data);
      });
    }
  ); 


  $('#submit-btn').click( 
    function() {
      var word = $("#search-results").val()[0];
        window.location.href = "/words/" + word;
    }
  ); 

});