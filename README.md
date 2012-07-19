FUJI-ROCK-Ticket-Clowler
========================

FUJI ROCKの３日通し券チケットを買い逃したため、twitterで募集が出てないかチェックするプログラムです。

基本的には、Search APIを延々と投げ続けます。  
Stream APIだと日本語検索に何があるので苦肉の策です…  
デフォルトでは以下の２つのワードを検索対象としています。

1. フジ 通し OR フジ ３日 -RT
2. fuji 通し -RT

"fuji 通し OR fuji ３日 -RT"で検索すると何故か結果が少なくなったので、省いています。

使い方
------
コマンドライン引数に応じてメールを送信します。

    # クロールのみ（メール送信なし）
    python search.py
    # 未実装；メール送信（標準）
    python search.py -d [send_addr]
    # メール送信（Gmail経由）
    python search.py -d [send_addr] -u [gmail_user] -p [gmail_pass]
    

動作環境
--------
以下のパッケージが必要です。

+ tweepy

    pip install tweepy

動作はMac OSX Lion、python2.7.3で確認しています。
その他のバージョンだと、パッケージが古かったりして動かないかもしれません。
