def main_menu():

    files = [
        'ファイル(&F)',
        [
            'プリセット登録 (&N)::new_preset::',
            'プリセット削除 (&D)::delete_preset::',
            'プリセット保存 (&S)::save_preset::',
            '---',
            '終了 (&X)::app_exit::'
        ]
    ]

    edits = [
        '編集(&E)',
        [
            'テキスト詳細設定 (&F)::text_setting::',
            'テキスト表示形式設定 (&G)::text_display::',
            '検索コマンド設定 (&H)::search_command::',
            #'---',
            #'環境設定 (&J)::global_setting::'
        ]
    ]

    helps = [
        'ヘルプ(&H)',
        [
            'Tweetron ユーザーマニュアル (&M)::user_manual::',
            'バージョン情報 (&I)::version_info::'
        ]
    ]

    menu_layout = [files, edits, helps]

    return menu_layout
