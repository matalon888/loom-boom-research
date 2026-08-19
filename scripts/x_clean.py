import json, re
rows=json.load(open("x_creators.json"))
OFF=re.compile(r'\b(politic|woke|conservative|liberal|maga|trump|biden|patriot|christ first|news|celebrit|entertainment|nfl|nba|football|soccer|anime|pokemon|genshin|artist|cartoonist|journalist|history|military|veteran|radio|music|singer|rapper|producer|pump|memecoin|token|airdrop|decentraliz|xmoney|trade internet)\b',re.I)
ON=re.compile(r'\b(game|games|gaming|puzzle|quiz|trivia|brain|app|apps|indie|build|builder|founder|dev|developer|engineer|design|saas|maker|creator|tech|ai\b|startup|viral|product|code|coding|no.?code|automation|tool)\b',re.I)
keep=[]
for r in rows:
    blob=(r["bio"] or "")+" "+(r["sample"] or "")
    if OFF.search(r["bio"] or ""): continue
    if not ON.search(blob): continue
    if r["followers"]>5_000_000: continue          # unreachable
    keep.append(r)
# score: viral efficiency (views per follower) x reach, favouring reachable accounts
for r in keep:
    r["viral_score"]=round((r["median_views"]**0.55)*(min(r["ratio"],400)**0.35)/100,1)
keep.sort(key=lambda r:-r["viral_score"])
for i,r in enumerate(keep,1): r["rank"]=i
json.dump(keep,open("x_top.json","w"),indent=1)
print("relevant X creators:",len(keep))
print(f"\n{'#':>3} {'handle':22s}{'followers':>10s}{'med views':>11s}{'v/f':>7s}  bio")
for r in keep[:32]:
    print(f"{r['rank']:>3} @{r['handle'][:20]:21s}{r['followers']:>10,}{r['median_views']:>11,}{r['ratio']:>7.1f}  {r['bio'][:58]}")
