import json, os, time, requests, re
from collections import defaultdict

TOKEN = os.environ["APIFY_TOKEN"]
ACTOR = "apidojo~tweet-scraper"

QUERIES = [
 # people SHOWING work on screen (their output is a screen recording)
 '("built this with" OR "made this with") (Cursor OR "Claude Code" OR Lovable OR v0 OR Bolt OR Windsurf OR Replit) filter:videos',
 '(#buildinpublic OR "building in public") (demo OR walkthrough OR "here is how") filter:videos',
 '("vibe coding" OR "vibe coded" OR "vibecoded") filter:videos',
 '("shipped" OR "just launched") (demo OR "quick demo" OR walkthrough) filter:videos min_faves:20',
 '("screen recording" OR screencast OR "screen record") (demo OR tutorial OR walkthrough) filter:videos',
 '("here is a quick demo" OR "quick demo of" OR "demo of what I built") filter:videos',
 '("dev log" OR devlog OR "build log") (app OR saas OR product) filter:videos',
 '("tutorial" OR "how I built") (saas OR app OR "side project") filter:videos min_faves:15',
 '("indie hacker" OR "indiehackers" OR "solo founder") demo filter:videos',
 '("product demo" OR "feature demo") (my OR our) filter:videos min_faves:10',
 '("course creator" OR "online course") (lesson OR module OR record) filter:videos',
 '("Claude Code" OR "Cursor") (workflow OR setup OR "my setup") filter:videos min_faves:25',
]

def run(q, maxi=60):
    url = f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items?token={TOKEN}&timeout=240"
    body = {"searchTerms":[q], "sort":"Top", "maxItems":maxi, "tweetLanguage":"en"}
    try:
        r = requests.post(url, json=body, timeout=280)
        if not r.ok:
            print(f"  ERR {r.status_code} {q[:45]}"); return []
        items = r.json()
        items = [i for i in items if i.get("id") and (i.get("text") or i.get("full_text"))]
        print(f"  {len(items):4d}  {q[:60]}")
        return items
    except Exception as e:
        print("  EXC", q[:45], e); return []

allt=[]
for q in QUERIES:
    allt += run(q)
    time.sleep(1)
json.dump(allt, open("creator_tweets.json","w"))
print("TOTAL tweets:", len(allt))
