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

from tweetron_library import htmlcss_save

import api_key
import software_info
software_version = software_info.VERSION()

#フォントリスト取得
root = tkinter.Tk()
fonts_list = list(font.families())
fonts_list.sort()
root.destroy()

png_icon_path = 'data/img/icon.ico'

#コンフィグ読み込み
main_config = configparser.ConfigParser()
main_config.read('data/ini/config.ini', encoding='utf-8')

#OAuth認証済みかどうか
twitter_oauth_sw = int(main_config.get('MainConfig', 'oauth2_sw'))

font_name = 'Meiryo UI'

window_title = 'Tweetron ' + software_version

#APIキー取得
consumer_key = api_key.CONSUMER_KEY()
consumer_secret = api_key.CONSUMER_SECRET()
callback_url = 'oob'

#プリセットリスト取得
dir_files = os.listdir('data/preset')
preset_list = [f for f in dir_files if os.path.isdir(os.path.join('data/preset', f))]
preset_list.append('(新規名称未設定)')

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

dt_now = datetime.datetime.now()

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
	'BACKGROUND': '#2d2d2d',
	'TEXT': 'white',
	'INPUT': '#DDE0DE',
	'SCROLL': '#4169e1',
	'TEXT_INPUT': 'black',
	'BUTTON': ('white', '#4169e1'),
	'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
	'BORDER': 0,
	'SLIDER_DEPTH': 0,
	'PROGRESS_DEPTH': 0
}

sg.theme('White')

preset_name = ''
search_word = ''
nogood_word = ''
since_rb = 1
imageurl_exclusion = 1
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

search_command = ''

def play_sound(file_path,play_cnt):
    mixer.init()
    mixer.music.load(file_path)
    mixer.music.play(play_cnt)

#設定ウィンドウ [ make_setting_window() ] のアップデート
def update_setting_window(preset_name_combo):

        global preset_name
        global search_word
        global nogood_word
        global since_rb
        global imageurl_exclusion
        global reply_exclusion
        global specity_h
        global specity_m
        global specity_s
        global specity_date
        global search_command
        global streamtext_font_size
        global streamtext_color
        global streamtext_font_name
        global streamtext_font_path
        global streamtext_displaytype
        global streamtext_scrollspeed

        if preset_name_combo == '(新規名称未設定)':

            preset_name = ''
            search_word = ''
            nogood_word = ''
            since_rb = 1
            imageurl_exclusion = 1
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

            search_command = ''

            main_window['-calender_button-'].update(disabled = since_rb)
            main_window['-spin_h-'].update(disabled = since_rb)
            main_window['-spin_m-'].update(disabled = since_rb)
            main_window['-spin_s-'].update(disabled = since_rb)

            main_window['-preset_name-'].update(value = preset_name)
            main_window['-search_word-'].update(value = search_word)
            main_window['-nogood_word-'].update(value = nogood_word)
            main_window['-imageurl_exclusion-'].update(value = imageurl_exclusion)
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
            imageurl_exclusion = int(read_main_config.get('main_setting', 'imageurl_exclusion'))
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
            main_window['-imageurl_exclusion-'].update(value = imageurl_exclusion)
            main_window['-reply_exclusion-'].update(value = reply_exclusion)
            main_window['-calender_input-'].update(value = specity_date)
            main_window['-spin_h-'].update(value = specity_h)
            main_window['-spin_m-'].update(value = specity_m)
            main_window['-spin_s-'].update(value = specity_s)

def make_welcome_window():
        main_layout = [  [sg.Image(filename = 'data/img/tweetron_icon.png', pad = ((0,0),(15,0)))],
                            [sg.Text(text = 'Tweetronへようこそ', pad = ((0,0),(0,0)))],
                            [sg.Text(text = 'Twitterアカウントの認証を行ってください', pad = ((0,0),(50,0)))],
                            [sg.Button(button_text = '認証', font = ['Meiryo',10], size = (20,1), pad = ((0,0),(20,0)), key = 'Auth_Button')] ]
        return sg.Window(window_title, main_layout, icon = png_icon_path, size = (700,500), font = ['Meiryo',12], element_justification='c')

