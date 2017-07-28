$(document).ready( function () {	
  console.log("HERE");
	//$("#navigation").load("/navbar/navbar.html");	
	// $("#navigation").load("/navbar/navbar.html", function() {
 //    	$.getScript("/navbar/navbarscript.js");
	// });	

  $("#navigation").load("static/navbar/navbar.html", function() {
      $.getScript("static/navbar/navbarscript.js");
  }); 

  // $("#navigation").load("{{ url_for('static',filename='navbar/navbar.html') }}", function() {
  //     $.getScript("{{ url_for('static',filename='navbar/navbarscript.js') }}");
  // }); 


});

