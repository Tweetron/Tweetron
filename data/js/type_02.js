$(function(){

  scroll_speed = 11.0 - parseFloat(scroll_speed, 10)/10;
  display_delay = display_delay*1000;
  fadein_speed = fadein_speed*1000;
  fadeout_speed = fadeout_speed*1000;
  start_delay = start_delay*1000;

  var ws = new WebSocket("ws://127.0.0.1:" + port_number + "/");

  ws.onmessage = function(message){

    var message_data = message.data.split(/\r\n|\n/);

    $("#twitter-text-username").text(message_data[0]);
    $("#twitter-text-message").text(message_data[1]);

    var window_w = window.innerWidth;
    var text_width = parseInt($('#twitter-text-message').width());
    var text_scroll = window_w - text_width;

    if (text_width >= window_w) {

      $('#twitter-text-username').animate({opacity: 1},{duration: fadein_speed,easing: 'swing'}).delay((display_delay + start_delay) + (text_width*2));
      $('#twitter-text-message').animate({opacity: 1},{queue: false,duration: fadein_speed,easing: 'swing'});
      $('#twitter-text-message').animate({marginLeft: 0},{queue: false,duration: fadein_speed,easing: 'swing'}).delay(fadein_speed + start_delay);
      $('#twitter-text-message').animate({marginLeft: text_scroll-20},{duration: text_width*2,easing: 'linear'}).delay(display_delay);
      $('#twitter-text-username').animate({opacity: 0},{duration: fadeout_speed,easing: 'swing'});
      $('#twitter-text-message').animate({opacity: 0},{duration: fadeout_speed,complete: function(){ws.send('JS'),$('#twitter-text-message').css('margin-left','250px');}});

    }else{

      $('#twitter-text-username').animate({opacity: 1},{duration: fadein_speed,easing: 'swing'}).delay(fadein_speed + display_delay);
      $('#twitter-text-message').animate({opacity: 1,marginLeft: 0},{duration: fadein_speed,easing: 'swing'}).delay(fadein_speed + display_delay);
      $('#twitter-text-username').animate({opacity: 0},{duration: fadeout_speed,easing: 'swing'});
      $('#twitter-text-message').animate({opacity: 0},{duration: fadeout_speed,complete: function(){ws.send('JS'),$('#twitter-text-message').css('margin-left','250px');}});

    }
  }
})
