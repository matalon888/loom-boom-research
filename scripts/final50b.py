import json, re
rows = json.load(open("creators_ranked.json"))
BLOCK = re.compile(r'\b(dao|token|airdrop|web3|nft|defi|presale|memecoin|prediction market|xbt|blockchain|staking|crypto|@base\b|ourbit|exchange|trading|CA:|\$[A-Z]{3,6}\b)\b', re.I)
GOOD  = re.compile(r'\b(build|builder|founder|dev\b|developer|engineer|design|indie|saas|maker|creator|teach|teaching|tutorial|course|automat|product|startup|no.?code|coding|code|ship|app)\b', re.I)
BLOCKED_HANDLES = {"RoundtableSpace","prediction_xbt","0xyoussea","zodchiii","mikenevermiss","galileoprotocol","SagaDaoAlpha","magnetaixyz"}

keep=[]
for r in rows:
    if r["handle"] in BLOCKED_HANDLES: continue
    blob=(r["bio"] or "")+" "+(r["sample"] or "")+" "+r["handle"]
    if BLOCK.search(blob): continue
    if not (r["bio"] or "").strip(): continue
    if not r["tools"] and not GOOD.search(r["bio"]): continue
    keep.append(r)

L=[r for r in keep if r["followers"]>=50000]
M=[r for r in keep if 10000<=r["followers"]<50000]
S=[r for r in keep if r["followers"]<10000]
final = L[:12]+M[:20]+S[:18]
final.sort(key=lambda r:-r["followers"])
for i,r in enumerate(final,1): r["rank"]=i
json.dump(final, open("final50.json","w"), indent=2)
print("clean pool:",len(keep),"| L",len(L),"M",len(M),"S",len(S),"| FINAL",len(final))
tot=sum(r["followers"] for r in final)
print(f"combined reach: {tot:,}  |  median followers: {sorted(r['followers'] for r in final)[len(final)//2]:,}")
for r in final: print(f"{r['rank']:>3} @{r['handle'][:20]:21s}{r['followers']:>9,}{r['avg_eng']:>7,}  {r['bio'][:78]}")