def make_twitteroauth_window():
        twitter_oauth_layout = [ [sg.Text(text = '表示されたPINを入力してください', pad = ((0,0),(30,0)))],
                            [sg.Input(size = (10,1), pad = ((0,10),(15,0)), tooltip = 'ブラウザに表示された7桁のPINコードを入力してください', key = 'pin_code')],
                            [sg.Button(button_text = 'OK', font = ['Meiryo',10], size = (10,1), pad = ((0,15),(20,0)), key = 'AuthPIN_Button_OK'), sg.Button(button_text = 'Cancel', font = ['Meiryo',10], size = (10,1), pad = ((15,0),(20,0)), key = 'AuthPIN_Button_Cancel')] ]
        return sg.Window(window_title, twitter_oauth_layout, icon = png_icon_path, size = (500,200), font = ['Meiryo',12], element_justification='c')

def make_setting_window():

        global preset_name
        global search_word
        global nogood_word
        global since_rb
        global imageurl_exclusion
        global reply_exclusion
        global specity_h
        global specity_m
        global specity_s
        global specity_date

        if since_rb == 1:
            since_auto_rb = 1
            since_specify_rb = 0
        else:
            since_auto_rb = 0
            since_specify_rb = 1

        main_layout = [  [sg.Text(text = 'プリセット一覧', pad = ((0,10),(10,0)), font = ['Meiryo',10]), sg.Combo(values = preset_list, default_value = preset_list[-1], size=(60,1), font = ['Meiryo',8], readonly = True, pad = ((0,0),(10,0)), enable_events = True, key = '-preset_list_combo-'), sg.Button(button_text = 'プリセット削除', font = ['Meiryo',8], size = (15,1), pad = ((20,0),(8,0)), disabled = True, k = '-preset_del-')],
                         [sg.Text(text = '_____________________________________________________________________________________', pad = ((0,0),(5,0)), font = ['Meiryo',10], text_color = '#bdbdbd')],
                         [sg.Text(text = 'プリセット名', pad = ((0,22),(20,0)), font = ['Meiryo',10]), sg.Input(default_text = preset_name, size=(100,1), font = ['Meiryo',8], tooltip = 'プリセット名を入力してください', pad = ((0,0),(20,0)), key = '-preset_name-')],
                         [sg.Text(text = '検索ワード(単語ごとに改行してください)', pad = ((0,0),(20,0)), font = ['Meiryo',10], justification = 'left'), sg.Text(text = 'NGワード(単語ごとに改行してください)', pad = ((100,0),(20,0)), font = ['Meiryo',10], justification = 'center')],
                         [sg.Multiline(default_text = search_word, size = (39,5), font = ['Meiryo',10], key = '-search_word-'), sg.Multiline(default_text = nogood_word, size = (40,5), font = ['Meiryo',10], tooltip = 'NGワードに設定された単語が含まれているツイートを除外します', key = '-nogood_word-')],
                         [sg.Radio(text = '検索開始時から投稿されたツイートのみ取得', font = ['Meiryo',10], pad = ((0,0),(20,0)), group_id = 0, default = since_auto_rb, enable_events = True, k = '-rb_01-'), sg.Radio(text = '指定した日時から投稿されたツイートのみ取得', font = ['Meiryo',10], pad = ((57,0),(20,0)), group_id = 0, default = since_specify_rb, enable_events = True, k = '-rb_02-')],
                         [sg.Checkbox(text = 'ツイートの画像URLを除外(推奨)', font = ['Meiryo',10], pad = ((0,0),(20,0)), default = imageurl_exclusion, key = '-imageurl_exclusion-'), sg.Text(text = '日付指定', pad = ((125,10),(20,0)), font = ['Meiryo',10]),
                         sg.Input(default_text = specity_date, size=(30,1), font = ['Meiryo',8], tooltip = '指定された日時から最新のツイートを取得します', pad = ((0,0),(20,0)), readonly = True, key = '-calender_input-'),
                         sg.CalendarButton('選択', title='日付選択', target = '-calender_input-', no_titlebar=False, format = '20%y-%m-%d', default_date_m_d_y = (dt_now.month,dt_now.day,dt_now.year), close_when_date_chosen = True, month_names=('1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'), day_abbreviations=('月', '火', '水', '木', '金', '土', '日'), size = (5,1), font = ['Meiryo',8], pad = ((10,0),(20,0)), disabled = True, k = '-calender_button-')],
                         [sg.Checkbox(text = 'リプライを除外', font = ['Meiryo',10], pad = ((0,0),(20,0)), default = reply_exclusion, key = '-reply_exclusion-'), sg.Button(button_text = '検索コマンド設定', font = ['Meiryo',8], size = (15,1), pad = ((60,0),(20,0)), k = '-filter_setting-'), sg.Text(text = '時間指定', pad = ((57,10),(20,0)), font = ['Meiryo',10]),
                         sg.Spin(values = time_h_list, initial_value = specity_h, font = ['Meiryo',10], pad = ((0,0),(20,0)), readonly = True, disabled = True, k = '-spin_h-'), sg.Text(text = '時', pad = ((10,0),(20,0)), font = ['Meiryo',10]),
                         sg.Spin(values = time_m_list, initial_value = specity_m, font = ['Meiryo',10], pad = ((10,0),(20,0)), readonly = True, disabled = True, k = '-spin_m-'), sg.Text(text = '分', pad = ((10,0),(20,0)), font = ['Meiryo',10]),
                         sg.Spin(values = time_s_list, initial_value = specity_s, font = ['Meiryo',10], pad = ((10,0),(20,0)), readonly = True, disabled = True, k = '-spin_s-'), sg.Text(text = '秒', pad = ((10,0),(20,0)), font = ['Meiryo',10])],
                         [sg.Button(button_text = 'テキスト詳細設定', font = ['Meiryo',8], size = (20,1), pad = ((0,0),(20,0)), k = '-text_set-'), sg.Button(button_text = 'テキスト表示形式設定', font = ['Meiryo',8], size = (20,1), pad = ((30,0),(20,0)), k = '-display_set-'),
                         sg.Button(button_text = 'プリセット保存', font = ['Meiryo',8], size = (20,1), pad = ((30,0),(20,0))), sg.Button(button_text = '実行', font = ['Meiryo',8], size = (20,1), pad = ((30,0),(20,0)))] ]
        return sg.Window(window_title, main_layout, icon = png_icon_path, size = (700,465), font = ['Meiryo',12], finalize = True)

