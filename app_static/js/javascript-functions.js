$(function(){
  var profile_name = $('.profile_name').text().split(" ");
  var image_text = profile_name[0].charAt(0) + profile_name[1].charAt(0);
  $('#profileImage').text(image_text);
});