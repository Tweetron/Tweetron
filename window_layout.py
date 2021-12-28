def make_welcome_window(sg, window_title, png_icon_path):

    main_layout = [

    [sg.Image(filename = 'data/img/tweetron_icon.png', pad = ((0,0),(7,0)))],

    [sg.Text(text = 'Tweetronへようこそ', pad = ((0,0),(0,0)))],
    [sg.Text(text = 'Twitterアカウントの認証を行ってください', pad = ((0,0),(30,0)))],

    [sg.Button(button_text = '認証', font = ['Meiryo',10], size = (20,1), pad = ((0,0),(20,0)), key = '-Auth_Button-')],
    [sg.Button(button_text = 'Tweetronの使用方法', font = ['Meiryo',8], size = (18,1), pad = ((0,0),(20,0)), key = '-wikipage_open-')]

    ]

    return sg.Window(window_title, main_layout, icon = png_icon_path, size = (700,500), font = ['Meiryo',12], element_justification='c')



def make_twitteroauth_window(sg, window_title, png_icon_path):

    twitter_oauth_layout = [

    [sg.Text(text = '表示されたPINを入力してください', pad = ((0,0),(30,0)))],

    [sg.Input(size = (10,1), pad = ((0,10),(15,0)), tooltip = 'ブラウザに表示された7桁のPINコードを入力してください', key = '-pin_code-')],

    [sg.Button(button_text = 'OK', font = ['Meiryo',10], size = (10,1), pad = ((0,15),(20,0)), key = '-AuthPIN_Button_OK-'),
     sg.Button(button_text = 'Cancel', font = ['Meiryo',10], size = (10,1), pad = ((15,0),(20,0)), key = '-AuthPIN_Button_Cancel-')]

    ]

    return sg.Window(window_title, twitter_oauth_layout, icon = png_icon_path, size = (500,200), font = ['Meiryo',12], element_justification='c')