def make_filterset_window():

        global search_command

        if search_command == 'null':
            search_command = ''

        filterset_layout = [ [sg.Text(text = '検索コマンド', pad = ((0,0),(20,0))), sg.Input(default_text = search_command, size = (50,1), pad = ((15,0),(20,0)), tooltip = 'コマンドを入力してください', k = '-filter_input-')],
                            [sg.Text(text = '公式が用意したコマンドを使用してツイート検索にフィルタを設定できます\n(※sinceコマンドは使用できません)\nコマンド一覧の引用元(https://yonoi.com/twitter-search-command/)', pad = ((0,0),(20,0)), font = ['Meiryo',8], text_color = '#808080'), sg.Button(button_text = 'コマンド一覧', font = ['Meiryo',8], size = (13,1), pad = ((17,0),(20,0)), key = '-command_list-')],
                            [sg.Button(button_text = 'OK', font = ['Meiryo',8], size = (15,1), pad = ((100,15),(20,0)), key = 'Button_OK'), sg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (15,1), pad = ((45,0),(20,0)), key = 'Button_Cancel')] ]
        return sg.Window('検索コマンド設定', filterset_layout, icon = png_icon_path, size = (500,185), font = ['Meiryo',10])

def make_textset_window():

        global streamtext_font_size
        global streamtext_color
        global streamtext_font_name
        global streamtext_font_path

        if streamtext_font_path == 'null':
            streamtext_font_path = ''

        textset_layout = [ [sg.Text(text = 'Sampleテキスト', pad = ((0,0),(20,0)), size = (50,1), font = [streamtext_font_name,streamtext_font_size], text_color = streamtext_color, auto_size_text = False, k = '-sample_text-')],
                            [sg.Text(text = '_____________________________________________________________________________________', pad = ((0,0),(5,0)), font = ['Meiryo',10], text_color = '#bdbdbd')],
                            [sg.Text(text = '実際に表示されるテキストと若干異なる場合があります\n下の[実際に確認する]を選択し、ブラウザで確認することをおすすめします', pad = ((0,0),(20,0)), font = ['Meiryo',8], text_color = '#808080')],
                            [sg.Text(text = 'サンプルテキスト', pad = ((0,0),(20,0))), sg.Input(default_text = 'Sampleテキスト', size = (50,1), pad = ((15,0),(20,0)), tooltip = 'サンプルテキストを変更できます', enable_events = True, k = '-sample_text_input-')],
                            [sg.Text(text = 'フォントサイズ', pad = ((0,0),(20,0))), sg.Spin(values = fontsize_list, initial_value = streamtext_font_size, pad = ((10,0),(20,0)), enable_events = True, k = '-fontsize_spin-'),
                            sg.Text(text = 'テキストカラー', pad = ((10,0),(20,0))), sg.Input(default_text = streamtext_color, size = (22,1), pad = ((10,0),(20,0)), enable_events = True, tooltip = '16進数のカラーコードを指定できます\n( # から入力してください)', k = '-color_input-'), sg.ColorChooserButton(button_text = '選択', size = (5,1), pad = ((10,0),(20,0)), target = '-color_input-', k = '-cc_button-')],
                            [sg.Text(text = 'フォントリスト', pad = ((0,0),(20,0)))],
                            [sg.Text(text = '以下のリストから指定してもうまく反映されない場合があります\nその場合直接ttfファイルを読み込むことをおすすめします', pad = ((0,0),(0,0)), font = ['Meiryo',8], text_color = '#808080')],
                            [sg.Input(default_text = streamtext_font_name, size = (60,1), pad = ((0,0),(5,5)), tooltip = 'フォント名を直接指定できます', enable_events = True, k = '-font_name_input-')],
                            [sg.Listbox(fonts_list, size = (60,10), default_values = font_name, enable_events = True, highlight_background_color = '#4169e1', pad = ((0,0),(0,0)), key = '-font_list-')],
                            [sg.Input(default_text = streamtext_font_path, size = (53,1), pad = ((0,0),(10,5)), tooltip = 'ttfフォントを指定できます', enable_events = True, k = '-font_path-'), sg.FileBrowse(button_text = '参照', target = "-font_path-", file_types=((".ttf file", "*.ttf"),), size = (5,1), pad = ((10,0),(10,5)))],
                            [sg.Button(button_text = 'OK', font = ['Meiryo',8], size = (15,1), pad = ((10,15),(20,0)), key = 'Button_OK'), sg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (15,1), pad = ((45,0),(20,0)), key = 'Button_Cancel'), sg.Button(button_text = '実際に確認する', font = ['Meiryo',8], size = (15,1), pad = ((60,0),(20,0)), key = '-Verification-')] ]
        return sg.Window('テキスト詳細設定', textset_layout, icon = png_icon_path, size = (500,750), font = ['Meiryo',10], finalize = True)

