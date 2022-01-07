# coding: utf-8

def save_css(font_name, color_code, font_size, font_path = 'null'):

    if font_path == 'null':
        css_font_data = ('@font-face {\n'
                    '  font-family: \'datafont\';\n'
                    '  src: local(\'' + str(font_name) + '\');\n'
                    '}\n')

    else:
        css_font_data = ('@font-face {\n'
                    '  font-family: \'datafont\';\n'
                    '  src: url(\'' + font_path + '\') format(\'truetype\');\n'
                    '}\n')

    css_body_data = ('\n'
                '#textarea{\n'
                '\n'
                '   overflow: hidden;\n'
                '\n'
                '}\n'
                '\n'
                '#twitter-text-message{\n'
                '\n'
                '  font-family: \'datafont\', sans-serif;\n'
                '  font-size: ' + str(font_size) + 'px;\n'
                '  color: ' + str(color_code) + ';\n'
                '  letter-spacing: 0;\n'
                '\n'
                '  opacity: 0;\n'
                '  white-space: nowrap;\n'
                '  margin-left: 250px;\n'
                '  overflow: hidden;\n'
                '\n'
                '}\n'
                '\n'
                '#twitter-text-username{\n'
                '\n'
                '  font-family: \'datafont\', sans-serif;\n'
                '  font-size: ' + str(int(font_size)-10) + 'px;\n'
                '  color: ' + str(color_code) + ';\n'
                '  letter-spacing: 0;\n'
                '\n'
                '  opacity: 0;\n'
                '  white-space: nowrap;\n'
                '  margin-left: 0px;\n'
                '  overflow: hidden;\n'
                '\n'
                '}')

    css_data = css_font_data + css_body_data

    with open('data/css/style.css', mode='w', encoding='utf-8') as file:
        file.write(css_data)

def save_test_css(font_name, color_code, font_size, font_path = 'null'):

    if font_path == 'null':
        css_font_data = ('@font-face {\n'
                    '  font-family: \'datafont\';\n'
                    '  src: local(\'' + str(font_name) + '\');\n'
                    '}\n')

    else:
        css_font_data = ('@font-face {\n'
                    '  font-family: \'datafont\';\n'
                    '  src: url(\'' + font_path + '\') format(\'truetype\');\n'
                    '}\n')

    css_body_data = ('\n'
                '#twitter-text-message{\n'
                '\n'
                '  font-family: \'datafont\', sans-serif;\n'
                '  font-size: ' + str(font_size) + 'px;\n'
                '  color: ' + str(color_code) + ';\n'
                '  letter-spacing: 0;\n'
                '  overflow: hidden;\n'
                '\n'
                '}')

    css_data = css_font_data + css_body_data

    with open('data/verification/css/style_html.css', mode='w', encoding='utf-8') as file:
        file.write(css_data)

def save_test_html(text):

    html_data = ('<!DOCTYPE html>\n'
                '<html lang="ja">\n'
                '\n'
                '  <head>\n'
                '      <meta charset="utf-8"/>\n'
                '      <title>Tweetron</title>\n'
                '      <link rel="stylesheet" href="css/style_html.css">\n'
                '  </head>\n'
                '\n'
                '  <body>\n'
                '    <div id="twitter-text-message">' + text + '</div>\n'
                '  </body>\n'
                '\n'
                '</html>')

    with open('data/verification/verification.html', mode='w', encoding='utf-8') as file:
        file.write(html_data)

def save_js_data(scroll_speed, display_delay, fadein_speed, fadeout_speed, start_delay, type):

    js_data = ('var scroll_speed = ' + scroll_speed + ';\n'
               'var display_delay = ' + display_delay + ';\n'
               'var fadein_speed = ' + fadein_speed + ';\n'
               'var fadeout_speed = ' + fadeout_speed + ';\n'
               'var start_delay = ' + start_delay + ';')

    if type == 0:
        with open('data/verification/js/verification_data.js', mode='w', encoding='utf-8') as file:
            file.write(js_data)

    elif type == 1:
        with open('data/js/data.js', mode='w', encoding='utf-8') as file:
            file.write(js_data)

def save_js_portnumber(portnumber):

    js_data = "var port_number = '" + str(portnumber) + "';"

    with open('data/js/port_number.js', mode='w', encoding='utf-8') as file:
        file.write(js_data)
