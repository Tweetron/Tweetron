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

#ライブラリインポート
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

#APIキー読み込み
import api_key

import software_info
version = software_info.VERSION()

#APIキー割り当て
consumer_key = api_key.CONSUMER_KEY()
consumer_secret = api_key.CONSUMER_SECRET()
callback_url = 'oob'

tweet_send_cnt = 0
searchword_loop_cnt = 0
searchword_loop_cnt_tmp = 0

random_list = []
tweet_list_text = []
random_list = []

relast_id = '0'
relast_id_tmp = ''

checkid = ''
checkid_loop = 0
checkid_sw = 0

nogood_word_list = ''

colorama.init()

#original_src: demoji(https://github.com/bsolomon1124/demoji)
def delete_emoji(original_string):

    global demoji_json_load

    escp = (re.escape(c) for c in sorted(demoji_json_load, key = len, reverse = True))
    emoji_pattern = re.compile(r"|".join(escp))

    return emoji_pattern.sub('', original_string)

#それぞれのステータスに色割り当て
def print_info(text):
    print(colored('[INFO] ', 'green'), text)

def print_warning(text):
    print(colored('[WARNING] ', 'yellow'), text)

def print_error(text):
    print(colored('[ERROR] ', 'red'), text)

os.system('title Tweetron v' + version)

print(colored(figlet_text, 'cyan'))
print(colored('Hello! Welcome to Tweetron!', 'cyan'), colored('Version: ' + version, 'green'))
print(colored('https://github.com/CubeZeero/Tweetron', 'cyan'))
print(colored('(C)Cube', 'cyan'))
print('\n')

try:
    preset_name = sys.argv[1]
except:
    print_error('TweetronCore.exe を直接起動せずに Tweetron.exe の[実行]から起動してください')
    time.sleep(10)

    sys.exit()

if os.path.isdir('data/preset/' + preset_name) == False:
    print_error('プリセット [' + preset_name + '] は存在しません 10秒後にシャットダウンします')
    time.sleep(10)

    sys.exit()

demoji_json_open = open('data/emoji_codes.json', 'r')
demoji_json_load = json.load(demoji_json_open)

#プリセット設定読み込み
read_main_config = configparser.RawConfigParser()

read_main_config.read('data/preset/' + preset_name  + '/config.ini')

since_rb = int(read_main_config.get('main_setting', 'since_rb'))
reply_exclusion = int(read_main_config.get('main_setting', 'reply_exclusion'))
emoji_exclusion = int(read_main_config.get('main_setting', 'emoji_exclusion'))
specity_date = str(read_main_config.get('main_setting', 'specity_date'))
specity_h = int(read_main_config.get('main_setting', 'specity_h'))
specity_m = int(read_main_config.get('main_setting', 'specity_m'))
specity_s = int(read_main_config.get('main_setting', 'specity_s'))
search_command = str(read_main_config.get('filter_setting', 'search_command'))
streamtext_displaytype = int(read_main_config.get('textdisplay_setting', 'streamtext_displaytype'))

if search_command == 'null':
    search_command = ''

#検索ワード読み込み
with open('data/preset/' + preset_name + '/search_word.txt') as file:
    for i in range(sum(1 for line in open('data/preset/' + preset_name + '/search_word.txt'))):
        if i == 0:
            search_word = file.readline().rstrip(os.linesep)
        else:
            search_word = search_word + ' OR ' + file.readline().rstrip(os.linesep)

#NGワード読み込み
with open('data/preset/' + preset_name + '/nogood_word.txt') as file:
    nogood_word = file.readlines()

for ngword in nogood_word:
    nogood_word_list = nogood_word_list + ngword + ', '

#リプライ除外
if reply_exclusion == 1:
    reply_exclusion_text = 'exclude:replies'
else:
    reply_exclusion_text = ''

#現在時刻取取得
datetime_now = datetime.datetime.now()

if since_rb == 1:
    since_date = datetime_now.strftime('%Y-%m-%d_%H:%M:%S_JST')
else:
    since_date = specity_date + '_' + str(specity_h).zfill(2) + ':' + str(specity_m).zfill(2) + ':' + str(specity_s).zfill(2) + '_JST'

search_text_raw = search_word + ' -filter:retweets since:' + since_date + ' ' + reply_exclusion_text + ' ' + search_command

main_config = configparser.ConfigParser()
main_config.read('data/ini/config.ini', encoding='utf-8')

#TwitterAPI認証
access_token = main_config.get('TwitterAPI', 'access_token')
access_token_secret = main_config.get('TwitterAPI', 'access_token_secret')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)

auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

port_number = main_config.get('MainConfig', 'portnumber')

print_info('再起動をした場合は再度[ Tweetron.html ]を読み込んでください')
print_info('使用プリセット: ' + preset_name + ' ポート番号: ' + str(port_number))
print_info('検索ワード: ' + search_text_raw)


if nogood_word_list == '':
    print_info('NGワードは設定されていません')