def make_displayset_window():

        global streamtext_displaytype

        rb_default = []
        if streamtext_displaytype == 1:
            rb_default = [True,False]
        else:
            rb_default = [False,True]

        displayset_layout = [ [sg.Image(filename = 'data/img/ex_img_01.png', pad = ((0,0),(30,0)))],
                                [sg.Radio(text = 'ツイートとユーザーネームを一行に表示する(従来の方式)', font = ['Meiryo',10], pad = ((0,0),(20,0)), group_id = 0, default = rb_default[0], enable_events = True, k = '-rb_01-')],
                                [sg.Text(text = 'OBS-Twitter-Streamで使用されていた方式です\nツイートとユーザーネームを一行に合わせて表示します', pad = ((0,0),(20,0)), font = ['Meiryo',8], text_color = '#808080')],
                                [sg.Text(text = '_____________________________________________________________________________________', pad = ((0,0),(15,0)), font = ['Meiryo',10], text_color = '#bdbdbd')],
                                [sg.Image(filename = 'data/img/ex_img_02.png', pad = ((0,0),(30,0)))],
                                [sg.Radio(text = 'ツイートとユーザーネームを分ける', font = ['Meiryo',10], pad = ((0,0),(20,0)), group_id = 0, default = rb_default[1], enable_events = True, k = '-rb_02-')],
                                [sg.Text(text = 'ツイートとユーザーネームを上下に分けて表示します\nスクリーンネームだけでなくユーザーネームも表示できます\n(上下の間隔は設定できませんのでクロップ機能を使って分けて頂く必要があります)', pad = ((0,0),(20,0)), font = ['Meiryo',8], text_color = '#808080')],
                                [sg.Text(text = 'テキストのスクロールスピード', pad = ((118,0),(30,0)), font = ['Meiryo',10]),
                                sg.Spin(values = streamtext_scrollspeed_list, initial_value = streamtext_scrollspeed, pad = ((0,0),(30,0)), enable_events = True, readonly = True, k = '-scrollspeed_spin-'), sg.Text(text = '%', pad = ((0,0),(30,0)), font = ['Meiryo',10])],
                                [sg.Button(button_text = 'OK', font = ['Meiryo',8], size = (15,1), pad = ((90,15),(35,0)), key = 'Button_OK'), sg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (15,1), pad = ((45,0),(35,0)), key = 'Button_Cancel')] ]
        return sg.Window('テキスト表示形式設定', displayset_layout, icon = png_icon_path, size = (500,550), font = ['Meiryo',10], finalize=True)

