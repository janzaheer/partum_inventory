$(function(){
  var profile_name = $('.profile_name').text().split(" ");
  if (profile_name.length > 1) {

      console.log(profile_name.length);
      var image_text = profile_name[0].charAt(0) + profile_name[1].charAt(0);
  } else {
      console.log(profile_name.length);
    var image_text = profile_name[0].charAt(0);
  }
  $('#profileImage').text(image_text);
});