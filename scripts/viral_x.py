import json, os, time, requests
TOKEN=os.environ["APIFY_TOKEN"]; ACTOR="apidojo~tweet-scraper"
Q=[
 # memory / brain-challenge format — the viral lane
 '("test your memory" OR "how good is your memory" OR "memory game") min_faves:200',
 '("can you beat" OR "can you spot" OR "beat my score") (game OR challenge OR puzzle) min_faves:300',
 '("brain teaser" OR "brain test" OR "iq test" OR "attention test") min_faves:500',
 '("only 1%" OR "99% fail" OR "most people cant") (spot OR remember OR find) min_faves:500',
 '("reply with your score" OR "comment your score" OR "what did you get") min_faves:200',
 # challenge/game creators with big reach
 '("i made a game" OR "built a game" OR "tiny game") min_faves:300 filter:videos',
 '("daily puzzle" OR "wordle" OR "connections" OR "puzzle game") min_faves:400',
 # big tech/creator accounts that post demos (top of funnel seeds)
 '("screen recording" OR "screen record" OR demo OR walkthrough) min_faves:400 filter:videos',
 '("vibe coding" OR "claude code" OR cursor) min_faves:500 filter:videos',
 '("build in public" OR "#buildinpublic") min_faves:300 filter:videos',
 # prize / earn hooks (Boom Match adjacency)
 '("cash prize" OR "win real money" OR "paid to play") (game OR app) min_faves:200',
]
out=[]
for q in Q:
    url=f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items?token={TOKEN}&timeout=240"
    try:
        r=requests.post(url,json={"searchTerms":[q],"sort":"Top","maxItems":70,"tweetLanguage":"en"},timeout=280)
        items=[i for i in r.json() if i.get("id")] if r.ok else []
        print(f"  {len(items):4d}  {q[:62]}",flush=True); out+=items
    except Exception as e: print("  EXC",q[:40],e,flush=True)
    time.sleep(1)
json.dump(out,open("viral_x.json","w")); print("TOTAL",len(out))
