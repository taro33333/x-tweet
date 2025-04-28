import os
import random
import requests
from requests_oauthlib import OAuth1

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
USER_ID = os.getenv("TWITTER_USER_ID")

auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# --- ランダム検索ワード
KEYWORDS = ["相互", "相互フォロー", "お得", "歓迎", "ポイ活"]

def search_users(keyword):
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Content-Type": "application/json"}
    params = {
        "query": keyword,
        "max_results": 10,
        "tweet.fields": "author_id"
    }
    resp = requests.get(url, headers=headers, params=params, auth=auth, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    user_ids = list({tweet["author_id"] for tweet in data.get("data", [])})
    return user_ids

def follow_user(target_user_id):
    url = f"https://api.twitter.com/2/users/{USER_ID}/following"
    headers = {"Content-Type": "application/json"}
    payload = {"target_user_id": target_user_id}
    resp = requests.post(url, headers=headers, json=payload, auth=auth, timeout=30)
    if resp.status_code == 200:
        print(f"✅ フォロー成功: {target_user_id}")
    else:
        print(f"❌ フォロー失敗: {resp.text}")
        resp.raise_for_status()

if __name__ == "__main__":
    try:
        keyword = random.choice(KEYWORDS)
        print(f"🔍 キーワード検索: {keyword}")
        candidates = search_users(keyword)
        if not candidates:
            print("候補者が見つかりませんでした。")
        else:
            target = random.choice(candidates)
            print(f"🎯 選ばれたユーザーID: {target}")
            follow_user(target)
    except Exception as e:
        print("エラー:", e)
