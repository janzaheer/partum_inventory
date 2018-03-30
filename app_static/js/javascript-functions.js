(function($){
	"use strict";

$(document).ready(function(){
  var firstName = "Hasnan";
  var lastName = "Amin";
  var abc = firstName.charAt(0) + lastName.charAt(0);
  
  var profileImage = $('#profileImage').text(abc);
});

})(jQuery);