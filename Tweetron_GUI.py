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

#ライブラリインポート
import PySimpleGUI as sg
import tweepy
import webbrowser
import configparser
import random
from websocket_server import WebsocketServer
import time
import os
import datetime
from tkinter import font
import tkinter
import sys
import subprocess
from pygame import mixer
import shutil
import json

from tweetron_library import webscript_save

import api_key
import software_info

import window_layout

software_version = software_info.VERSION()
window_title = 'Tweetron ' + software_version

png_icon_path = 'data/img/icon.ico'
font_name = 'Meiryo UI'

time_h_list = []
time_m_list = []
time_s_list = []
fontsize_list = []
streamtext_scrollspeed_list = []

for num in range(25):
    time_h_list.append(num)
for num in range(61):
    time_m_list.append(num)
    time_s_list.append(num)
for num in range(61):
    fontsize_list.append(num)
for num in range(101):
    streamtext_scrollspeed_list.append(num)

def isint(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True

def dialogwindow(text):
    sg.popup_ok(text, title = window_title, icon = png_icon_path)

dt_now = datetime.datetime.now()

#コンフィグ読み込み
main_config = configparser.ConfigParser()
main_config.read('data/ini/config.ini', encoding='utf-8')

#OAuth認証済みかどうか
twitter_oauth_sw = int(main_config.get('MainConfig', 'oauth2_sw'))

#APIキー取得
consumer_key = api_key.CONSUMER_KEY()
consumer_secret = api_key.CONSUMER_SECRET()
callback_url = 'oob'

#フォントリスト取得
root = tkinter.Tk()
fonts_list = list(font.families())
fonts_list.sort()
root.destroy()

#プリセットリスト取得
dir_files = os.listdir('data/preset')
preset_list = [f for f in dir_files if os.path.isdir(os.path.join('data/preset', f))]
preset_list.append('(新規名称未設定)')

#テーマ作成
sg.LOOK_AND_FEEL_TABLE['White'] = {
	'BACKGROUND': '#ffffff',
	'TEXT': 'black',
	'INPUT': '#eeeeee',
	'SCROLL': '#4169e1',
	'TEXT_INPUT': 'black',
	'BUTTON': ('white', '#4169e1'),
	'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
	'BORDER': 0,
	'SLIDER_DEPTH': 0,
	'PROGRESS_DEPTH': 0
}

sg.LOOK_AND_FEEL_TABLE['Dark'] = {
	'BACKGROUND': '#000000',
	'TEXT': 'white',
	'INPUT': '#1e1e1e',
	'SCROLL': '#1e1e1e',
	'TEXT_INPUT': 'white',
	'BUTTON': ('white', '#1e1e1e'),
	'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
	'BORDER': 0,
	'SLIDER_DEPTH': 0,
	'PROGRESS_DEPTH': 0
}

sg.theme('White')

preset_name = ''
search_word = ''
nogood_word = ''
since_rb = 0
reply_exclusion = 0
specity_date = dt_now.strftime("%Y-%m-%d")
specity_h = time_h_list[0]
specity_m = time_m_list[0]
specity_s = time_s_list[0]

streamtext_font_size = 25
streamtext_color = '#000000'
streamtext_font_name = 'Meiryo UI'
streamtext_font_path = ''

streamtext_displaytype = 1
streamtext_scrollspeed = 80
streamtext_displaydelay = 5
streamtext_fadeinspeed = 3
streamtext_fadeoutspeed = 3
streamtext_startdelay = 3

template_list = ['未実装']

search_command = ''

#設定ウィンドウ [ make_setting_window() ] のアップデート
def update_setting_window(preset_name_combo):

    global preset_name
    global search_word
    global nogood_word
    global since_rb
    global reply_exclusion
    global specity_date
    global specity_h
    global specity_m
    global specity_s

    global streamtext_font_size
    global streamtext_color
    global streamtext_font_name
    global streamtext_font_path

    global streamtext_scrollspeed
    global streamtext_displaydelay
    global streamtext_fadeinspeed
    global streamtext_fadeoutspeed
    global streamtext_startdelay

    dt_now = datetime.datetime.now()

    if preset_name_combo == '(新規名称未設定)':

        preset_name = ''
        search_word = ''
        nogood_word = ''
        since_rb = 0
        reply_exclusion = 0
        specity_date = dt_now.strftime("%Y-%m-%d")
        specity_h = time_h_list[0]
        specity_m = time_m_list[0]
        specity_s = time_s_list[0]

        streamtext_font_size = 25
        streamtext_color = '#000000'
        streamtext_font_name = 'Meiryo UI'
        streamtext_font_path = ''

        streamtext_displaytype = 1
        streamtext_scrollspeed = 80
        streamtext_displaydelay = 5
        streamtext_fadeinspeed = 3
        streamtext_fadeoutspeed = 3
        streamtext_startdelay = 3

        search_command = ''

        main_window['-calender_button-'].update(disabled = since_rb)
        main_window['-spin_h-'].update(disabled = since_rb)
        main_window['-spin_m-'].update(disabled = since_rb)
        main_window['-spin_s-'].update(disabled = since_rb)

        main_window['-preset_name-'].update(value = preset_name)
        main_window['-search_word-'].update(value = search_word)
        main_window['-nogood_word-'].update(value = nogood_word)
        main_window['-reply_exclusion-'].update(value = reply_exclusion)
        main_window['-calender_input-'].update(value = specity_date)
        main_window['-spin_h-'].update(value = specity_h)
        main_window['-spin_m-'].update(value = specity_m)
        main_window['-spin_s-'].update(value = specity_s)

    else:

        read_main_config = configparser.RawConfigParser()

        read_main_config.read('data/preset/' + preset_name_combo  + '/config.ini')

        preset_name = str(read_main_config.get('main_setting', 'preset_name'))
        since_rb = int(read_main_config.get('main_setting', 'since_rb'))
        reply_exclusion = int(read_main_config.get('main_setting', 'reply_exclusion'))
        specity_date = str(read_main_config.get('main_setting', 'specity_date'))
        specity_h = int(read_main_config.get('main_setting', 'specity_h'))
        specity_m = int(read_main_config.get('main_setting', 'specity_m'))
        specity_s = int(read_main_config.get('main_setting', 'specity_s'))

        search_command = str(read_main_config.get('filter_setting', 'search_command'))

        streamtext_font_size = int(read_main_config.get('text_setting', 'streamtext_font_size'))
        streamtext_color = str(read_main_config.get('text_setting', 'streamtext_color'))
        streamtext_font_name = str(read_main_config.get('text_setting', 'streamtext_font_name'))
        streamtext_font_path = str(read_main_config.get('text_setting', 'streamtext_font_path'))
        streamtext_displaytype = int(read_main_config.get('textdisplay_setting', 'streamtext_displaytype'))
        streamtext_scrollspeed = int(read_main_config.get('textdisplay_setting', 'streamtext_scrollspeed'))
        streamtext_displaydelay = int(read_main_config.get('textdisplay_setting', 'streamtext_displaydelay'))
        streamtext_fadeinspeed = int(read_main_config.get('textdisplay_setting', 'streamtext_fadeinspeed'))
        streamtext_fadeoutspeed = int(read_main_config.get('textdisplay_setting', 'streamtext_fadeoutspeed'))
        streamtext_startdelay = int(read_main_config.get('textdisplay_setting', 'streamtext_startdelay'))

        with open('data/preset/' + preset_name_combo  + '/search_word.txt') as file:
            search_word = file.read()

        with open('data/preset/' + preset_name_combo  + '/nogood_word.txt') as file:
            nogood_word = file.read()

        if since_rb == 1:
            main_window['-rb_01-'].update(value = True)
            main_window['-rb_02-'].update(value = False)
            main_window['-calender_button-'].update(disabled = True)
            main_window['-spin_h-'].update(disabled = True)
            main_window['-spin_m-'].update(disabled = True)
            main_window['-spin_s-'].update(disabled = True)
        else:
            main_window['-rb_01-'].update(value = False)
            main_window['-rb_02-'].update(value = True)
            main_window['-calender_button-'].update(disabled = False)
            main_window['-spin_h-'].update(disabled = False)
            main_window['-spin_m-'].update(disabled = False)
            main_window['-spin_s-'].update(disabled = False)

        main_window['-preset_name-'].update(value = preset_name)
        main_window['-search_word-'].update(value = search_word)
        main_window['-nogood_word-'].update(value = nogood_word)
        main_window['-reply_exclusion-'].update(value = reply_exclusion)
        main_window['-calender_input-'].update(value = specity_date)
        main_window['-spin_h-'].update(value = specity_h)
        main_window['-spin_m-'].update(value = specity_m)
        main_window['-spin_s-'].update(value = specity_s)

if twitter_oauth_sw == 0:

    main_window = window_layout.make_welcome_window(sg, window_title, png_icon_path)

    while True:
        main_event, main_values = main_window.read()

        if main_event == sg.WIN_CLOSED:
            break

        #認証ボタン
        if main_event == '-wikipage_open-':
            webbrowser.open('https://github.com/CubeZeero/Tweetron/wiki')

        #認証ボタン
        if main_event == '-Auth_Button-':

            main_window.Element('-Auth_Button-').Update(disabled = True)

            #認証URL作成
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
            auth_url = auth.get_authorization_url()

            webbrowser.open(auth_url)

            #PINコード入力ウィンドウ作成
            twitter_oauth_window = window_layout.make_twitteroauth_window(sg, window_title, png_icon_path)

            while True:
                twitter_oauth_event, twitter_oauth_values = twitter_oauth_window.read()

                if twitter_oauth_event == sg.WIN_CLOSED or twitter_oauth_event == '-AuthPIN_Button_Cancel-':
                    main_window.Element('-Auth_Button-').Update(disabled = False)
                    break

                if twitter_oauth_event == '-AuthPIN_Button_OK-':

                    #入力されたPINコードを使用して認証
                    try:
                        auth.get_access_token(twitter_oauth_values['-pin_code-'])

                    except Exception as error_result:
                        if '401' in str(error_result):
                            dialogwindow('有効なPINコードではありません\nもう一度お試しください')
                        else:
                            dialogwindow('エラーが発生しました\nもう一度お試しください')

                        main_window.Element('-Auth_Button-').Update(disabled = False)
                        break

                    print(auth.get_access_token)
                    auth.set_access_token(auth.access_token, auth.access_token_secret)

                    #メインコンフィグ書き込み
                    main_config['TwitterAPI'] = {
                        'access_token': auth.access_token,
                        'access_token_secret': auth.access_token_secret
                    }

                    main_config['MainConfig'] = {
                        'OAuth2_sw': 1
                    }

                    with open('data/ini/config.ini', 'w') as cw:
                        main_config.write(cw)

                    dialogwindow('認証が完了しました')
                    twitter_oauth_sw = 1

                    main_window.close()
                    twitter_oauth_window.close()
                    break

            twitter_oauth_window.close()

        if twitter_oauth_sw == 1:
            break

    if twitter_oauth_sw == 0:
        main_window.close()

if twitter_oauth_sw == 1:
    main_window = window_layout.make_setting_window(\
    sg, window_title, png_icon_path,
    preset_name, search_word, nogood_word,
    since_rb, reply_exclusion,
    specity_h, specity_m, specity_s,
    specity_date, preset_list, dt_now,
    time_h_list, time_m_list, time_s_list)

while True:
    main_event, main_values = main_window.read()

    if main_event == sg.WIN_CLOSED:
        break

    #設定画面のアップデート
    #プリセットの変更時に作動
    if main_event == '-preset_list_combo-':

        update_setting_window(main_values['-preset_list_combo-'])

        if main_values['-preset_list_combo-'] == '(新規名称未設定)':
            main_window['-preset_del-'].update(disabled = True)
        else:
            main_window['-preset_del-'].update(disabled = False)

    #プリセット保存
    if main_event == 'プリセット保存':

        preset_name = str(main_values['-preset_name-'])

        search_word = str(main_values['-search_word-'])
        nogood_word = str(main_values['-nogood_word-'])

        reply_exclusion = int(main_values['-reply_exclusion-'])
        specity_date = str(main_values['-calender_input-'])
        specity_h = int(main_values['-spin_h-'])
        specity_m = int(main_values['-spin_m-'])
        specity_s = int(main_values['-spin_s-'])

        #検索ワードかプリセットの名前が指定されていなかった場合エラー処理
        if search_word.replace('\n','') == '' or preset_name == '':

            error_message = ''

            if main_values['-preset_name-'] == '':
                error_message += 'プリセット名を設定してください\n'

            if main_values['-search_word-'].replace('\n','') == '':
                error_message += '検索ワードを設定してください'

            dialogwindow(error_message)

        else:

            #プリセットのフォルダが存在しなかった場合新規作成と見なす
            if os.path.exists('data/preset/' + main_values['-preset_list_combo-']) == False:
                os.mkdir('data/preset/' + main_values['-preset_name-'])
            else:
                os.rename('data/preset/' + main_values['-preset_list_combo-'],'data/preset/' + main_values['-preset_name-'])

            if int(main_values['-rb_01-']) == 1:
                since_rb = 1
            else:
                since_rb = 0

            if streamtext_font_path == '':
                streamtext_font_path = 'null'

            if search_command == '':
                search_command = 'null'

            #コンフィグファイルへの書き込み
            write_main_config = configparser.RawConfigParser()

            write_main_config.add_section('main_setting')
            write_main_config.set('main_setting', 'preset_name', preset_name)
            write_main_config.set('main_setting', 'since_rb', since_rb)
            write_main_config.set('main_setting', 'reply_exclusion', reply_exclusion)
            write_main_config.set('main_setting', 'specity_date', specity_date)
            write_main_config.set('main_setting', 'specity_h', specity_h)
            write_main_config.set('main_setting', 'specity_m', specity_m)
            write_main_config.set('main_setting', 'specity_s', specity_s)

            write_main_config.add_section('filter_setting')
            write_main_config.set('filter_setting', 'search_command', search_command)

            write_main_config.add_section('text_setting')
            write_main_config.set('text_setting', 'streamtext_font_size', streamtext_font_size)
            write_main_config.set('text_setting', 'streamtext_color', streamtext_color)
            write_main_config.set('text_setting', 'streamtext_font_name', streamtext_font_name)
            write_main_config.set('text_setting', 'streamtext_font_path', streamtext_font_path)

            write_main_config.add_section('textdisplay_setting')
            write_main_config.set('textdisplay_setting', 'streamtext_displaytype', streamtext_displaytype)
            write_main_config.set('textdisplay_setting', 'streamtext_scrollspeed', streamtext_scrollspeed)
            write_main_config.set('textdisplay_setting', 'streamtext_displaydelay', streamtext_displaydelay)
            write_main_config.set('textdisplay_setting', 'streamtext_fadeinspeed', streamtext_fadeinspeed)
            write_main_config.set('textdisplay_setting', 'streamtext_fadeoutspeed', streamtext_fadeoutspeed)
            write_main_config.set('textdisplay_setting', 'streamtext_startdelay', streamtext_startdelay)

            with open('data/preset/' + main_values['-preset_name-'] + '/config.ini', 'w') as file:
                write_main_config.write(file)

            with open('data/preset/' + main_values['-preset_name-'] + '/search_word.txt', mode='w') as file:
                file.write(search_word)

            with open('data/preset/' + main_values['-preset_name-'] + '/nogood_word.txt', mode='w') as file:
                file.write(nogood_word)

            dialogwindow('プリセットを保存しました')

            #プリセットリストを再度読み込み
            dir_files = os.listdir('data/preset')
            preset_list = [f for f in dir_files if os.path.isdir(os.path.join('data/preset', f))]
            preset_list.append('(新規名称未設定)')

            main_window['-preset_list_combo-'].update(value = preset_name, values = preset_list)

    #プリセット削除
    if main_event == '-preset_del-':

        return_value = sg.popup_yes_no('このプリセットを削除しますか？', title = window_title, icon = png_icon_path)

        if return_value == 'Yes':

            #フォルダ削除
            shutil.rmtree('data/preset/' + main_values['-preset_list_combo-'])

            dir_files = os.listdir('data/preset')
            preset_list = [f for f in dir_files if os.path.isdir(os.path.join('data/preset', f))]
            preset_list.append('(新規名称未設定)')

            main_window['-preset_list_combo-'].update(value = preset_list[0], values = preset_list)

            if preset_list[0] == '(新規名称未設定)':
                main_window['-preset_del-'].update(disabled = True)

            update_setting_window(preset_list[0])

    #日付設定類の有効化無効化
    if main_event == '-rb_01-':
        main_window['-calender_button-'].update(disabled = True)
        main_window['-add_nowtime-'].update(disabled = True)
        main_window['-spin_h-'].update(disabled = True)
        main_window['-spin_m-'].update(disabled = True)
        main_window['-spin_s-'].update(disabled = True)

    if main_event == '-rb_02-':
        main_window['-calender_button-'].update(disabled = False)
        main_window['-add_nowtime-'].update(disabled = False)
        main_window['-spin_h-'].update(disabled = False)
        main_window['-spin_m-'].update(disabled = False)
        main_window['-spin_s-'].update(disabled = False)

    #wikiページを開く
    if main_event == '-wikipage_open-':
        webbrowser.open('https://github.com/CubeZeero/Tweetron/wiki')

    if main_event == '-add_nowtime-':
        dt_now = datetime.datetime.now()
        main_window['-spin_h-'].update(value = dt_now.hour)
        main_window['-spin_m-'].update(value = dt_now.minute)
        main_window['-spin_s-'].update(value = dt_now.second)

    #検索フィルタ設定
    if main_event == '-filter_setting-':

        filterset_window = window_layout.make_filterset_window(sg, window_title, png_icon_path, search_command)

        while True:
            filterset_event, filterset_values = filterset_window.read()

            if filterset_event == sg.WIN_CLOSED or filterset_event == 'Button_Cancel':
                break

            if filterset_event == '-command_list-':
                #Thanks yonoi blog (https://yonoi.com/)
                webbrowser.open('https://yonoi.com/twitter-search-command/')

            if filterset_event == 'Button_OK':
                search_command = filterset_values['-filter_input-']
                break

        filterset_window.close()

    #テキスト表示設定
    if main_event == '-text_set-':

        textset_window = window_layout.make_textset_window(\
        sg, window_title, png_icon_path,
        streamtext_font_size, streamtext_color, streamtext_font_name,
        streamtext_font_path, fonts_list, font_name,
        fontsize_list)

        #textset_window['-sample_text-'].expand(expand_x = True, expand_y = True, expand_row = True)

        while True:
            textset_event, textset_values = textset_window.read()

            if textset_event == sg.WIN_CLOSED or textset_event == 'Button_Cancel':
                break
            #サンプルテキストのアップデート
            if textset_event == '-sample_text_input-':
                textset_window['-sample_text-'].update(textset_values['-sample_text_input-'])

            #フォントサイズのアップデート
            if textset_event == '-fontsize_spin-':
                textset_window['-sample_text-'].update(font = [font_name,textset_values['-fontsize_spin-']])

            #テキストカラーのアップデート
            if textset_event == '-color_input-':
                try:
                    color_code_text = textset_values['-color_input-']
                    textset_window['-sample_text-'].update(text_color = color_code_text)
                except:
                    color_code_text = textset_values['-color_input-']
                    #カラーコードが無記入か"#"から始まっていなかった場合
                    #強制的に#から記入を始める
                    if len(color_code_text) == 0 or color_code_text[0] != '#':
                        color_code_text = '#'
                    textset_window['-color_input-'].update(value = color_code_text)

            #フォントのアップデート
            #フォントリストから選択されたフォントを適用
            if textset_event == '-font_list-':
                font_name = textset_values['-font_list-'][0]
                textset_window['-sample_text-'].update(font = [font_name,textset_values['-fontsize_spin-']])
                textset_window['-font_name_input-'].update(value = font_name)

            #フォントのアップデート
            #フォントの名前を直接指定して適用
            if textset_event == '-font_name_input-':
                textset_window['-sample_text-'].update(font = [textset_values['-font_name_input-'],textset_values['-fontsize_spin-']])

            #ttfのフォントファイルの有無
            #存在しない場合赤文字で警告
            if textset_event == '-font_path-':
                if os.path.exists(textset_values['-font_path-']) == True:
                    textset_window['-font_path-'].update(text_color = '#000000')
                else:
                    textset_window['-font_path-'].update(text_color = '#ff0000')

            #htmlで実際に確認
            if textset_event == '-Verification-':
                if len(textset_values['-color_input-']) == 7:

                    #フォントファイルが存在する場合そのフォントを優先して適用
                    if textset_values['-font_path-'] != '' and os.path.exists(textset_values['-font_path-']) == True and textset_values['-font_path-'][-3:] == 'ttf':
                        webscript_save.save_test_css(textset_values['-font_name_input-'], textset_values['-color_input-'], textset_values['-fontsize_spin-'], textset_values['-font_path-'])
                    else:
                        webscript_save.save_test_css(textset_values['-font_name_input-'], textset_values['-color_input-'], textset_values['-fontsize_spin-'])

                    #設定されているサンプルテキストを適用したhtmlファイルを作成
                    webscript_save.save_test_html(textset_values['-sample_text_input-'])

                    time.sleep(0.5)
                    subprocess.Popen(['start', 'data/verification/verification_html.html'], shell = True)

                else:

                    dialogwindow('カラーコードを指定してください')

            if textset_event == 'Button_OK':

                if os.path.exists(textset_values['-font_path-']) == False and textset_values['-font_path-'] != '':
                    dialogwindow('指定したttfファイルが存在しません')
                else:
                    streamtext_font_size = int(textset_values['-fontsize_spin-'])
                    streamtext_color = textset_values['-color_input-']
                    streamtext_font_name = textset_values['-font_name_input-']
                    streamtext_font_path = textset_values['-font_path-']

                    break

        textset_window.close()

    #テキスト表示設定
    if main_event == '-display_set-':

        displayset_window = window_layout.make_displayset_window(\
        sg, window_title, png_icon_path,
        streamtext_displaytype, streamtext_scrollspeed_list,
        streamtext_scrollspeed, streamtext_displaydelay,
        streamtext_fadeinspeed, streamtext_fadeoutspeed,
        streamtext_startdelay, template_list)

        while True:
            displayset_event, displayset_values = displayset_window.read()

            if displayset_event == sg.WIN_CLOSED or displayset_event == 'Button_Cancel':
                break

            if displayset_event == '-verification-':
                webscript_save.save_js_data(\
                str(displayset_values['-scrollspeed_spin-']), str(displayset_values['-displaydelay_input-']),
                str(displayset_values['-fadeinspeed_input-']), str(displayset_values['-fadeoutspeed_input-']),
                str(displayset_values['-startdelay_input-']), 0)

                time.sleep(0.5)
                subprocess.Popen(['start', 'data/verification/verification_js.html'], shell = True)

            if displayset_event == '-setting_init-':
                return_value = sg.popup_yes_no('設定を初期化しますか？', title = window_title, icon = png_icon_path)

                if return_value == 'Yes':
                    displayset_window['-rb_01-'].update(value = True)
                    displayset_window['-scrollspeed_spin-'].update(value = 80)
                    displayset_window['-displaydelay_input-'].update(value = '5')
                    displayset_window['-startdelay_input-'].update(value = '3')
                    displayset_window['-fadeinspeed_input-'].update(value = '3')
                    displayset_window['-fadeoutspeed_input-'].update(value = '3')

            if displayset_event == 'Button_OK':
                if displayset_values['-rb_01-'] == True:
                    streamtext_displaytype = 1
                else:
                    streamtext_displaytype = 2

                if isint(displayset_values['-scrollspeed_spin-']) == False or\
                   isint(displayset_values['-displaydelay_input-']) == False or\
                   isint(displayset_values['-fadeinspeed_input-']) == False or\
                   isint(displayset_values['-fadeoutspeed_input-']) == False or\
                   isint(displayset_values['-startdelay_input-']) == False:

                    dialogwindow('一部数値が無効です')

                else:

                    streamtext_scrollspeed = int(displayset_values['-scrollspeed_spin-'])
                    streamtext_displaydelay = int(displayset_values['-displaydelay_input-'])
                    streamtext_fadeinspeed = int(displayset_values['-fadeinspeed_input-'])
                    streamtext_fadeoutspeed = int(displayset_values['-fadeoutspeed_input-'])
                    streamtext_startdelay = int(displayset_values['-startdelay_input-'])
                    break

        displayset_window.close()

    #プリセット実行
    if main_event == '実行':

        if search_word.replace('\n','') == '' or preset_name == '' or main_values['-preset_list_combo-'] == '(新規名称未設定)':

            error_message = ''

            if main_values['-preset_list_combo-'] == '(新規名称未設定)':
                error_message += '一度プリセットを保存してください'

            else:

                if main_values['-preset_name-'] == '':
                    error_message += 'プリセット名を設定してください\n'

                if main_values['-search_word-'].replace('\n','') == '':
                    error_message += '検索ワードを設定してください'

            dialogwindow(error_message)

        else:

            #実際に使用するcssを作成
            if streamtext_font_path != '' and streamtext_font_path != 'null':
                webscript_save.save_css(streamtext_font_name, streamtext_color, streamtext_font_size, streamtext_font_path)
            else:
                webscript_save.save_css(streamtext_font_name, streamtext_color, streamtext_font_size)

            webscript_save.save_js_data(\
            str(streamtext_scrollspeed), str(streamtext_displaydelay),
            str(streamtext_fadeinspeed), str(streamtext_fadeoutspeed),
            str(streamtext_startdelay), 1)

            #テキスト表示設定をもとに2つのタイプから選択
            if streamtext_displaytype == 1:
                shutil.copy('./data/html/type_01.html','Tweetron.html')
            else:
                shutil.copy('./data/html/type_02.html','Tweetron.html')

            os.system("taskkill /f /im Tweetron_Core.exe")
            subprocess.Popen(['start', 'data/Tweetron_Core.exe', preset_name], shell = True)

main_window.close()
sys.exit()
