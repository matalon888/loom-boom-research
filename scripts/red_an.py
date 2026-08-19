import json, re, html, sys, glob
from collections import Counter
rows=[]
for f in ["reddit2.json","reddit3.json"]:
    try: rows += json.load(open(f))
    except Exception: pass
seen={}
for r in rows:
    t = r.get('body') or r.get('title','')+'. '+(r.get('text') or '')
    t = html.unescape(re.sub(r'<[^>]+>',' ', t or '')).strip()
    t = re.sub(r'\s+',' ', t)
    if not t: continue
    seen[r.get('id') or r.get('url')] = {
        "sub": r.get('parsedCommunityName'), "url": r.get('url'),
        "type": r.get('dataType'), "score": r.get('upVotes') or r.get('score'),
        "date": (r.get('createdAt') or '')[:10], "text": t}
items=list(seen.values())
print("raw rows", len(rows), "unique", len(items))
LOOM = re.compile(r'\bloom\b', re.I)
NOISE = re.compile(r'(loom(ing|ed)\b|weav|textile|jacquard|hand ?loom|knitting|loom band|dark clouds|loom large)', re.I)
CTX = re.compile(r'(screen ?record|screencast|video|record|async|share.{0,15}link|demo|walkthrough|tutorial|saas|app|tool|extension|subscription|zoom|obs)', re.I)
rel=[]
for x in items:
    if not LOOM.search(x['text']): continue
    if NOISE.search(x['text']) and not CTX.search(x['text']): continue
    if not CTX.search(x['text']): continue
    rel.append(x)
print("loom-relevant", len(rel))
print(Counter(x['sub'] for x in rel).most_common(20))
json.dump(rel, open("reddit_rel.json","w"), indent=1)
