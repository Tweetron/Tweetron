'''

Tweetron_Core.py

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

figlet_text = r'''
 _______                _
|__   __|              | |
   | |_      _____  ___| |_ _ __ ___  _ __
   | \ \ /\ / / _ \/ _ \ __| '__/ _ \| '_ \
   | |\ V  V /  __/  __/ |_| | | (_) | | | |
   |_| \_/\_/ \___|\___|\__|_|  \___/|_| |_|

'''

import tweepy
import webbrowser
import configparser
import random
from websocket_server import WebsocketServer
import time
import datetime
import os
from termcolor import colored, cprint
import colorama
import re
import sys
import json
from xml.sax.saxutils import unescape
import argparse

from tweetron_library import webscript_save, utility, tweetron_variable

import api_key

import software_info
version = software_info.VERSION()



parser = argparse.ArgumentParser(description = 'Tweetron ver' + version)

parser.add_argument('--preset_name', required = True)
parser.add_argument('--debug_mode', required = True)
args = parser.parse_args()
preset_name = args.preset_name
debugmode_sw = bool(int(args.debug_mode))


#original_src: demoji(https://github.com/bsolomon1124/demoji)
demoji_json_open = open('tweetron_data/emoji_codes.json', 'r', encoding = 'utf-8')
demoji_json_load = json.load(demoji_json_open)

def delete_emoji(original_string):

    global demoji_json_load

    escp = (re.escape(c) for c in sorted(demoji_json_load, key = len, reverse = True))
    emoji_pattern = re.compile(r"|".join(escp))

    return emoji_pattern.sub('', original_string)

colorama.init()

def print_info(text):
    print(colored('[INFO] ', 'green'), text)

def print_warning(text):
    print(colored('[WARNING] ', 'yellow'), text)

def print_error(text):
    print(colored('[ERROR] ', 'red'), text)

settingvalue_dict_all = tweetron_variable.reset_settingvalue_dict_all(datetime)
datetime_now = datetime.datetime.now()



consumer_key = api_key.CONSUMER_KEY()
consumer_secret = api_key.CONSUMER_SECRET()
callback_url = 'oob'

main_config = configparser.ConfigParser()
main_config.read('tweetron_data/ini/config.ini', encoding='utf-8')

access_token = main_config.get('TwitterAPI', 'access_token')
access_token_secret = main_config.get('TwitterAPI', 'access_token_secret')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

port_number = main_config.get('MainConfig', 'portnumber')



tweet_send_cnt = 0
searchword_loop_cnt = 0
searchword_loop_cnt_tmp = 0
tweet_list_text = []
tweet_text_tmp = ''
relast_id = '0'
relast_id_tmp = ''
checkid = ''
checkid_loop = 0
checkid_sw = 0
loadloop_sw = 0
nogood_word_list = ''
current_client_id = 0



os.system('title Tweetron v' + version)

print(colored(figlet_text, 'cyan'))
print(colored('Version: ' + version + '\n', 'green'))
print(colored('Developed by Tweetron Developers', 'cyan'))
print(colored('https://github.com/Tweetron/\n', 'cyan'))



read_main_config = configparser.RawConfigParser()
read_main_config.read('tweetron_data/preset/' + preset_name  + '/config.ini')

for key_p_name in settingvalue_dict_all.keys():
    for key_c_name in settingvalue_dict_all[key_p_name].keys():
        if utility.isint(read_main_config.get(key_p_name, key_c_name)) == True:
            settingvalue_dict_all[key_p_name][key_c_name] = int(read_main_config.get(key_p_name, key_c_name))
        else:
            settingvalue_dict_all[key_p_name][key_c_name] = read_main_config.get(key_p_name, key_c_name)



with open('tweetron_data/preset/' + preset_name + '/search_word.txt') as file:
    for i in range(sum(1 for line in open('tweetron_data/preset/' + preset_name + '/search_word.txt'))):
        if i == 0:
            search_word = file.readline().rstrip(os.linesep)
        else:
            search_word = search_word + ' OR ' + file.readline().rstrip(os.linesep)



with open('tweetron_data/preset/' + preset_name + '/nogood_word.txt') as file:
    nogood_word = file.readlines()

for ngword in nogood_word:
    nogood_word_list = nogood_word_list + ngword + ', '

loadloop_sw = settingvalue_dict_all['display_setting']['text_loadloop']
reply_exclusion_text = 'exclude:replies' if settingvalue_dict_all['main_setting']['reply_exclusion'] == 1 else ''
search_command = '' if settingvalue_dict_all['filter_setting']['search_command'] == 'null' else settingvalue_dict_all['filter_setting']['search_command']
since_date = datetime_now.strftime('%Y-%m-%d_%H:%M:%S_JST') if settingvalue_dict_all['main_setting']['since_rb'] == 1 else settingvalue_dict_all['main_setting']['searchdate'] + '_' + str(settingvalue_dict_all['main_setting']['searchdate_h']).zfill(2) + ':' + str(settingvalue_dict_all['main_setting']['searchdate_m']).zfill(2) + ':' + str(settingvalue_dict_all['main_setting']['searchdate_s']).zfill(2) + '_JST'

search_text_raw = search_word + ' -filter:retweets since:' + since_date + ' ' + reply_exclusion_text + ' ' + search_command



print_info('再起動をした場合は再度[ Tweetron.html ]を読み込んでください')
if debugmode_sw == True: print_info('デバッグモード: 有効')
print_info('使用プリセット: ' + preset_name + ' ポート番号: ' + str(port_number))
print_info('検索ワード: ' + search_text_raw)

print_info('NGワードは設定されていません') if nogood_word_list == '' else print_info('NGワードリスト: ' + nogood_word_list)



def search_word_api(si):

    tweet_list = []
    tweet_text_raw = ''

    global searchword_loop_cnt
    global relast_id
    global checkid_sw
    global streamtext_displaytype
    global status_list
    global since_date
    global since_rb

    searchword_loop_cnt = 0

    #ワード検索
    if si == '0':
        tweets = api.search_tweets(q = search_text_raw, result_type = 'recent', count = random.randint(10,30), include_entities = False, tweet_mode = 'extended')
    else:
        #前回取得したツイートより最新のツイートを取得する
        tweets = api.search_tweets(q = search_text_raw, result_type = 'recent', count = random.randint(5,10), include_entities = False, tweet_mode = 'extended', since_id = si)

    for result in tweets:
        tweet_text_raw = unescape(result.full_text)

        ng_flag = 0

        for nogood_word_if in nogood_word:
            if nogood_word != '' and nogood_word_if in tweet_text_raw: ng_flag = 1

        if ng_flag == 0:
            if searchword_loop_cnt == 0: relast_id = result.id_str

            #画像URLを削除
            tweet_text = re.sub(r'https://t.co/\w{10}', '', tweet_text_raw)

            if settingvalue_dict_all['main_setting']['emoji_exclusion'] == 1: tweet_text = delete_emoji(tweet_text)

            #それぞれの表示形態に合わせて整形
            if settingvalue_dict_all['display_setting']['text_displaytype'] == 1:
                tweet_list.append(tweet_text.replace('\n','') +' (@'+ unescape(result.user.name) +')')
            else:
                tweet_list.append(unescape(result.user.name) + ' (@' + unescape(result.user.screen_name) + ')\n' + tweet_text.replace('\n',''))

            searchword_loop_cnt += 1

    if debugmode_sw == True: print_info('取得したツイート数: ' + str(searchword_loop_cnt))

    return tweet_list



#ツイートID取得
def checkid_relast():

    relast_id_return = ''
    lpcnt = 0

    tweets = api.search_tweets(q = search_text_raw, result_type = 'recent', count = 3, include_entities = False)

    for result in tweets:
        if lpcnt == 0: relast_id_return = result.id_str

        lpcnt += 1

    return relast_id_return



#JSと接続
def new_client(client, server):

    dt_now = datetime.datetime.now()

    global tweet_send_cnt
    global random_list
    global tweet_list_text
    global random_list
    global checkid
    global relast_id
    global relast_id_tmp
    global checkid_loop
    global current_client_id

    current_client_id = client['id']

    print_info(dt_now.strftime('%H:%M:%S') + ' server.ID[' + str(client['id']) + '] - 接続されました')

    tweet_send_cnt = 0
    tweet_list_text = []
    random_list = []

    tweet_list_text = search_word_api('0')
    relast_id_tmp = relast_id
    checkid = relast_id

    if searchword_loop_cnt != 0:
        tweet_text_tmp = random.choice(tweet_list_text)
        tweet_list_text.remove(tweet_text_tmp)

        server.send_message(client, tweet_text_tmp)

        checkid_loop += 1
    else:
        print_warning('ツイートが存在しません テストツイートを行い、しばらくしてからページを再読込してください')



#JSから切断
def client_left(client, server):
    dt_now = datetime.datetime.now()

    if current_client_id != client['id']:
        print_warning(dt_now.strftime('%H:%M:%S') + ' server.ID[' + str(client['id']) + '] - クライアントの重複により切断されました')
    else:
        print_info(dt_now.strftime('%H:%M:%S') + ' server.ID[' + str(client['id']) + '] - 切断されました')



#JSからのメッセージ受信
def message_received(client, server, message):

    global tweet_send_cnt
    global random_list
    global tweet_list_text
    global random_list
    global searchword_loop_cnt
    global relast_id
    global checkid
    global checkid_loop
    global checkid_sw
    global relast_id_tmp
    global current_client_id

    #JSから送信が来た場合ツイートを送る
    if message == 'JS':

        if debugmode_sw == True: print_info('現在のツイート数: ' + str(len(tweet_list_text)) + ' / 現在の最新id:' + str(relast_id) + ' / 控えid: ' + str(relast_id_tmp))

        #searchword_loop_cnt = 0 は取得できるツイートが存在しない
        if searchword_loop_cnt != 0:

            #すべてのツイートストックを送信し終えた
            if not tweet_list_text:
                time.sleep(0.5)

                tweet_list_text = []

                if loadloop_sw == 0:

                    #idを指定してツイートを取得
                    tweet_list_text = search_word_api(relast_id)
                    if debugmode_sw == True: print_info('取得された最新id:' + str(relast_id))

                    #前回取得したツイートより最新のツイートが存在する場合
                    if relast_id_tmp != relast_id:
                        relast_id_tmp = relast_id

                        checkid = relast_id
                        checkid_loop = 0

                        if debugmode_sw == True: print_info('取得/送信タイプ: 1')

                        while True:

                            if bool(tweet_list_text):

                                tweet_text_tmp = random.choice(tweet_list_text)
                                tweet_list_text.remove(tweet_text_tmp)

                                server.send_message(client, tweet_text_tmp)

                                checkid_loop += 1
                                break

                            time.sleep(5)
                            tweet_list_text = search_word_api(relast_id)

                    #前回取得したツイートより最新のツイートが存在しない場合
                    else:

                        tweet_list_text = []
                        checkid_loop = 0

                        if debugmode_sw == True: print_info('取得/送信タイプ: 2')

                        while True:

                            #idを指定せずにツイートを取得
                            tweet_list_text = search_word_api('0')

                            if bool(tweet_list_text):

                                tweet_text_tmp = random.choice(tweet_list_text)
                                tweet_list_text.remove(tweet_text_tmp)

                                server.send_message(client, tweet_text_tmp)

                                checkid_loop += 1
                                break

                            time.sleep(5)

                    #最新のツイートのみ受け付ける
                else:

                    if debugmode_sw == True: print_info('取得/送信タイプ: 3')

                    while True:
                        time.sleep(10)

                        if current_client_id != client['id']: break

                        checkid = checkid_relast()
                        checkid_loop = 0

                        if checkid != relast_id:

                            tweet_list_text = []
                            relast_id_tmp = checkid

                            while True:

                                tweet_list_text = search_word_api(relast_id)

                                if bool(tweet_list_text):

                                    tweet_text_tmp = random.choice(tweet_list_text)
                                    tweet_list_text.remove(tweet_text_tmp)

                                    server.send_message(client, tweet_text_tmp)

                                    checkid_loop += 1
                                    break

                                time.sleep(5)

                            if checkid_loop > 0:
                                break


            #まだ未送信のツイートがある
            else:

                if debugmode_sw == True: print_info('取得/送信タイプ: 4')

                tweet_text_tmp = random.choice(tweet_list_text)
                tweet_list_text.remove(tweet_text_tmp)

                server.send_message(client, tweet_text_tmp)

                checkid_loop += 1

                #5回目のループで最新のツイートがあるかidを取得
                if checkid_loop >= 5:
                    checkid = checkid_relast()
                    checkid_loop = 0

                #取得したidを検証/最新のものであれば強制再取得
                if checkid != relast_id:
                    tweet_list_text.clear()
                    if debugmode_sw == True: print_info('ツイートリスト強制更新')

        else:

            print_warning('ツイートが存在しません テストツイートを行い、しばらくしてからページを再読込してください')



server = WebsocketServer(port = int(port_number))

server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)

server.run_forever()