if twitter_oauth_sw == 0:

    main_window = make_welcome_window()

    while True:
        main_event, main_values = main_window.read()
        if main_event == sg.WIN_CLOSED:
            break

        elif main_event == 'Auth_Button':

            main_window.Element('Auth_Button').Update(disabled = True)

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

            auth_url = auth.get_authorization_url()
            webbrowser.open(auth_url)

            twitter_oauth_window = make_twitteroauth_window()

            while True:
                twitter_oauth_event, twitter_oauth_values = twitter_oauth_window.read()

                if twitter_oauth_event == sg.WIN_CLOSED or twitter_oauth_event == 'Cancel':
                    main_window.Element('Auth_Button').Update(disabled = False)
                    break

                elif twitter_oauth_event == 'AuthPIN_Button_OK':

                    auth.get_access_token(twitter_oauth_values['pin_code'])
                    auth.set_access_token(auth.access_token, auth.access_token_secret)

                    main_config['TwitterAPI'] = {
                        'access_token': auth.access_token,
                        'access_token_secret': auth.access_token_secret
                    }

                    main_config['MainConfig'] = {
                        'OAuth2_sw': 1
                    }

                    with open('data/ini/config.ini', 'w') as cw:
                        main_config.write(cw)

                    value = sg.popup_ok('認証が完了しました')
                    twitter_oauth_sw = 1

                    main_window.close()
                    twitter_oauth_window.close()
                    break

        if twitter_oauth_sw == 1:
            break

    if twitter_oauth_sw == 0:
        main_window.close()

if twitter_oauth_sw == 1:
    main_window = make_setting_window()