def make_setting_window(sg, window_title, png_icon_path,
                        preset_name, search_word, nogood_word,
                        since_rb, reply_exclusion,
                        specity_h, specity_m, specity_s,
                        specity_date, preset_list, dt_now,
                        time_h_list, time_m_list, time_s_list):

    if since_rb == 1:
        since_auto_rb = 1
        since_specify_rb = 0
    else:
        since_auto_rb = 0
        since_specify_rb = 1

    main_layout = [

    [sg.Text(text = 'プリセット一覧', pad = ((0,10),(10,0)), font = ['Meiryo',10]),
     sg.Combo(values = preset_list, default_value = preset_list[-1], size=(60,1), font = ['Meiryo',8], readonly = True, pad = ((0,0),(10,0)), enable_events = True, key = '-preset_list_combo-'),
     sg.Button(button_text = 'プリセット削除', font = ['Meiryo',8], size = (15,1), pad = ((20,0),(8,0)), disabled = True, k = '-preset_del-')],

    [sg.Text(text = '_____________________________________________________________________________________', pad = ((0,0),(5,0)), font = ['Meiryo',10], text_color = '#bdbdbd')],

    [sg.Text(text = 'プリセット名', pad = ((0,22),(20,0)), font = ['Meiryo',10]),
     sg.Input(default_text = preset_name, size=(100,1), font = ['Meiryo',8], tooltip = 'プリセット名を入力してください', pad = ((0,0),(20,0)), key = '-preset_name-')],

    [sg.Text(text = '検索ワード(単語ごとに改行してください)', pad = ((0,0),(20,0)), font = ['Meiryo',10], justification = 'left'),
     sg.Text(text = 'NGワード(単語ごとに改行してください)', pad = ((100,0),(20,0)), font = ['Meiryo',10], justification = 'center')],

    [sg.Multiline(default_text = search_word, size = (39,5), font = ['Meiryo',10], key = '-search_word-'),
     sg.Multiline(default_text = nogood_word, size = (40,5), font = ['Meiryo',10], tooltip = 'NGワードに設定された単語が含まれているツイートを除外します', key = '-nogood_word-')],

    [sg.Radio(text = '検索開始時から投稿されたツイートのみ取得', font = ['Meiryo',10], pad = ((0,0),(20,0)), group_id = 0, default = since_auto_rb, enable_events = True, k = '-rb_01-'),
     sg.Radio(text = '指定した日時から投稿されたツイートのみ取得', font = ['Meiryo',10], pad = ((57,0),(20,0)), group_id = 0, default = since_specify_rb, enable_events = True, k = '-rb_02-')],

    [sg.Checkbox(text = 'リプライを除外', font = ['Meiryo',10], pad = ((0,0),(20,0)), default = reply_exclusion, key = '-reply_exclusion-'),
     sg.Text(text = '日付指定', pad = ((240,10),(20,0)), font = ['Meiryo',10]),
     sg.Input(default_text = specity_date, size=(30,1), font = ['Meiryo',8], tooltip = '指定された日時から最新のツイートを取得します', pad = ((0,0),(20,0)), readonly = True, key = '-calender_input-'),

     sg.CalendarButton('選択', title = '日付選択', target = '-calender_input-', no_titlebar = False, format = '20%y-%m-%d', default_date_m_d_y = (dt_now.month,dt_now.day,dt_now.year), close_when_date_chosen = True,
     month_names = ('1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'),
     day_abbreviations = ('月', '火', '水', '木', '金', '土', '日'), size = (5,1), font = ['Meiryo',8], pad = ((10,0),(20,0)), disabled = False, k = '-calender_button-')],

    [sg.Button(button_text = 'Tweetron 使用方法', font = ['Meiryo',8], size = (20,1), pad = ((0,0),(20,0)), k = '-wikipage_open-'),
     sg.Button(button_text = '検索コマンド設定', font = ['Meiryo',8], size = (20,1), pad = ((30,0),(20,0)), k = '-filter_setting-'),
     sg.Text(text = '時間指定', pad = ((33,10),(20,0)), font = ['Meiryo',10]),

     sg.Spin(values = time_h_list, initial_value = specity_h, font = ['Meiryo',10], pad = ((0,0),(20,0)), readonly = True, disabled = False, k = '-spin_h-'), sg.Text(text = '時', pad = ((10,0),(20,0)), font = ['Meiryo',10]),
     sg.Spin(values = time_m_list, initial_value = specity_m, font = ['Meiryo',10], pad = ((10,0),(20,0)), readonly = True, disabled = False, k = '-spin_m-'), sg.Text(text = '分', pad = ((10,0),(20,0)), font = ['Meiryo',10]),
     sg.Spin(values = time_s_list, initial_value = specity_s, font = ['Meiryo',10], pad = ((10,0),(20,0)), readonly = True, disabled = False, k = '-spin_s-'), sg.Text(text = '秒', pad = ((10,0),(20,0)), font = ['Meiryo',10]),

     sg.Button(button_text = '現在時刻', font = ['Meiryo',8], size = (12,1), pad = ((5,0),(20,0)), k = '-add_nowtime-')],

    [sg.Button(button_text = 'テキスト詳細設定', font = ['Meiryo',8], size = (20,1), pad = ((0,0),(20,0)), k = '-text_set-'),
     sg.Button(button_text = 'テキスト表示形式設定', font = ['Meiryo',8], size = (20,1), pad = ((30,0),(20,0)), k = '-display_set-'),
     sg.Button(button_text = 'プリセット保存', font = ['Meiryo',8], size = (20,1), pad = ((30,0),(20,0))),
     sg.Button(button_text = '実行', font = ['Meiryo',8], size = (20,1), pad = ((30,0),(20,0)))]

    ]

    return sg.Window(window_title, main_layout, icon = png_icon_path, size = (700,465), font = ['Meiryo',12], finalize = True)



