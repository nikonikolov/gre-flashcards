$(document).ready( function() {

  page = window.location.pathname;
  console.log(page);
  page = page.slice(0, page.lastIndexOf('/'));
  console.log(page);

  $('#meaning-block').hide();

  $('#show-meaning').click( 
    function() {
      console.log("click")
      $('#meaning-block').show();
      $('#show-meaning').hide();
    }
  );

});
