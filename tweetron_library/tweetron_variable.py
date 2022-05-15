def reset_settingvalue_dict_all(datetime):

    dt_now = datetime.datetime.now()

    settingvalue_dict_all = {
        'main_setting': {
            'preset_name': '',
            'reply_exclusion': 0,
            'emoji_exclusion': 0,
            'searchdate': dt_now.strftime("%Y-%m-%d"),
            'searchdate_h': 0,
            'searchdate_m': 0,
            'searchdate_s': 0,
            'since_rb': 0
        },

        'filter_setting': {
            'search_command': ''
        },

        'text_setting': {
            'text_fontsize': 25,
            'text_color': '#000000',
            'text_fontname': 'Meiryo UI',
            'text_fontpath': ''
        },

        'display_setting': {
            'text_displaytype': 1,
            'text_scrollspeed': 80,
            'text_displaydelay': 3,
            'text_fadeinspeed': 2,
            'text_fadeoutspeed': 2,
            'text_startdelay': 2,
            'text_loadloop': 1
        }
    }

    return settingvalue_dict_all
