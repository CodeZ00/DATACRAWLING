# -*- coding: utf-8 -*-
import json
import urllib.parse
import urllib.request

def test_search():
    query = "오창읍"
    encoded_q = urllib.parse.quote(query)
    url = f"https://apis.zigbang.com/v2/search?leaseYn=N&q={encoded_q}&serviceType=%EC%9B%90%EB%A3%B8"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        print("Search error:", e)

if __name__ == "__main__":
    test_search()
