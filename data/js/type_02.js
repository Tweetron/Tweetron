$(function(){

  let css_selector = document.getElementById('twitter-text-message');
  let css_fontsize = window.getComputedStyle(css_selector, null).getPropertyValue('font-size');
  let css_ls = window.getComputedStyle(css_selector, null).getPropertyValue('letter-spacing');

  var scrollspeed = 0;
  var loopcnt = 0;

  var ws = new WebSocket("ws://127.0.0.1:10356/");

  ws.onmessage = function(message){

    if (loopcnt == 0){
      scrollspeed = 11.0 - parseFloat(message.data, 10)/10;
      console.log(scrollspeed);

    }else{

      var window_w = window.innerWidth;

      var span = document.createElement('span');

      span.style.position = 'absolute';
      span.style.top = '-1000px';
      span.style.left = '-1000px';

      span.style.whiteSpace = 'nowrap';

      var ws_data = message.data;

      var message_data = ws_data.split(/\r\n|\n/);

      span.innerHTML = message_data[1];

      span.style.fontSize = css_fontsize;
      span.style.letterSpacing = css_ls;

      document.body.appendChild(span);

      var text_width = span.clientWidth;
      var text_width_int = parseInt(text_width);
      var text_scroll = window_w - text_width_int

      span.parentElement.removeChild(span);

      if (text_width_int >= window_w) {

        $("#twitter-text-username").text(message_data[0]);
        $("#twitter-text-message").text(message_data[1]);
        $('#twitter-text-username').animate({opacity: 1},{duration: 2000,easing: 'swing'}).delay(4000+text_width_int*2);
        $('#twitter-text-message').animate({opacity: 1},{queue: false,duration: 2000,easing: 'swing'});
        $('#twitter-text-message').animate({marginLeft: 0},{queue: false,duration: 2000,easing: 'swing'}).delay(3000);
        $('#twitter-text-message').animate({marginLeft: text_scroll-10},{duration: text_width_int*2,easing: 'linear'}).delay(3000);
        $('#twitter-text-username').animate({opacity: 0},{duration: 2000,easing: 'swing'});
        $('#twitter-text-message').animate({opacity: 0},{duration: 2000,complete: function(){ws.send('JS'),$('#twitter-text-message').css('margin-left','250px');}});

      }else{

        $("#twitter-text-username").text(message_data[0]);
        $("#twitter-text-message").text(message_data[1]);
        $('#twitter-text-username').animate({opacity: 1},{duration: 2000,easing: 'swing'}).delay(5000);
        $('#twitter-text-message').animate({opacity: 1,marginLeft: 0},{duration: 2000,easing: 'swing'}).delay(5000);
        $('#twitter-text-username').animate({opacity: 0},{duration: 2000,easing: 'swing'});
        $('#twitter-text-message').animate({opacity: 0},{duration: 2000,complete: function(){ws.send('JS'),$('#twitter-text-message').css('margin-left','250px');}});

      }
    }
    loopcnt++
  }
})