else:
    print_info('NGワードリスト: ' + nogood_word_list)

print(colored('--------------------------------------------------------------------------------------------------------------', 'green'),)

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
        tweets = api.search_tweets(q = search_text_raw, result_type = 'recent', count = random.randint(10,50), include_entities = False, tweet_mode='extended')
    else:
        #前回取得したツイートより最新のツイートを取得する
        tweets = api.search_tweets(q = search_text_raw, result_type = 'recent', count = random.randint(5,10), include_entities = False, tweet_mode='extended', since_id = si)

    for result in tweets:
        tweet_text_raw = unescape(result.full_text)

        ng_flag = 0

        for nogood_word_if in nogood_word:
            if nogood_word != '' and nogood_word_if in tweet_text_raw:
                ng_flag = 1

        if ng_flag == 0:
            if searchword_loop_cnt == 0:
                relast_id = result.id_str

            #画像URLを削除
            tweet_text = re.sub(r'https://t.co/\w{10}', '', tweet_text_raw)

            if emoji_exclusion == 1:
                tweet_text = delete_emoji(tweet_text)

            #それぞれの表示形態に合わせて整形
            if streamtext_displaytype == 1:
                tweet_list.append(tweet_text.replace('\n','') +' (@'+ unescape(result.user.name) +')')
            else:
                tweet_list.append(unescape(result.user.name) + ' (@' + unescape(result.user.screen_name) + ')\n' + tweet_text.replace('\n',''))

            searchword_loop_cnt += 1

    return tweet_list

#ツイートID取得
def checkid_relast():

    relast_id_return = ''

    tweets = api.search_tweets(q = search_text_raw, result_type = 'recent', count = 1, include_entities = False)

    for result in tweets:
        relast_id_return = result.id_str

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

    print_info(dt_now.strftime('%H:%M:%S') + ' - 接続されました')

    tweet_send_cnt = 0
    tweet_list_text = []
    random_list = []

    tweet_list_text = search_word_api('0')
    relast_id_tmp = relast_id
    checkid = relast_id

    if searchword_loop_cnt != 0:
        while True:
            random_int = random.randint(0,searchword_loop_cnt -1)
            if random_int not in random_list:
                server.send_message(client, tweet_list_text[random_int])
                checkid_loop += 1
                break
    else:
        print_warning('ツイートが存在しません テストツイートを行い、しばらくしてからページを再読込してください')

#JSから切断
def client_left(client, server):
    dt_now = datetime.datetime.now()

    print_info(dt_now.strftime('%H:%M:%S') + ' - 切断されました')

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

    #JSからRTの送信が来た場合ツイートを送る
    if message == 'JS':

        #searchword_loop_cnt = 0 は取得できるツイートが存在しない
        if searchword_loop_cnt != 0:

            #すべてのツイートストックを送信し終えた
            if tweet_send_cnt == searchword_loop_cnt:
                time.sleep(0.5)

                tweet_send_cnt = 0
                tweet_list_text = []
                random_list = []

                #idを指定してツイートを取得
                tweet_list_text = search_word_api(relast_id)

                #前回取得したツイートより最新のツイートが存在する場合
                if relast_id_tmp != relast_id:
                    relast_id_tmp = relast_id

                    checkid = relast_id
                    checkid_loop = 0

                    while True:
                        random_int = random.randint(0,searchword_loop_cnt -1)
                        if random_int not in random_list:
                            server.send_message(client, tweet_list_text[random_int])
                            checkid_loop += 1
                            break

                    random_list.append(random_int)
                    tweet_send_cnt += 1

                #前回取得したツイートより最新のツイートが存在しない場合
                else:

                    tweet_send_cnt = 0
                    tweet_list_text = []
                    random_list = []
                    checkid_loop = 0

                    #idを指定せずにツイートを取得
                    tweet_list_text = search_word_api('0')

                    while True:
                        random_int = random.randint(0,searchword_loop_cnt -1)
                        if random_int not in random_list:
                            server.send_message(client, tweet_list_text[random_int])
                            checkid_loop += 1
                            break

                    random_list.append(random_int)
                    tweet_send_cnt += 1

            #まだ未送信のツイートがある
            else:

                #5回目のループで最新のツイートがあるかidを取得
                if checkid_loop >= 5:
                    checkid = checkid_relast()
                    checkid_loop = 0

                #取得したidを検証/最新のものであれば強制再取得
                if checkid != relast_id:
                    searchword_loop_cnt = tweet_send_cnt + 1

                while True:
                    random_int = random.randint(0,searchword_loop_cnt -1)
                    if random_int not in random_list:
                        server.send_message(client, tweet_list_text[random_int])
                        checkid_loop += 1
                        break

                random_list.append(random_int)
                tweet_send_cnt += 1

        else:

            print_warning('ツイートが存在しません テストツイートを行い、しばらくしてからページを再読込してください')

server = WebsocketServer(port = int(port_number))

server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)

server.run_forever()
