$(function(){

  let css_selector = document.getElementById('twitter-text-message');
  let css_fontsize = window.getComputedStyle(css_selector, null).getPropertyValue('font-size');
  let css_ls = window.getComputedStyle(css_selector, null).getPropertyValue('letter-spacing');

  scroll_speed = 11.0 - parseFloat(scroll_speed, 10)/10;
  display_delay = display_delay*1000;
  fadein_speed = fadein_speed*1000;
  fadeout_speed = fadeout_speed*1000;
  start_delay = start_delay*1000

  var ws = new WebSocket("ws://127.0.0.1:10356/");

  ws.onmessage = function(message){

    var window_w = window.innerWidth;

    var span = document.createElement('span');

    span.style.position = 'absolute';
    span.style.top = '-1000px';
    span.style.left = '-1000px';

    span.style.whiteSpace = 'nowrap';

    span.innerHTML = message.data;

    span.style.fontSize = css_fontsize;
    span.style.letterSpacing = css_ls;

    document.body.appendChild(span);

    var text_width = span.clientWidth;
    var text_width_int = parseInt(text_width);
    var text_scroll = window_w - text_width_int

    span.parentElement.removeChild(span);

    if (text_width_int >= window_w) {

      $("#twitter-text-message").text(message.data);
      $('#twitter-text-message').animate({opacity: 1},{queue: false,duration: fadein_speed,easing: 'swing'});
      $('#twitter-text-message').animate({marginLeft: 0},{queue: false,duration: fadein_speed,easing: 'swing'}).delay(start_delay);
      $('#twitter-text-message').animate({marginLeft: text_scroll-10},{duration: text_width_int*scroll_speed,easing: 'linear'}).delay(display_delay);
      $('#twitter-text-message').animate({opacity: 0},{duration: fadeout_speed,complete: function(){ws.send('JS'),$('#twitter-text-message').css('margin-left','250px');}});

    }else{

      $("#twitter-text-message").text(message.data);
      $('#twitter-text-message').animate({opacity: 1},{queue: false,duration: fadein_speed,easing: 'swing'});
      $('#twitter-text-message').animate({marginLeft: 0},{queue: false,duration: fadein_speed,easing: 'swing'}).delay(display_delay);
      $('#twitter-text-message').animate({opacity: 0},{duration: fadeout_speed,complete: function(){ws.send('JS'),$('#twitter-text-message').css('margin-left','250px');}});

    }
  }
})
