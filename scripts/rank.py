import json, re
from collections import defaultdict

d = json.load(open("creator_tweets.json"))
by = defaultdict(lambda: {"tw":[], "a":None})
for t in d:
    a = t.get("author") or {}
    u = a.get("userName")
    if not u: continue
    by[u]["a"] = a
    by[u]["tw"].append(t)

# signals that this person's OUTPUT is a screen recording
TOOL   = re.compile(r'\b(cursor|claude code|lovable|v0\b|bolt\.new|bolt\b|windsurf|replit|copilot|codex|antigravity|n8n|supabase|vercel|figma|notion)\b', re.I)
DEMO   = re.compile(r'\b(demo|walkthrough|screencast|screen record|screen recording|tutorial|devlog|dev log|build log|how i built|watch me|breakdown|step by step|showing you|here.s how)\b', re.I)
BUILD  = re.compile(r'\b(built|building|shipped|launch|launched|side project|indie|solo founder|saas|#buildinpublic|building in public|vibe cod)\b', re.I)
BAD    = re.compile(r'\b(onlyfans|casino|betting|nsfw|crypto pump|airdrop|forex|giveaway.*retweet|follow.*for.*follow)\b', re.I)

rows=[]
for u, v in by.items():
    a=v["a"]; tws=v["tw"]
    f = a.get("followers") or 0
    if f < 800 or f > 400000: continue          # real audience, not a mega-account we can't reach
    txt = " ".join((t.get("fullText") or t.get("text") or "") for t in tws)
    bio = a.get("description") or ""
    blob = txt + " " + bio
    if BAD.search(blob): continue
    vids = sum(1 for t in tws if t.get("media") or t.get("extendedEntities"))
    if vids == 0: continue                       # must actually post video
    eng = sum((t.get("likeCount") or 0)+(t.get("retweetCount") or 0)*2 for t in tws)
    views = sum(t.get("viewCount") or 0 for t in tws)
    s_tool = len(set(m.lower() for m in TOOL.findall(blob)))
    s_demo = len(DEMO.findall(blob))
    s_build= len(BEV:=BUILD.findall(blob))
    # engagement rate matters more than raw followers for recruitment
    er = (eng / max(1,len(tws))) / max(1,f) * 1000
    score = (min(s_tool,4)*10) + (min(s_demo,6)*7) + (min(s_build,6)*4) + min(er*6, 40) + min(vids,5)*3
    rows.append({
      "handle":u, "name":a.get("name"), "followers":f, "verified":bool(a.get("isBlueVerified")),
      "bio":re.sub(r'\s+',' ',bio)[:190], "posts_found":len(tws), "videos":vids,
      "avg_eng":round(eng/max(1,len(tws))), "views":views,
      "tools":sorted(set(m.lower() for m in TOOL.findall(blob)))[:6],
      "score":round(score,1),
      "url":f"https://x.com/{u}",
      "sample":re.sub(r'\s+',' ',(tws[0].get('fullText') or tws[0].get('text') or ''))[:230],
      "sample_url":tws[0].get("url") or tws[0].get("twitterUrl"),
    })
rows.sort(key=lambda r:-r["score"])
json.dump(rows, open("creators_ranked.json","w"), indent=1)
print("qualified creators:", len(rows))
print(f"\n{'#':>3} {'handle':22s}{'followers':>10s}{'avgEng':>8s}{'score':>7s}  tools")
for i,r in enumerate(rows[:60],1):
    print(f"{i:>3} @{r['handle'][:20]:21s}{r['followers']:>10,}{r['avg_eng']:>8,}{r['score']:>7.1f}  {','.join(r['tools'][:3])}")
