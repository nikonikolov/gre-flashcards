$(document).ready(function(){

	$(".social_pages").hover(
		function(){
			var im = $(this).find(".google_icon");
			var src = im.attr('src');
			var position = src.length-4;
			var hover_src = [src.slice(0, position), '_hover', src.slice(position)].join('');
			im.attr("src",hover_src);
		},
		function(){
			var im = $(this).find(".google_icon");
			var hover_src = im.attr('src');
			var position = hover_src.length-4;
			var src = [hover_src.slice(0, position-6), hover_src.slice(position)].join('');
			im.attr("src",src);
	});

});

