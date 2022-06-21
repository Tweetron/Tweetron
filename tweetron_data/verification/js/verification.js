$(function(){

  const short_button = document.getElementById("short_button");
  const long_button = document.getElementById("long_button");

  var test_message_short = "これはテストメッセージです";
  var test_message_long = "これはテストメッセージです。TweetronはOBSブラウザーソースを使用してツイートを画面上に表示するツールソフトです。";

  test_message_long = test_message_long + test_message_long;

  $("#twitter-shorttext-message").text(test_message_short);
  $("#twitter-longtext-message").text(test_message_long);

  scroll_speed = 11.0 - parseFloat(scroll_speed, 10)/10;
  display_delay = display_delay*1000;
  fadein_speed = fadein_speed*1000;
  fadeout_speed = fadeout_speed*1000;
  start_delay = start_delay*1000;

  var window_w = window.innerWidth;
  var text_width = parseInt($('#twitter-longtext-message').width());
  var text_scroll = window_w - text_width;

  document.getElementById("short_button").onclick = function() {

    $('#twitter-shorttext-message').css('opacity',0);
    $('#twitter-shorttext-message').css('margin-left',250);

    $('#twitter-shorttext-message').animate({opacity: 1},{queue: false,duration: fadein_speed,easing: 'swing'});
    $('#twitter-shorttext-message').animate({marginLeft: 0},{queue: false,duration: fadein_speed,easing: 'swing'}).delay(fadein_speed + display_delay);
    $('#twitter-shorttext-message').animate({opacity: 0},{duration: fadeout_speed,complete: function(){$('#twitter-shorttext-message').css('margin-left','250px');}});

  }

  document.getElementById("long_button").onclick = function() {

    $('#twitter-longtext-message').css('opacity',0);
    $('#twitter-longtext-message').css('margin-left',250);

    $('#twitter-longtext-message').animate({opacity: 1},{queue: false,duration: fadein_speed,easing: 'swing'});
    $('#twitter-longtext-message').animate({marginLeft: 0},{queue: false,duration: fadein_speed,easing: 'swing'}).delay(start_delay + fadein_speed);
    $('#twitter-longtext-message').animate({marginLeft: text_scroll-20},{duration: text_width*scroll_speed,easing: 'linear'}).delay(display_delay);
    $('#twitter-longtext-message').animate({opacity: 0},{duration: fadeout_speed,complete: function(){$('#twitter-longtext-message').css('margin-left','250px');}});;

  }
})
