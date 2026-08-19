import json, re
from collections import defaultdict
d=json.load(open("viral_x.json"))
by=defaultdict(lambda:{"t":[], "a":None})
for t in d:
    a=t.get("author") or {}; u=a.get("userName")
    if not u: continue
    by[u]["a"]=a; by[u]["t"].append(t)
BAD=re.compile(r'\b(onlyfans|casino|betting|sportsbook|nsfw|escort|airdrop|memecoin|presale|CA:|pump\.fun)\b',re.I)
rows=[]
for u,v in by.items():
    a=v["a"]; tw=v["t"]; f=a.get("followers") or 0
    if f<10000: continue
    bio=(a.get("description") or "")
    blob=bio+" "+" ".join((x.get("fullText") or x.get("text") or "") for x in tw)
    if BAD.search(blob): continue
    views=[x.get("viewCount") or 0 for x in tw]
    med=sorted(views)[len(views)//2] if views else 0
    if med<5000: continue
    eng=sum((x.get("likeCount") or 0)+(x.get("retweetCount") or 0)*3 for x in tw)/max(1,len(tw))
    qs=sorted(set((x.get("searchQuery") or "")[:34] for x in tw))
    rows.append({"handle":u,"name":a.get("name"),"followers":f,"bio":re.sub(r'\s+',' ',bio)[:150],
      "url":f"https://x.com/{u}","posts_found":len(tw),"median_views":med,"max_views":max(views),
      "avg_eng":round(eng),"ratio":round(med/max(1,f),2),
      "sample":re.sub(r'\s+',' ',(tw[0].get('fullText') or tw[0].get('text') or ''))[:170],
      "sample_url":tw[0].get("url") or tw[0].get("twitterUrl")})
rows.sort(key=lambda r:-r["median_views"])
json.dump(rows,open("x_creators.json","w"),indent=1)
print("X creators (10k+ followers, 5k+ median views):",len(rows))
print(f"\n{'handle':22s}{'followers':>10s}{'med views':>11s}{'max views':>11s}{'v/f':>6s}  bio")
for r in rows[:30]:
    print(f"@{r['handle'][:20]:21s}{r['followers']:>10,}{r['median_views']:>11,}{r['max_views']:>11,}{r['ratio']:>6.1f}  {r['bio'][:56]}")
