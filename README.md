FUJI-ROCK-Ticket-Clowler
========================

FUJI ROCKの３日通し券チケットを買い逃したため、twitterで募集が出てないかチェックするプログラムです。

基本的には、Search APIを延々と投げ続けます。  
Stream APIだと日本語検索に何があるので苦肉の策です…  
デフォルトでは以下の２つのワードを検索対象としています。

1. (フジ OR fuji) AND (ゆず OR 譲 OR あま OR 余 OR チケ OR ３日 OR 3日 OR 通し)

後半はTwitter Search APIに投げているのではなく、python内でマッチングを見ています。
なのでAPIからもらってくるデータは、「フジ」もしくは「fuji」が含まれるつぶやきを全部もらってきます。
ちなみに、RTから始まるものは除外しています。
数がえらいことになるので…

ほかに良い検索ワードとかあれば教えて下さい。


使い方
------
コマンドライン引数に応じてメールを送信します。

    # クロールのみ（メール送信なし）
    python search.py
    # 未実装；メール送信（標準）
    python search.py -d [send_addr]
    # メール送信（Gmail経由）
    python search.py -d [send_addr] -u [gmail_user] -p [gmail_pass]
    
    # Twitterのリプライ定型文
    python search.py -t チケットくださいな！
    
    # 新しいTweetが見つかったらブラウザで開く
    python search.py -b

動作環境
--------
以下のパッケージが必要です。

+ tweepy

    pip install tweepy

動作はMac OSX Lion、python2.7.3で確認しています。
その他のバージョンだと、パッケージが古かったりして動かないかもしれません。
