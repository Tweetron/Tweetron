$(function(){

  let css_selector = document.getElementById('twitter-text-message');
  let css_fontsize = window.getComputedStyle(css_selector, null).getPropertyValue('font-size');
  let css_ls = window.getComputedStyle(css_selector, null).getPropertyValue('letter-spacing');

  const short_button = document.getElementById("short_button");
  const long_button = document.getElementById("long_button");

  var test_message_short = "これはテストメッセージです";
  var test_message_long = "これはテストメッセージです。TweetronはOBSブラウザーソースを使用してツイートを画面上に表示するツールソフトです。";

  test_message_long = test_message_long + test_message_long;

  scroll_speed = 11.0 - parseFloat(scroll_speed, 10)/10;
  display_delay = display_delay*1000;
  fadein_speed = fadein_speed*1000;
  fadeout_speed = fadeout_speed*1000;
  start_delay = start_delay*1000

  var window_w = window.innerWidth;

  var span = document.createElement('span');

  span.style.position = 'absolute';
  span.style.top = '-1000px';
  span.style.left = '-1000px';

  span.style.whiteSpace = 'nowrap';

  span.innerHTML = test_message_long;

  span.style.fontSize = css_fontsize;
  span.style.letterSpacing = css_ls;

  document.body.appendChild(span);

  var text_width = span.clientWidth;
  var text_width_int = parseInt(text_width);
  var text_scroll = window_w - text_width_int

  span.parentElement.removeChild(span);

  document.getElementById("short_button").onclick = function() {

    $('#twitter-text-message').css('opacity',0);
    $('#twitter-text-message').css('margin-left',250);

    $("#twitter-text-message").text(test_message_short);
    $('#twitter-text-message').animate({opacity: 1},{queue: false,duration: fadein_speed,easing: 'swing'});
    $('#twitter-text-message').animate({marginLeft: 0},{queue: false,duration: fadein_speed,easing: 'swing'}).delay(display_delay);
    $('#twitter-text-message').animate({opacity: 0},{duration: fadeout_speed,complete: function(){$('#twitter-text-message').css('margin-left','250px');}});

  }

  document.getElementById("long_button").onclick = function() {

    $('#twitter-text-message').css('opacity',0);
    $('#twitter-text-message').css('margin-left',250);

    $("#twitter-text-message").text(test_message_long);
    $('#twitter-text-message').animate({opacity: 1},{queue: false,duration: fadein_speed,easing: 'swing'});
    $('#twitter-text-message').animate({marginLeft: 0},{queue: false,duration: fadein_speed,easing: 'swing'}).delay(start_delay);
    $('#twitter-text-message').animate({marginLeft: text_scroll-10},{duration: text_width_int*scroll_speed,easing: 'linear'}).delay(display_delay);
    $('#twitter-text-message').animate({opacity: 0},{duration: fadeout_speed,complete: function(){$('#twitter-text-message').css('margin-left','250px');}});;

  }
})
