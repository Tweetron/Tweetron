'''

Tweetron_GUI.py

-
MIT License

Copyright (c) 2021 Cube

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-

'''

# coding: utf-8

#-------------------------------------------------------------------------------

#Lib import

#-------------------------------------------------------------------------------

import PySimpleGUI as sg
import tweepy
import webbrowser
import configparser
import time
import os
import datetime
from tkinter import font
import tkinter
import sys
import subprocess
import shutil
import json
import psutil

from tweetron_layout import window_layout, menu_layout, window_theme
from tweetron_library import webscript_save, utility, tweetron_variable

import api_key
import software_info

#-------------------------------------------------------------------------------

#read setting file

#-------------------------------------------------------------------------------

software_version = software_info.VERSION()
window_title = 'Tweetron ' + software_version
png_icon_path = 'tweetron_data/img/icon.ico'
font_name = 'Meiryo UI'

consumer_key = api_key.CONSUMER_KEY()
consumer_secret = api_key.CONSUMER_SECRET()
callback_url = 'oob'

dt_now = datetime.datetime.now()
current_path = os.getcwd()

main_config = configparser.ConfigParser()
main_config.read('tweetron_data/ini/config.ini', encoding='utf-8')

twitter_oauth_sw = int(main_config.get('MainConfig', 'oauth2_sw'))
port_number = main_config.get('MainConfig', 'portnumber')

sg.LOOK_AND_FEEL_TABLE['theme'] = window_theme.white(sg)
sg.theme('theme')

root = tkinter.Tk()
fonts_list = list(font.families())
fonts_list.sort()
root.destroy()

dir_files = os.listdir('tweetron_data/preset')
preset_list = [f for f in dir_files if os.path.isdir(os.path.join('tweetron_data/preset', f))]
preset_list.append('(新規名称未設定)')

search_word = ''
nogood_word = ''

settingvalue_dict_all = tweetron_variable.reset_settingvalue_dict_all(datetime)
template_list = ['未実装']

time_h_list = [num for num in range(25)]
time_m_list = [num for num in range(61)]
time_s_list = [num for num in range(61)]
fontsize_list = [num for num in range(61)]
text_scrollspeed_list = [num for num in range(101)]

#-------------------------------------------------------------------------------

#twitter authentication

#-------------------------------------------------------------------------------

if twitter_oauth_sw == 0:

    main_window = window_layout.make_welcome_window(sg, window_title, png_icon_path)

    while True:
        main_event, main_values = main_window.read()

        if main_event == sg.WIN_CLOSED: break

        if main_event == '-wikipage_open-': webbrowser.open('https://github.com/Tweetron/Tweetron/wiki')

        if main_event == '-Auth_Button-':

            main_window.Element('-Auth_Button-').Update(disabled = True)

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
            auth_url = auth.get_authorization_url()
            webbrowser.open(auth_url)

            twitter_oauth_window = window_layout.make_twitteroauth_window(sg, window_title, png_icon_path)

            while True:
                twitter_oauth_event, twitter_oauth_values = twitter_oauth_window.read()

                if twitter_oauth_event == sg.WIN_CLOSED or twitter_oauth_event == '-AuthPIN_Button_Cancel-':
                    main_window.Element('-Auth_Button-').Update(disabled = False)
                    break

                if twitter_oauth_event == '-AuthPIN_Button_OK-':

                    try:
                        auth.get_access_token(twitter_oauth_values['-pin_code-'])

                    except Exception as error_result:
                        if '401' in str(error_result):
                            sg.popup_ok('有効なPINコードではありません\nもう一度お試しください', title = window_title, icon = png_icon_path, modal = True)
                        else:
                            sg.popup_ok('エラーが発生しました\nもう一度お試しください', title = window_title, icon = png_icon_path, modal = True)

                        main_window.Element('-Auth_Button-').Update(disabled = False)
                        break

                    auth.set_access_token(auth.access_token, auth.access_token_secret)

                    main_config['TwitterAPI']['access_token'] = auth.access_token
                    main_config['TwitterAPI']['access_token_secret'] = auth.access_token_secret

                    main_config['MainConfig']['OAuth2_sw'] = '1'
                    main_config['MainConfig']['portnumber'] = '10356'

                    with open('tweetron_data/ini/config.ini', 'w') as cw:
                        main_config.write(cw)

                    sg.popup_ok('認証が完了しました', title = window_title, icon = png_icon_path, modal = True)
                    twitter_oauth_sw = 1

                    main_window.close()
                    twitter_oauth_window.close()
                    break

            twitter_oauth_window.close()

        if twitter_oauth_sw == 1: break

    if twitter_oauth_sw == 0: main_window.close()

