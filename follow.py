import os
import random
import time
import requests
from requests_oauthlib import OAuth1

# --- 認証情報 ---
API_KEY            = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY     = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN       = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET= os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
USER_ID            = os.getenv("TWITTER_USER_ID")

auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# --- ランダム検索ワード ---
KEYWORDS = ["相互", "相互フォロー", "お得", "歓迎", "ポイ活"]

# --- 何人フォローするか・待ち時間 ---
NUM_FOLLOWS  = 5
DELAY_RANGE  = (3, 8)

def search_users(keyword: str) -> list[str]:
    """キーワードで直近ツイートを検索し、著者 ID を抽出して返す"""
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        "query": keyword,
        "max_results": 10,
        "tweet.fields": "author_id"
    }
    resp = requests.get(url, params=params, auth=auth, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return list({tweet["author_id"] for tweet in data.get("data", [])})

def follow_user(target_user_id: str) -> None:
    """指定ユーザーをフォロー"""
    url     = f"https://api.twitter.com/2/users/{USER_ID}/following"
    payload = {"target_user_id": target_user_id}
    resp    = requests.post(url, json=payload, auth=auth, timeout=30)

    if resp.status_code == 200:
        print(f"✅ フォロー成功: {target_user_id}")
    else:
        print(f"❌ フォロー失敗: {resp.text}")
        resp.raise_for_status()

if __name__ == "__main__":
    followed_ids: set[str] = set()   # この実行中にフォロー済みの ID

    for i in range(NUM_FOLLOWS):
        try:
            keyword = random.choice(KEYWORDS)
            print(f"\n🔍 {i+1}/{NUM_FOLLOWS} 回目 — 検索キーワード: {keyword}")

            # 候補取得
            candidates = search_users(keyword)
            # 重複・自分自身を除外
            candidates = [
                uid for uid in candidates
                if uid not in followed_ids and uid != USER_ID
            ]

            if not candidates:
                print("候補が見つかりませんでした。スキップします。")
                continue

            target = random.choice(candidates)
            follow_user(target)
            followed_ids.add(target)

            if i < NUM_FOLLOWS - 1:
                sleep_sec = random.randint(*DELAY_RANGE)
                print(f"⏸ {sleep_sec} 秒待機…")
                time.sleep(sleep_sec)

        except Exception as e:
            # 1 回失敗してもループ継続
            print("⚠️ エラー:", e)