def make_filterset_window(sg, window_title, png_icon_path, search_command):

    if search_command == 'null':
        search_command = ''

    filterset_layout = [

    [sg.Text(text = '検索コマンド', pad = ((0,0),(20,0))),
     sg.Input(default_text = search_command, size = (50,1), pad = ((15,0),(20,0)), tooltip = 'コマンドを入力してください', k = '-filter_input-')],

    [sg.Text(text = '公式が用意したコマンドを使用してツイート検索にフィルタを設定できます\n(※sinceコマンドは使用できません)\nコマンド一覧の引用元(https://yonoi.com/twitter-search-command/)',
     pad = ((0,0),(20,0)), font = ['Meiryo',8], text_color = '#808080'),
     sg.Button(button_text = 'コマンド一覧', font = ['Meiryo',8], size = (13,1), pad = ((17,0),(20,0)), key = '-command_list-')],

    [sg.Button(button_text = 'OK', font = ['Meiryo',8], size = (15,1), pad = ((100,15),(20,0)), key = 'Button_OK'),
     sg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (15,1), pad = ((45,0),(20,0)), key = 'Button_Cancel')]

     ]

    return sg.Window('検索コマンド設定', filterset_layout, icon = png_icon_path, size = (500,185), font = ['Meiryo',10])

def make_textset_window(sg, window_title, png_icon_path,
                        streamtext_font_size, streamtext_color, streamtext_font_name,
                        streamtext_font_path, fonts_list, font_name,
                        fontsize_list):

    if streamtext_font_path == 'null':
        streamtext_font_path = ''

    textset_layout = [

    [sg.Text(text = 'Sampleテキスト', pad = ((0,0),(20,0)), size = (50,1), font = [streamtext_font_name,streamtext_font_size], text_color = streamtext_color, auto_size_text = False, k = '-sample_text-')],

    [sg.Text(text = '_____________________________________________________________________________________', pad = ((0,0),(5,0)), font = ['Meiryo',10], text_color = '#bdbdbd')],

    [sg.Text(text = '実際に表示されるテキストと若干異なる場合があります\n下の[実際に確認する]を選択し、ブラウザで確認することをおすすめします', pad = ((0,0),(20,0)), font = ['Meiryo',8], text_color = '#808080')],

    [sg.Text(text = 'サンプルテキスト', pad = ((0,0),(20,0))), sg.Input(default_text = 'Sampleテキスト', size = (50,1), pad = ((15,0),(20,0)), tooltip = 'サンプルテキストを変更できます', enable_events = True, k = '-sample_text_input-')],

    [sg.Text(text = 'フォントサイズ', pad = ((0,0),(20,0))),
     sg.Spin(values = fontsize_list, initial_value = streamtext_font_size, pad = ((10,0),(20,0)), enable_events = True, k = '-fontsize_spin-'),
     sg.Text(text = 'テキストカラー', pad = ((10,0),(20,0))),
     sg.Input(default_text = streamtext_color, size = (22,1), pad = ((10,0),(20,0)), enable_events = True, tooltip = '16進数のカラーコードを指定できます\n( # から入力してください)', k = '-color_input-'),
     sg.ColorChooserButton(button_text = '選択', size = (5,1), pad = ((10,0),(20,0)), target = '-color_input-', k = '-cc_button-')],

    [sg.Text(text = 'フォントリスト', pad = ((0,0),(20,0)))],

    [sg.Text(text = '以下のリストから指定してもうまく反映されない場合があります\nその場合直接ttfファイルを読み込むことをおすすめします', pad = ((0,0),(0,0)), font = ['Meiryo',8], text_color = '#808080')],

    [sg.Input(default_text = streamtext_font_name, size = (60,1), pad = ((0,0),(5,5)), tooltip = 'フォント名を直接指定できます', enable_events = True, k = '-font_name_input-')],

    [sg.Listbox(fonts_list, size = (60,10), default_values = font_name, enable_events = True, highlight_background_color = '#4169e1', pad = ((0,0),(0,0)), key = '-font_list-')],

    [sg.Input(default_text = streamtext_font_path, size = (53,1), pad = ((0,0),(10,5)), tooltip = 'ttfフォントを指定できます', enable_events = True, k = '-font_path-'),
     sg.FileBrowse(button_text = '参照', target = "-font_path-", file_types=((".ttf file", "*.ttf"),), size = (5,1), pad = ((10,0),(10,5)))],

    [sg.Button(button_text = 'OK', font = ['Meiryo',8], size = (15,1), pad = ((10,15),(20,0)), key = 'Button_OK'),
     sg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (15,1), pad = ((45,0),(20,0)), key = 'Button_Cancel'),
     sg.Button(button_text = '実際に確認する', font = ['Meiryo',8], size = (15,1), pad = ((60,0),(20,0)), key = '-Verification-')]

    ]

    return sg.Window('テキスト詳細設定', textset_layout, icon = png_icon_path, size = (500,750), font = ['Meiryo',10], finalize = True)

