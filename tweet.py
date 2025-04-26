# post_to_x.py
import os
import requests
from requests_oauthlib import OAuth1
import time
import random

# --- 必要な環境変数を読み込み ---
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# --- 複数投稿用のツイートリスト ---
TWEETS = [
    """
ワラウの紹介です！

最大500円分のポイント
招待コードを使用していただけると嬉しいです

招待コード 8Ffx
#ワラウ #招待 #招待コード #クーポンコード
""",
    """
ファミペイの紹介です！

ファミペイアプリをダウンロードして、アプリ画面右下「サービス」内の「ギフトを受け取る」から下記のギフトコードを入力して、特典を受け取れます

ギフトコード 9qd0zk6675q426js8
#ファミペイ #招待 #紹介コード #ギフトコード
""",
    """
auじぶん銀行の紹介です！

もし良ければ、口座開設申込の際に、申込フォームの「紹介コード」入力欄に以下の紹介コードを入力して口座開設をして頂ければ嬉しいです。

紹介コード 8a62be18z0
#auじぶん銀行 #招待 #紹介コード
""",
    """
バンドルカードの紹介です！

双方に200円がカード残高にチャージされるため
良ければ「紹介コード」してアカウント開設していただけますと嬉しいです。

紹介コード ttxyd2
#バンドルカード #招待 #紹介コード
""",
    """
Uvoiceの紹介です！

アカウント開設して招待コードを入力、行動データ提供設定すると300ポイントもらえるため、クーポンコード使用して頂けますと嬉しいです。

クーポンコード Tz7gnPDuEg
#Uvoice #招待 #招待コード #クーポンコード
""",
    """
ちょびリッチ
ご家族・お友達紹介プログラム

※下記URLから登録していただけますと双方にポイントが付与されるため、使用していただけますと嬉しいです
https://chobirich.com/cm/ad/?p=8225208671&i=4984041

#ちょびリッチ #紹介 #招待コード
""",
    """
エアウォレットの紹介です！

良ければ「紹介コード」入力欄に以下の紹介コードを入力頂ければ嬉しいです。

紹介コード
xbqa8zt

#エアウォレット #招待 #紹介コード
"""
]

# --- OAuth1認証オブジェクト作成 ---
auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# --- ランダム絵文字リスト ---
EMOJIS = ["✨", "🌟", "🔥", "🎯", "💡", "🚀", "🎉", "📣", "🏆", "🥇", "✅", "🥳", "💥", "🛫", "🏖️", "🍀", "🎶", "📢", "⚡", "🎈", "🧩"]

# --- 投稿処理 ---
def post_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Content-Type": "application/json"}
    emoji = random.choice(EMOJIS)
    payload = {"text": f"{text.strip()} {emoji}"}

    resp = requests.post(url, headers=headers, json=payload, auth=auth, timeout=30)

    if resp.status_code == 201:
        print("✅ 投稿成功:", resp.json())
    else:
        print("❌ 投稿失敗:", resp.text)
        resp.raise_for_status()

if __name__ == "__main__":
    try:
        for idx, tweet in enumerate(TWEETS):
            post_tweet(tweet)
            if idx != len(TWEETS) - 1:
                print("次のツイートまで5秒待機...")
                time.sleep(5)  # 次のツイートまで少し待つ（API制限対策）
    except Exception as e:
        print("エラー:", e)