#-------------------------------------------------------------------------------

#make main window

#-------------------------------------------------------------------------------

if twitter_oauth_sw == 1:
    main_window = window_layout.make_setting_window(\
    sg, window_title, png_icon_path,
    preset_list, dt_now,
    time_h_list, time_m_list, time_s_list,
    menu_layout.main_menu(), search_word, nogood_word,
    **settingvalue_dict_all['main_setting'])

while True:
    main_event, main_values = main_window.read()

    if main_event == sg.WIN_CLOSED or '::app_exit::' in main_event: break

    #-------------------------------------------------------------------------------

    #make version window

    #-------------------------------------------------------------------------------

    if '::version_info::' in main_event:
        info_window = window_layout.make_info_window(sg, window_title, png_icon_path, software_version)

        while True:
            info_event, info_values = info_window.read()

            if info_event == sg.WIN_CLOSED or info_event == '-button_ok-': break

            if info_event == '-homepage_link-': webbrowser.open('https://github.com/Tweetron/')

        info_window.close()

    #-------------------------------------------------------------------------------

    #make global setting window

    #-------------------------------------------------------------------------------

    if '::global_setting::' in main_event:
        globalsetting_window = window_layout.make_globalsetting_window(sg, window_title, png_icon_path, port_number)

        while True:
            globalsetting_event, globalsetting_values = globalsetting_window.read()

            if globalsetting_event == sg.WIN_CLOSED or globalsetting_event == '-button_cancel-': break

            if globalsetting_event == '-button_ok-':

                if utility.isint(globalsetting_values['-portnumber_input-']) == True:
                    port_number = globalsetting_values['-portnumber_input-']

                    webscript_save.save_js_portnumber(str(port_number))

                    write_setting_config = configparser.RawConfigParser()
                    write_setting_config.read('tweetron_data/ini/config.ini')
                    write_setting_config.set('MainConfig', 'portnumber', str(port_number))

                    with open('tweetron_data/ini/config.ini', 'w') as file:
                        write_setting_config.write(file)

                    break

                else:
                    sg.popup_ok('無効な設定が含まれています', title = window_title, icon = png_icon_path)

        globalsetting_window.close()



    if main_event == '-preset_list_combo-':

        update_window_data = utility.update_setting_window(sg, os, configparser, datetime, tweetron_variable, main_window, window_title, png_icon_path, main_values['-preset_list_combo-'])

        search_word = update_window_data[0]
        nogood_word = update_window_data[1]
        settingvalue_dict_all = update_window_data[2]

        main_window['-preset_del-'].update(disabled = True) if main_values['-preset_list_combo-'] == '(新規名称未設定)' else main_window['-preset_del-'].update(disabled = False)



    if '::new_preset::' in main_event:

        new_preset_path = sg.popup_get_folder('new_preset', title = 'new_preset', no_window = True, modal = True)

        if new_preset_path != '':

            if os.path.exists(new_preset_path + '/search_word.txt') == False or os.path.exists(new_preset_path + '/nogood_word.txt') == False or os.path.exists(new_preset_path + '/config.ini') == False:
                sg.popup_ok('プリセットフォルダではありません', title = window_title, icon = png_icon_path, modal = True)

            else:
                if current_path.replace('\\', '/') + '/tweetron_data/preset' in new_preset_path:
                    sg.popup_ok('プリセットフォルダ内のプリセットは登録できません', title = window_title, icon = png_icon_path, modal = True)

                elif os.path.exists('tweetron_data/preset/' + os.path.basename(new_preset_path)) == True:
                    #すでに存在している場合はコピーできないので一旦削除する
                    shutil.rmtree('tweetron_data/preset/' + os.path.basename(new_preset_path))
                    shutil.copytree(new_preset_path, 'tweetron_data/preset/' + os.path.basename(new_preset_path))
                    sg.popup_ok('正常に上書き登録されました', title = window_title, icon = png_icon_path, modal = True)

                else:
                    shutil.copytree(new_preset_path, 'tweetron_data/preset/' + os.path.basename(new_preset_path))
                    sg.popup_ok('正常に登録されました', title = window_title, icon = png_icon_path, modal = True)

                #config.ini内のpreset_nameと統一
                read_config = configparser.RawConfigParser()
                read_config.read('tweetron_data/preset/' + os.path.basename(new_preset_path) + '/config.ini')

                if read_config.get('main_setting', 'preset_name') != os.path.basename(new_preset_path):
                    read_config.set('main_setting', 'preset_name', os.path.basename(new_preset_path))

                    with open('tweetron_data/preset/' + os.path.basename(new_preset_path) + '/config.ini', 'w') as file:
                        read_config.write(file)

                dir_files = os.listdir('tweetron_data/preset')
                preset_list = [f for f in dir_files if os.path.isdir(os.path.join('tweetron_data/preset', f))]
                preset_list.append('(新規名称未設定)')

                main_window['-preset_list_combo-'].update(value = preset_list[0], values = preset_list)

                if preset_list[0] == '(新規名称未設定)': main_window['-preset_del-'].update(disabled = True)

                update_window_data = utility.update_setting_window(sg, os, configparser, datetime, tweetron_variable, main_window, window_title, png_icon_path, preset_list[0])

                search_word = update_window_data[0]
                nogood_word = update_window_data[1]
                settingvalue_dict_all = update_window_data[2]



    if main_event == 'プリセット保存' or '::save_preset::' in main_event:

        if '新規名称未設定' in main_values['-preset_list_combo-'] and os.path.isdir('tweetron_data/preset/' + main_values['-preset_name-']):

            sg.popup_ok('このプリセットはすでに存在しています', title = window_title, icon = png_icon_path, modal = True)

        else:

            #検索ワードかプリセットの名前が指定されていなかった場合エラー処理
            if main_values['-search_word-'].replace('\n','') == '' or main_values['-preset_list_combo-'] == '' or '新規名称未設定' in main_values['-preset_list_combo-'] == True:

                error_message = ''

                if main_values['-preset_name-'] == '': error_message += 'プリセット名を設定してください\n'

                if '新規名称未設定' in main_values['-preset_name-']: error_message += '「新規名称未設定」 以外のプリセット名を設定してください\n'

                if main_values['-search_word-'].replace('\n','') == '': error_message += '検索ワードを設定してください'

                sg.popup_ok(error_message, title = window_title, icon = png_icon_path, modal = True)

            else:
                for key_name in settingvalue_dict_all['main_setting'].keys():
                    if key_name != 'since_rb':
                        if main_values['-' + key_name + '-'] == True or main_values['-' + key_name + '-'] == False:
                            settingvalue_dict_all['main_setting'][key_name] = int(main_values['-' + key_name + '-'])
                        else:
                            settingvalue_dict_all['main_setting'][key_name] = str(main_values['-' + key_name + '-'])

                search_word = str(main_values['-search_word-'])
                nogood_word = str(main_values['-nogood_word-'])

                if os.path.exists('tweetron_data/preset/' + main_values['-preset_list_combo-']) == False:
                    os.mkdir('tweetron_data/preset/' + main_values['-preset_name-'])
                else:
                    os.rename('tweetron_data/preset/' + main_values['-preset_list_combo-'],'tweetron_data/preset/' + main_values['-preset_name-'])

                settingvalue_dict_all['main_setting'][('since_rb')] = int(main_values['-rb_01-'])

                if settingvalue_dict_all['text_setting']['text_fontpath'] == '': settingvalue_dict_all['text_setting']['text_fontpath'] = 'null'

                if settingvalue_dict_all['filter_setting']['search_command'] == '': settingvalue_dict_all['filter_setting']['search_command'] = 'null'

                write_main_config = configparser.RawConfigParser()

                for key_p_key in settingvalue_dict_all.keys():
                    write_main_config.add_section(key_p_key)

                    for key_c_key in settingvalue_dict_all[key_p_key].keys():
                        write_main_config.set(key_p_key, key_c_key, settingvalue_dict_all[key_p_key][key_c_key])

                with open('tweetron_data/preset/' + main_values['-preset_name-'] + '/config.ini', 'w') as file:
                    write_main_config.write(file)

                with open('tweetron_data/preset/' + main_values['-preset_name-'] + '/search_word.txt', mode='w') as file:
                    file.write(search_word)

                with open('tweetron_data/preset/' + main_values['-preset_name-'] + '/nogood_word.txt', mode='w') as file:
                    file.write(nogood_word)

                sg.popup_ok('プリセットを保存しました', title = window_title, icon = png_icon_path, modal = True)

                dir_files = os.listdir('tweetron_data/preset')
                preset_list = [pfiles for pfiles in dir_files if os.path.isdir(os.path.join('tweetron_data/preset', pfiles))]
                preset_list.append('(新規名称未設定)')

                main_window['-preset_list_combo-'].update(value = settingvalue_dict_all['main_setting']['preset_name'], values = preset_list)
                main_window['-preset_del-'].update(disabled = True) if preset_list[0] == '(新規名称未設定)' else main_window['-preset_del-'].update(disabled = False)



    if main_event == '-preset_del-' or '::delete_preset::' in main_event:
        if main_values['-preset_list_combo-'] == '(新規名称未設定)':
            sg.popup_ok('有効なプリセットが選択されていません', title = window_title, icon = png_icon_path,modal = True)

        else:
            return_value = sg.popup_yes_no('このプリセットを削除しますか？', title = window_title, icon = png_icon_path, modal = True)

            if return_value == 'Yes':
                shutil.rmtree('tweetron_data/preset/' + main_values['-preset_list_combo-'])

                dir_files = os.listdir('tweetron_data/preset')
                preset_list = [f for f in dir_files if os.path.isdir(os.path.join('tweetron_data/preset', f))]
                preset_list.append('(新規名称未設定)')

                main_window['-preset_list_combo-'].update(value = preset_list[0], values = preset_list)

                if preset_list[0] == '(新規名称未設定)': main_window['-preset_del-'].update(disabled = True)

                update_window_data = utility.update_setting_window(sg, os, configparser, datetime, tweetron_variable, main_window, window_title, png_icon_path, preset_list[0])

                search_word = update_window_data[0]
                nogood_word = update_window_data[1]
                settingvalue_dict_all = update_window_data[2]



    if main_event == '-rb_01-':
        main_window['-calender_button-'].update(disabled = True)
        main_window['-add_nowtime-'].update(disabled = True)
        main_window['-searchdate_h-'].update(disabled = True)
        main_window['-searchdate_m-'].update(disabled = True)
        main_window['-searchdate_s-'].update(disabled = True)



    if main_event == '-rb_02-':
        main_window['-calender_button-'].update(disabled = False)
        main_window['-add_nowtime-'].update(disabled = False)
        main_window['-searchdate_h-'].update(disabled = False)
        main_window['-searchdate_m-'].update(disabled = False)
        main_window['-searchdate_s-'].update(disabled = False)



    if '::user_manual::' in main_event: webbrowser.open('https://github.com/Tweetron/Tweetron/wiki')



    if main_event == '-add_nowtime-':
        dt_now = datetime.datetime.now()
        main_window['-searchdate_h-'].update(value = dt_now.hour)
        main_window['-searchdate_m-'].update(value = dt_now.minute)
        main_window['-searchdate_s-'].update(value = dt_now.second)

    #-------------------------------------------------------------------------------

    #make filter setting window

    #-------------------------------------------------------------------------------

    if main_event == '-filter_setting-' or '::search_command::' in main_event:

        filterset_window = window_layout.make_filterset_window(sg, window_title, png_icon_path, **settingvalue_dict_all['filter_setting'])

        while True:
            filterset_event, filterset_values = filterset_window.read()

            if filterset_event == sg.WIN_CLOSED or filterset_event == 'Button_Cancel': break

            #Thanks yonoi blog (https://yonoi.com/)
            if filterset_event == '-command_list-': webbrowser.open('https://yonoi.com/twitter-search-command/')

            if filterset_event == 'Button_OK':
                settingvalue_dict_all['filter_setting']['search_command'] = filterset_values['-filter_input-']
                break

        filterset_window.close()

    #-------------------------------------------------------------------------------

    #make text setting window

    #-------------------------------------------------------------------------------

    if main_event == '-text_set-' or '::text_setting::' in main_event:

        textset_window = window_layout.make_textset_window(\
        sg, window_title, png_icon_path, fontsize_list, fonts_list, font_name,
        **settingvalue_dict_all['text_setting'])

        while True:
            textset_event, textset_values = textset_window.read()

            if textset_event == sg.WIN_CLOSED or textset_event == 'Button_Cancel':
                break

            if textset_event == '-sample_text_input-': textset_window['-sample_text-'].update(textset_values['-sample_text_input-'])

            if textset_event == '-fontsize_spin-': textset_window['-sample_text-'].update(font = [font_name,textset_values['-fontsize_spin-']])

            if textset_event == '-color_input-':
                color_code_text = textset_values['-color_input-']
                if len(color_code_text) > 7:
                    color_code_text = color_code_text[:-1]
                try:
                    #color_code_text = textset_values['-color_input-']
                    textset_window['-sample_text-'].update(text_color = color_code_text)
                except:
                    #color_code_text = textset_values['-color_input-']
                    if len(color_code_text) == 0 or color_code_text[0] != '#':
                        color_code_text = '#'

                textset_window['-color_input-'].update(value = color_code_text)

            if textset_event == '-font_list-':
                font_name = textset_values['-font_list-'][0]
                textset_window['-sample_text-'].update(font = [font_name,textset_values['-fontsize_spin-']])
                textset_window['-font_name_input-'].update(value = font_name)

            if textset_event == '-font_name_input-':
                textset_window['-sample_text-'].update(font = [textset_values['-font_name_input-'],textset_values['-fontsize_spin-']])

            if textset_event == '-font_path-':
                textset_window['-font_path-'].update(text_color = '#4169e1') if os.path.exists(textset_values['-font_path-']) == True else textset_window['-font_path-'].update(text_color = '#ff0000')

            if textset_event == '-Verification-':
                if len(textset_values['-color_input-']) == 7:

                    if textset_values['-font_path-'] != '' and os.path.exists(textset_values['-font_path-']) and (textset_values['-font_path-'][-3:] == 'ttf' or textset_values['-font_path-'][-3:] == 'TTF'):
                        webscript_save.save_test_css(textset_values['-font_name_input-'], textset_values['-color_input-'], textset_values['-fontsize_spin-'], textset_values['-font_path-'])
                    else:
                        webscript_save.save_test_css(textset_values['-font_name_input-'], textset_values['-color_input-'], textset_values['-fontsize_spin-'])

                    webscript_save.save_test_html(textset_values['-sample_text_input-'])

                    time.sleep(0.5)
                    subprocess.Popen(['start', 'tweetron_data/verification/verification_html.html'], shell = True)

                else:

                    sg.popup_ok('カラーコードを指定してください', title = window_title, icon = png_icon_path, modal = True)

            if textset_event == '-init-':
                return_value = sg.popup_yes_no('設定を初期化しますか？', title = window_title, icon = png_icon_path, modal = True)

                if return_value == 'Yes':
                    textset_window['-sample_text-'].update('Sampleテキスト', font = ['Meiryo UI',25], text_color = '#000000')
                    textset_window['-sample_text_input-'].update(value = 'Sampleテキスト')
                    textset_window['-fontsize_spin-'].update(value = 25)
                    textset_window['-color_input-'].update(value = '#000000')
                    textset_window['-font_name_input-'].update(value = 'Meiryo UI')
                    textset_window['-font_path-'].update(value = '')

            if textset_event == 'Button_OK':

                if os.path.exists(textset_values['-font_path-']) == False and textset_values['-font_path-'] != '':
                    sg.popup_ok('指定したttfファイルが存在しません', title = window_title, icon = png_icon_path, modal = True)

                else:
                    settingvalue_dict_all['text_setting']['text_fontsize'] = int(textset_values['-fontsize_spin-'])
                    settingvalue_dict_all['text_setting']['text_color'] = textset_values['-color_input-']
                    settingvalue_dict_all['text_setting']['text_fontname'] = textset_values['-font_name_input-']
                    settingvalue_dict_all['text_setting']['text_fontpath']= textset_values['-font_path-']

                    break

        textset_window.close()

    #-------------------------------------------------------------------------------

    #make textdisplay setting window

    #-------------------------------------------------------------------------------

    if main_event == '-display_set-' or '::text_display::' in main_event:

        displayset_window = window_layout.make_displayset_window(\
        sg, window_title, png_icon_path,
        text_scrollspeed_list, template_list,
        **settingvalue_dict_all['display_setting'])

        while True:
            displayset_event, displayset_values = displayset_window.read()

            if displayset_event == sg.WIN_CLOSED or displayset_event == 'Button_Cancel': break

            if displayset_event == '-verification-':
                webscript_save.save_js_data(\
                str(displayset_values['-scrollspeed_spin-']), str(displayset_values['-displaydelay_input-']),
                str(displayset_values['-fadeinspeed_input-']), str(displayset_values['-fadeoutspeed_input-']),
                str(displayset_values['-startdelay_input-']), 0)

                time.sleep(0.5)
                subprocess.Popen(['start', 'tweetron_data/verification/verification_js.html'], shell = True)

            if displayset_event == '-setting_init-':
                return_value = sg.popup_yes_no('設定を初期化しますか？', title = window_title, icon = png_icon_path, modal = True)

                if return_value == 'Yes':
                    displayset_window['-rb_01-'].update(value = True)
                    displayset_window['-scrollspeed_spin-'].update(value = 80)
                    displayset_window['-displaydelay_input-'].update(value = '3')
                    displayset_window['-startdelay_input-'].update(value = '2')
                    displayset_window['-fadeinspeed_input-'].update(value = '2')
                    displayset_window['-fadeoutspeed_input-'].update(value = '2')
                    displayset_window['-loadloop_check-'].update(value = True)

            if displayset_event == 'Button_OK':
                if displayset_values['-rb_01-'] == True:
                    settingvalue_dict_all['display_setting']['text_displaytype'] = 1
                else:
                    settingvalue_dict_all['display_setting']['text_displaytype'] = 2

                if utility.isint(displayset_values['-scrollspeed_spin-']) == False or\
                   utility.isint(displayset_values['-displaydelay_input-']) == False or\
                   utility.isint(displayset_values['-fadeinspeed_input-']) == False or\
                   utility.isint(displayset_values['-fadeoutspeed_input-']) == False or\
                   utility.isint(displayset_values['-startdelay_input-']) == False:

                    sg.popup_ok('一部数値が無効です', title = window_title, icon = png_icon_path, modal = True)

                else:
                    settingvalue_dict_all['display_setting']['text_scrollspeed']  = int(displayset_values['-scrollspeed_spin-'])
                    settingvalue_dict_all['display_setting']['text_displaydelay'] = int(displayset_values['-displaydelay_input-'])
                    settingvalue_dict_all['display_setting']['text_fadeinspeed'] = int(displayset_values['-fadeinspeed_input-'])
                    settingvalue_dict_all['display_setting']['text_fadeoutspeed'] = int(displayset_values['-fadeoutspeed_input-'])
                    settingvalue_dict_all['display_setting']['text_startdelay'] = int(displayset_values['-startdelay_input-'])
                    settingvalue_dict_all['display_setting']['text_loadloop'] = int(displayset_values['-loadloop_check-'])
                    break

        displayset_window.close()

    #-------------------------------------------------------------------------------

    #start tweetron core

    #-------------------------------------------------------------------------------

    if main_event == '実行':

        if search_word.replace('\n','') == '' or settingvalue_dict_all['main_setting']['preset_name'] == '' or main_values['-preset_list_combo-'] == '(新規名称未設定)':

            error_message = ''

            if main_values['-preset_list_combo-'] == '(新規名称未設定)':
                error_message += '一度プリセットを保存してください'

            else:
                if main_values['-preset_name-'] == '': error_message += 'プリセット名を設定してください\n'

                if main_values['-search_word-'].replace('\n','') == '': error_message += '検索ワードを設定してください'

            sg.popup_ok(error_message, title = window_title, icon = png_icon_path, modal = True)

        else:

            if settingvalue_dict_all['text_setting']['text_fontpath'] != '' and settingvalue_dict_all['text_setting']['text_fontpath'] != 'null':
                webscript_save.save_css(settingvalue_dict_all['text_setting']['text_fontname'], settingvalue_dict_all['text_setting']['text_color'], settingvalue_dict_all['text_setting']['text_fontsize'], settingvalue_dict_all['text_setting']['text_fontpath'])
            else:
                webscript_save.save_css(settingvalue_dict_all['text_setting']['text_fontname'], settingvalue_dict_all['text_setting']['text_color'], settingvalue_dict_all['text_setting']['text_fontsize'])

            webscript_save.save_js_data(\
            str(settingvalue_dict_all['display_setting']['text_scrollspeed']), str(settingvalue_dict_all['display_setting']['text_displaydelay']),
            str(settingvalue_dict_all['display_setting']['text_fadeinspeed']), str(settingvalue_dict_all['display_setting']['text_fadeoutspeed']),
            str(settingvalue_dict_all['display_setting']['text_startdelay']), 1)

            if settingvalue_dict_all['display_setting']['text_displaytype'] == 1:
                shutil.copy('./tweetron_data/html/type_01.html','Tweetron.html')
            elif settingvalue_dict_all['display_setting']['text_displaytype'] == 2:
                shutil.copy('./tweetron_data/html/type_02.html','Tweetron.html')

            for proc in psutil.process_iter():
                if proc.name() == 'Tweetron_Core.exe': proc.kill()

            subprocess.Popen('start tweetron_data/Tweetron_Core.exe --preset_name ' + settingvalue_dict_all['main_setting']['preset_name'] + ' --debug_mode 0', shell = True)



main_window.close()
sys.exit()
