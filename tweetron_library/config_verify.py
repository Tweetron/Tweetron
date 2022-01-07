def config_verify(os, configparser, datetime, sg, window_title, png_icon_path, preset_name):

    msg_sw = 0

    dt_now = datetime.datetime.now()

    read_config = configparser.RawConfigParser()
    read_config.read('data/preset/' + preset_name + '/config.ini')

    if read_config.has_section('main_setting') == False:
        read_config.add_section('main_setting')
        read_config.set('main_setting', 'preset_name', preset_name)
        read_config.set('main_setting', 'since_rb', 0)
        read_config.set('main_setting', 'reply_exclusion', 0)
        read_config.set('main_setting', 'specity_date', dt_now.strftime("%Y-%m-%d"))
        read_config.set('main_setting', 'specity_h', 0)
        read_config.set('main_setting', 'specity_m', 0)
        read_config.set('main_setting', 'specity_s', 0)
        msg_sw = 1

    elif read_config.has_section('main_setting') == True:

        if read_config.has_option('main_setting', 'preset_name') == False or str(read_config.get('main_setting', 'preset_name')) == '':
            read_config.set('main_setting', 'preset_name', preset_name)
            msg_sw = 1

        if read_config.has_option('main_setting', 'since_rb') == False or str(read_config.get('main_setting', 'since_rb')) == '':
            read_config.set('main_setting', 'since_rb', 0)
            msg_sw = 1

        if read_config.has_option('main_setting', 'reply_exclusion') == False or str(read_config.get('main_setting', 'reply_exclusion')) == '':
            read_config.set('main_setting', 'reply_exclusion', 0)
            msg_sw = 1

        if read_config.has_option('main_setting', 'emoji_exclusion') == False or str(read_config.get('main_setting', 'emoji_exclusion')) == '':
            read_config.set('main_setting', 'emoji_exclusion', 0)
            msg_sw = 1

        if read_config.has_option('main_setting', 'specity_date') == False or str(read_config.get('main_setting', 'specity_date')) == '':
            read_config.set('main_setting', 'specity_date', dt_now.strftime("%Y-%m-%d"))
            msg_sw = 1

        if read_config.has_option('main_setting', 'specity_h') == False or str(read_config.get('main_setting', 'specity_h')) == '':
            read_config.set('main_setting', 'specity_h', 0)
            msg_sw = 1

        if read_config.has_option('main_setting', 'specity_m') == False or str(read_config.get('main_setting', 'specity_m')) == '':
            read_config.set('main_setting', 'specity_m', 0)
            msg_sw = 1

        if read_config.has_option('main_setting', 'specity_s') == False or str(read_config.get('main_setting', 'specity_s')) == '':
            read_config.set('main_setting', 'specity_s', 0)
            msg_sw = 1

    if read_config.has_section('filter_setting') == False:
        read_config.add_section('filter_setting')
        read_config.set('filter_setting', 'search_command', 'null')
        msg_sw = 1

    elif read_config.has_section('filter_setting') == True:

        if read_config.has_option('filter_setting', 'search_command') == False or str(read_config.get('filter_setting', 'search_command')) == '':
            read_config.set('filter_setting', 'search_command', 'null')
            msg_sw = 1

    if read_config.has_section('text_setting') == False:
        read_config.add_section('text_setting')
        read_config.set('text_setting', 'streamtext_font_size', 25)
        read_config.set('text_setting', 'streamtext_color', '#000000')
        read_config.set('text_setting', 'streamtext_font_name', 'Meiryo UI')
        read_config.set('text_setting', 'streamtext_font_path', 'null')
        msg_sw = 1

    elif read_config.has_section('text_setting') == True:

        if read_config.has_option('text_setting', 'streamtext_font_size') == False or str(read_config.get('text_setting', 'streamtext_font_size')) == '':
            read_config.set('text_setting', 'streamtext_font_size', 25)
            msg_sw = 1

        if read_config.has_option('text_setting', 'streamtext_color') == False or str(read_config.get('text_setting', 'streamtext_color')) == '':
            read_config.set('text_setting', 'streamtext_color', '#000000')
            msg_sw = 1

        if read_config.has_option('text_setting', 'streamtext_font_name') == False or str(read_config.get('text_setting', 'streamtext_font_name')) == '':
            read_config.set('text_setting', 'streamtext_font_name', 'Meiryo UI')
            msg_sw = 1

        if read_config.has_option('text_setting', 'streamtext_font_path') == False or str(read_config.get('text_setting', 'streamtext_font_path')) == '':
            read_config.set('text_setting', 'streamtext_font_path', 'null')
            msg_sw = 1

    if read_config.has_section('textdisplay_setting') == False:
        read_config.add_section('textdisplay_setting')
        read_config.set('textdisplay_setting', 'streamtext_displaytype', 1)
        read_config.set('textdisplay_setting', 'streamtext_scrollspeed', 80)
        read_config.set('textdisplay_setting', 'streamtext_displaydelay', 5)
        read_config.set('textdisplay_setting', 'streamtext_fadeinspeed', 3)
        read_config.set('textdisplay_setting', 'streamtext_fadeoutspeed', 3)
        read_config.set('textdisplay_setting', 'streamtext_startdelay', 3)
        msg_sw = 1

    elif read_config.has_section('textdisplay_setting') == True:

        if read_config.has_option('textdisplay_setting', 'streamtext_displaytype') == False or str(read_config.get('textdisplay_setting', 'streamtext_displaytype')) == '':
            read_config.set('textdisplay_setting', 'streamtext_displaytype', 1)
            msg_sw = 1

        if read_config.has_option('textdisplay_setting', 'streamtext_scrollspeed') == False or str(read_config.get('textdisplay_setting', 'streamtext_scrollspeed')) == '':
            read_config.set('textdisplay_setting', 'streamtext_scrollspeed', 80)
            msg_sw = 1

        if read_config.has_option('textdisplay_setting', 'streamtext_displaydelay') == False or str(read_config.get('textdisplay_setting', 'streamtext_displaydelay')) == '':
            read_config.set('textdisplay_setting', 'streamtext_displaydelay', 5)
            msg_sw = 1

        if read_config.has_option('textdisplay_setting', 'streamtext_fadeinspeed') == False or str(read_config.get('textdisplay_setting', 'streamtext_fadeinspeed')) == '':
            read_config.set('textdisplay_setting', 'streamtext_fadeinspeed', 3)
            msg_sw = 1

        if read_config.has_option('textdisplay_setting', 'streamtext_fadeoutspeed') == False or str(read_config.get('textdisplay_setting', 'streamtext_fadeoutspeed')) == '':
            read_config.set('textdisplay_setting', 'streamtext_fadeoutspeed', 3)
            msg_sw = 1

        if read_config.has_option('textdisplay_setting', 'streamtext_startdelay') == False or str(read_config.get('textdisplay_setting', 'streamtext_startdelay')) == '':
            read_config.set('textdisplay_setting', 'streamtext_startdelay', 3)
            msg_sw = 1

    if os.path.exists('data/preset/' + preset_name + '/search_word.txt') == False:
        with open('data/preset/' + preset_name + '/search_word.txt', mode='w') as file:
            file.write('')
        msg_sw = 1

    if os.path.exists('data/preset/' + preset_name + '/nogood_word.txt') == False:
        with open('data/preset/' + preset_name + '/nogood_word.txt', mode='w') as file:
            file.write('')
        msg_sw = 1

    if msg_sw == 1:
        with open('data/preset/' + preset_name + '/config.ini', 'w') as file:
            read_config.write(file)

        sg.popup_ok('プリセットファイルが破損していたため自動修復を行いました', title = window_title, icon = png_icon_path)
