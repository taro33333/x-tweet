import os
import requests
from requests_oauthlib import OAuth1

# --- 必要な環境変数を読み込み ---
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

POST_TEXT = "おはようございます☀️ 今日もコツコツやっていきましょう！ #エンジニア #朝活"

# --- OAuth1認証オブジェクト作成 ---
auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# --- 投稿処理 ---
def post_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}

    resp = requests.post(url, headers=headers, json=payload, auth=auth, timeout=30)

    if resp.status_code == 201:
        print("✅ 投稿成功:", resp.json())
    else:
        print("❌ 投稿失敗:", resp.text)
        resp.raise_for_status()

if __name__ == "__main__":
    try:
        post_tweet(POST_TEXT)
    except Exception as e:
        print("エラー:", e)
