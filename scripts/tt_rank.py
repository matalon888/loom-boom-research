import json, re
from collections import defaultdict
d=json.load(open("viral_tt.json"))
by=defaultdict(lambda:{"v":[], "a":None})
for t in d:
    a=t.get("authorMeta") or {}
    n=a.get("name")
    if not n: continue
    by[n]["a"]=a; by[n]["v"].append(t)

BAD=re.compile(r'\b(onlyfans|casino|betting|gambl|sportsbook|nsfw|18\+|escort)\b',re.I)
rows=[]
for n,v in by.items():
    a=v["a"]; vids=v["v"]
    fans=a.get("fans") or 0
    if fans<3000: continue
    bio=(a.get("signature") or "")
    if BAD.search(bio+" "+" ".join(x.get("text","") for x in vids)): continue
    plays=[x.get("playCount") or 0 for x in vids]
    med=sorted(plays)[len(plays)//2]
    eng=sum((x.get("diggCount") or 0)+(x.get("commentCount") or 0)*3+(x.get("shareCount") or 0)*5 for x in vids)/max(1,len(vids))
    er=eng/max(1,med)*100
    qs=sorted(set(x.get("searchQuery") or "" for x in vids))
    rows.append({"handle":n,"nick":a.get("nickName"),"fans":fans,"videos_total":a.get("video"),
        "hearts":a.get("heart"),"verified":bool(a.get("verified")),
        "bio":re.sub(r'\s+',' ',bio)[:150],"url":a.get("profileUrl") or f"https://www.tiktok.com/@{n}",
        "posts_found":len(vids),"median_plays":med,"max_plays":max(plays),"avg_eng":round(eng),
        "er":round(er,1),"queries":qs,
        "sample":re.sub(r'\s+',' ',vids[0].get("text",""))[:170],
        "sample_url":vids[0].get("webVideoUrl")})
rows.sort(key=lambda r:-r["median_plays"])
json.dump(rows,open("tt_creators.json","w"),indent=1)
print("TikTok creators (3k+ fans):",len(rows))
print(f"\n{'handle':24s}{'fans':>10s}{'med plays':>11s}{'max plays':>11s}{'ER%':>7s}  niche")
for r in rows[:35]:
    print(f"@{r['handle'][:22]:23s}{r['fans']:>10,}{r['median_plays']:>11,}{r['max_plays']:>11,}{r['er']:>7.1f}  {(r['queries'][0] if r['queries'] else '')[:26]}")