def make_displayset_window(sg, window_title, png_icon_path,
                           streamtext_displaytype,
                           streamtext_scrollspeed_list,
                           streamtext_scrollspeed):

    rb_default = []
    if streamtext_displaytype == 1:
        rb_default = [True,False]
    else:
        rb_default = [False,True]

    displayset_layout = [

    [sg.Image(filename = 'data/img/ex_img_01.png', pad = ((0,0),(30,0)))],

    [sg.Radio(text = 'ツイートとユーザーネームを一行に表示する(従来の方式)', font = ['Meiryo',10], pad = ((0,0),(20,0)), group_id = 0, default = rb_default[0], enable_events = True, k = '-rb_01-')],

    [sg.Text(text = 'OBS-Twitter-Streamで使用されていた方式です\nツイートとユーザーネームを一行に合わせて表示します', pad = ((0,0),(20,0)), font = ['Meiryo',8], text_color = '#808080')],

    [sg.Text(text = '_____________________________________________________________________________________', pad = ((0,0),(15,0)), font = ['Meiryo',10], text_color = '#bdbdbd')],

    [sg.Image(filename = 'data/img/ex_img_02.png', pad = ((0,0),(30,0)))],

    [sg.Radio(text = 'ツイートとユーザーネームを分ける', font = ['Meiryo',10], pad = ((0,0),(20,0)), group_id = 0, default = rb_default[1], enable_events = True, k = '-rb_02-')],

    [sg.Text(text = 'ツイートとユーザーネームを上下に分けて表示します\nスクリーンネームだけでなくユーザーネームも表示できます\n(上下の間隔は設定できませんのでクロップ機能を使って分けて頂く必要があります)',
     pad = ((0,0),(20,0)), font = ['Meiryo',8], text_color = '#808080')],

    [sg.Text(text = 'テキストのスクロールスピード', pad = ((118,0),(30,0)), font = ['Meiryo',10]),
     sg.Spin(values = streamtext_scrollspeed_list, initial_value = streamtext_scrollspeed, pad = ((0,0),(30,0)), enable_events = True, readonly = True, k = '-scrollspeed_spin-'),
     sg.Text(text = '%', pad = ((0,0),(30,0)), font = ['Meiryo',10])],

    [sg.Button(button_text = 'OK', font = ['Meiryo',8], size = (15,1), pad = ((90,15),(35,0)), key = 'Button_OK'),
     sg.Button(button_text = 'Cancel', font = ['Meiryo',8], size = (15,1), pad = ((45,0),(35,0)), key = 'Button_Cancel')]

    ]

    return sg.Window('テキスト表示形式設定', displayset_layout, icon = png_icon_path, size = (500,550), font = ['Meiryo',10], finalize=True)
