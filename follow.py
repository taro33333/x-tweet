import os, random, time, requests
from requests_oauthlib import OAuth1

API_KEY            = os.getenv("TWITTER_API_KEY")
API_SECRET_KEY     = os.getenv("TWITTER_API_SECRET_KEY")
ACCESS_TOKEN       = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET= os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
USER_ID            = os.getenv("TWITTER_USER_ID")

auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

KEYWORDS     = ["相互", "相互フォロー", "お得", "歓迎", "ポイ活"]
NUM_FOLLOWS  = 5
DELAY_RANGE  = (3, 8)          # フォロー間の待機
MAX_RESULTS  = 100             # 検索で返してほしいツイート数

def search_users(keyword: str) -> list[str]:
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        "query": keyword,
        "max_results": MAX_RESULTS,
        "tweet.fields": "author_id"
    }
    resp = requests.get(url, params=params, auth=auth, timeout=30)
    if resp.status_code == 429:
        reset = int(resp.headers.get("x-rate-limit-reset", time.time()+900))
        wait  = max(reset - int(time.time()), 0) + 2   # ちょい余裕
        print(f"🔒 Rate-limit hit. {wait} 秒待機してリトライ…")
        time.sleep(wait)
        return search_users(keyword)                   # 1 回だけ再帰リトライ
    resp.raise_for_status()
    data = resp.json()
    return list({t["author_id"] for t in data.get("data", [])})

def follow_user(target_id: str) -> None:
    url     = f"https://api.twitter.com/2/users/{USER_ID}/following"
    payload = {"target_user_id": target_id}
    resp    = requests.post(url, json=payload, auth=auth, timeout=30)
    if resp.status_code == 200:
        print(f"✅ フォロー成功: {target_id}")
    else:
        print(f"❌ フォロー失敗: {resp.text}")

if __name__ == "__main__":
    keyword    = random.choice(KEYWORDS)
    print(f"🔍 検索キーワード: {keyword}")
    candidates = search_users(keyword)

    # 自分や重複を除外
    candidates = [uid for uid in candidates if uid != USER_ID]
    random.shuffle(candidates)

    if not candidates:
        print("候補が見つかりませんでした。終了します。")
        exit(0)

    for i, target in enumerate(candidates[:NUM_FOLLOWS], 1):
        follow_user(target)
        if i < NUM_FOLLOWS:
            sleep_sec = random.randint(*DELAY_RANGE)
            print(f"⏸ {sleep_sec} 秒待機…")
            time.sleep(sleep_sec)