while True:
    main_event, main_values = main_window.read()

    if main_event == sg.WIN_CLOSED:
        break

    #日付設定類の有効化無効化
    if main_event == '-rb_01-':
        main_window['-calender_button-'].update(disabled = True)
        main_window['-spin_h-'].update(disabled = True)
        main_window['-spin_m-'].update(disabled = True)
        main_window['-spin_s-'].update(disabled = True)

    if main_event == '-rb_02-':
        main_window['-calender_button-'].update(disabled = False)
        main_window['-spin_h-'].update(disabled = False)
        main_window['-spin_m-'].update(disabled = False)
        main_window['-spin_s-'].update(disabled = False)

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

        imageurl_exclusion = int(main_values['-imageurl_exclusion-'])
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

            sg.popup_ok(error_message, title = window_title, icon = png_icon_path)

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
            write_main_config.set('main_setting', 'imageurl_exclusion', imageurl_exclusion)
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

            with open('data/preset/' + main_values['-preset_name-'] + '/config.ini', 'w') as file:
                write_main_config.write(file)

            with open('data/preset/' + main_values['-preset_name-'] + '/search_word.txt', mode='w') as file:
                file.write(search_word)

            with open('data/preset/' + main_values['-preset_name-'] + '/nogood_word.txt', mode='w') as file:
                file.write(nogood_word)

            play_sound('data/sound/complete.mp3',1)

            sg.popup_ok('プリセットを保存しました', title = window_title, icon = png_icon_path)

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

    #検索フィルタ設定
    if main_event == '-filter_setting-':

        filterset_window = make_filterset_window()

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

        textset_window = make_textset_window()
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
                        htmlcss_save.save_test_css(textset_values['-font_name_input-'], textset_values['-color_input-'], textset_values['-fontsize_spin-'], textset_values['-font_path-'])
                    else:
                        htmlcss_save.save_test_css(textset_values['-font_name_input-'], textset_values['-color_input-'], textset_values['-fontsize_spin-'])

                    #設定されているサンプルテキストを適用したhtmlファイルを作成
                    htmlcss_save.save_test_html(textset_values['-sample_text_input-'])
                    time.sleep(0.5)
                    subprocess.Popen(['start', 'data/html/verification/verification.html'], shell = True)

                else:
                    value = sg.popup_ok('カラーコードを指定してください', title = window_title, icon = png_icon_path)

            if textset_event == 'Button_OK':

                if os.path.exists(textset_values['-font_path-']) == False and textset_values['-font_path-'] != '':
                    sg.popup_ok('指定したttfファイルが存在しません', title = window_title, icon = png_icon_path)
                else:
                    streamtext_font_size = int(textset_values['-fontsize_spin-'])
                    streamtext_color = textset_values['-color_input-']
                    streamtext_font_name = textset_values['-font_name_input-']
                    streamtext_font_path = textset_values['-font_path-']

                    break

        textset_window.close()

    #テキスト表示設定
    if main_event == '-display_set-':

        displayset_window = make_displayset_window()

        while True:
            displayset_event, displayset_values = displayset_window.read()

            if displayset_event == sg.WIN_CLOSED or displayset_event == 'Button_Cancel':
                break

            if displayset_event == 'Button_OK':
                if displayset_values['-rb_01-'] == True:
                    streamtext_displaytype = 1
                else:
                    streamtext_displaytype = 2

                streamtext_scrollspeed = displayset_values['-scrollspeed_spin-']

                break

        displayset_window.close()

    #プリセット実行
    if main_event == '実行':

        preset_name = str(main_values['-preset_name-'])

        search_word = str(main_values['-search_word-'])
        nogood_word = str(main_values['-nogood_word-'])

        imageurl_exclusion = int(main_values['-imageurl_exclusion-'])
        reply_exclusion = int(main_values['-reply_exclusion-'])
        specity_date = str(main_values['-calender_input-'])
        specity_h = int(main_values['-spin_h-'])
        specity_m = int(main_values['-spin_m-'])
        specity_s = int(main_values['-spin_s-'])

        if search_word.replace('\n','') == '' or preset_name == '':

            error_message = ''

            if main_values['-preset_name-'] == '':
                error_message += 'プリセット名を設定してください\n'

            if main_values['-search_word-'].replace('\n','') == '':
                error_message += '検索ワードを設定してください'

            sg.popup_ok(error_message)

        else:

            #実際に使用するcssを作成
            if streamtext_font_path != '' and streamtext_font_path != 'null':
                htmlcss_save.save_css(streamtext_font_name, streamtext_color, streamtext_font_size, streamtext_font_path)
            else:
                htmlcss_save.save_css(streamtext_font_name, streamtext_color, streamtext_font_size)

            #テキスト表示設定をもとに2つのタイプから選択
            if streamtext_displaytype == 1:
                shutil.copy('./data/html/type_01.html','Tweetron.html')
            else:
                shutil.copy('./data/html/type_02.html','Tweetron.html')

            os.system("taskkill /f /im Tweetron_Core.exe")
            subprocess.Popen(['start', 'data/Tweetron_Core.exe', preset_name], shell = True)

main_window.close()
