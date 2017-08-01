$(document).ready( function () {  

  function itemHighlight(traverse_class, classOn) {
    var page = window.location.pathname;

    $(traverse_class).each( 
      function (){
        var href = $(this).find("a").attr('href');
        if( href == page){
          $(this).addClass(classOn);
        }
        else{
          $(this).removeClass(classOn);
        }
      }
    );
  }

  itemHighlight('.nav-item', 'active');
  // itemHighlight('.subj_item', 'subj_item_on');

  // $("#nav_bar").hover(
  //   function(){
  //     $("#nav_bar").toggleClass("nav_hover");
  //   },
  //   function(){
  //     $("#nav_bar").toggleClass("nav_hover");
  // });

  // $("#drop_down_container").hover(
  //   function(){
  //     $("#subj_menu").slideDown(200, function(){});
  //   },
  //   function(){
  //     setTimeout(function(){}, 1000);
  //     $("#subj_menu").slideUp(200, function(){});
  // }); 

});