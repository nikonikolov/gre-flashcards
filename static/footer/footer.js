$(document).ready( function () {	
	//$("#navigation").load("/navbar/navbar.html");	
	$("#footer").load("/footer/footer.html", function() {
    	$.getScript("/footer/footerscript.js");
	});	
});