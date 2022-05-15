def isint(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True

def config_verify(sg, os, configparser, datetime, tweetron_variable, window_title, png_icon_path, preset_name):

    msg_sw = 0

    settingvalue_dict_all = tweetron_variable.reset_settingvalue_dict_all(datetime)

    read_config = configparser.RawConfigParser()
    read_config.read('data/preset/' + preset_name + '/config.ini')

    for key_p_key in settingvalue_dict_all.keys():
        if read_config.has_section(key_p_key) == False:
            read_config.add_section(key_p_key)

        for key_c_key, key_c_value in zip(settingvalue_dict_all[key_p_key].keys(), settingvalue_dict_all[key_p_key].values()):
            if read_config.has_option(key_p_key, key_c_key) == False or str(read_config.get(key_p_key, key_c_key)) == '':
                read_config.set(key_p_key, key_c_key, key_c_value)
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


def update_setting_window(sg, os, configparser, datetime, tweetron_variable, main_window, window_title, png_icon_path, preset_name_combo):

    dt_now = datetime.datetime.now()

    if preset_name_combo == '(新規名称未設定)':
        settingvalue_dict_all = tweetron_variable.reset_settingvalue_dict_all(datetime)

        search_word = ''
        nogood_word = ''

        local_since_rb = bool(int(settingvalue_dict_all['main_setting']['since_rb']))

        main_window['-rb_01-'].update(value = local_since_rb)
        main_window['-rb_02-'].update(value = not local_since_rb)

        main_window['-calender_button-'].update(disabled = local_since_rb)
        main_window['-searchdate_h-'].update(disabled = local_since_rb)
        main_window['-searchdate_m-'].update(disabled = local_since_rb)
        main_window['-searchdate_s-'].update(disabled = local_since_rb)

        main_window['-search_word-'].update(value = '')
        main_window['-nogood_word-'].update(value = '')

        for key_name, value_name in zip(settingvalue_dict_all['main_setting'].keys(), settingvalue_dict_all['main_setting'].values()):
            if key_name != 'since_rb':
                main_window['-' + key_name + '-'].update(value = value_name)

    else:
        settingvalue_dict_all = tweetron_variable.reset_settingvalue_dict_all(datetime)

        config_verify(sg, os, configparser, datetime, tweetron_variable, window_title, png_icon_path, preset_name_combo)

        read_main_config = configparser.RawConfigParser()
        read_main_config.read('data/preset/' + preset_name_combo  + '/config.ini')

        for key_p_name in settingvalue_dict_all.keys():
            for key_c_name in settingvalue_dict_all[key_p_name].keys():
                if isint(read_main_config.get(key_p_name, key_c_name)) == True:
                    settingvalue_dict_all[key_p_name][key_c_name] = int(read_main_config.get(key_p_name, key_c_name))
                else:
                    settingvalue_dict_all[key_p_name][key_c_name] = read_main_config.get(key_p_name, key_c_name)

        with open('data/preset/' + preset_name_combo  + '/search_word.txt') as file:
            search_word = file.read()

        with open('data/preset/' + preset_name_combo  + '/nogood_word.txt') as file:
            nogood_word = file.read()

        main_window['-search_word-'].update(value = search_word)
        main_window['-nogood_word-'].update(value = nogood_word)

        local_since_rb = bool(int(settingvalue_dict_all['main_setting']['since_rb']))

        main_window['-rb_01-'].update(value = local_since_rb)
        main_window['-rb_02-'].update(value = not local_since_rb)

        main_window['-calender_button-'].update(disabled = local_since_rb)
        main_window['-searchdate_h-'].update(disabled = local_since_rb)
        main_window['-searchdate_m-'].update(disabled = local_since_rb)
        main_window['-searchdate_s-'].update(disabled = local_since_rb)

        for key_name, value_name in zip(settingvalue_dict_all['main_setting'].keys(), settingvalue_dict_all['main_setting'].values()):
            if key_name != 'since_rb':
                main_window['-' + key_name + '-'].update(value = value_name)

    return search_word, nogood_word, settingvalue_dict_all
