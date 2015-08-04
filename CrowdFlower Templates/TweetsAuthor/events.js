require(['jquery-noconflict', 'bootstrap-tooltip'], function(jQuery) {
  
  //Ensure MooTools is where it must be
  Window.implement('$', function(el, nc){
    return document.id(el, nc, this.document);
  });
  
  var $ = window.jQuery;

  $(function() {   
    $("a").tooltip();
    
    $("input[value='tweet1']").on("click", function() {
      $("#tweet1-box").removeClass().addClass("panel panel-success");
      $("#tweet1-box .panel-heading h2").html("This tweet is <strong>MORE</strong> credible");
      $("#tweet2-box").removeClass().addClass("panel panel-danger");
      $("#tweet2-box .panel-heading h2").html("This tweet is <strong>LESS</strong> credible");  
      $(".morecredible").val(1);
      $(".lesscredible").val(0);
      $(".same").val(0);
    });
    
    $("input[value='tweet2']").on("click", function() {
      $("#tweet1-box").removeClass().addClass("panel panel-danger");
      $("#tweet1-box .panel-heading h2").html("This tweet is <strong>LESS</strong> credible"); 
      $("#tweet2-box").removeClass().addClass("panel panel-success");
      $("#tweet2-box .panel-heading h2").html("This tweet is <strong>MORE</strong> credible"); 
      $(".morecredible").val(0);
      $(".lesscredible").val(1);
      $(".same").val(0);
    });
    
    $("input[value='same']").on("click", function() {
      $("#tweet1-box").removeClass().addClass("panel panel-default");
      $("#tweet1-box .panel-heading h2").html("Both tweets are <strong>EQUALLY</strong> credible"); 
      $("#tweet2-box").removeClass().addClass("panel panel-default");
      $("#tweet2-box .panel-heading h2").html("Both tweets are <strong>EQUALLY</strong> credible");
      $(".morecredible").val(0);
      $(".lesscredible").val(0);
      $(".same").val(1);
    });
    
    $(".list-group-item").on("click", function(e) {
      e.preventDefault();
      if ($(this).find('input').val() == 0) {
        $(this).find('input').val(1);
        $(this).removeClass().addClass("list-group-item list-group-item-info");
      }
      else if ($(this).find('input').val() == 1) {
        $(this).find('input').val(0);
        $(this).removeClass().addClass("list-group-item");
      }
    });
    
    $(".submit").on("click", function(e) {
      var found = false
      $('.list-group-item').each(function(i, obj) {
        if ($(this).hasClass('list-group-item-info')) {
          found = true;
          return false;
        }
      });    
      if (found) return true;
      
      if(confirm('You have not selected any credibility factors. Are you sure?')) {
        return true;
      }
      
      return false;
    });
  });
});



