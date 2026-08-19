import json
d=json.load(open("final50.json"))
HAIRCUT=0.40      # scrape used "Top" sort -> observed posts are best-case
CAP_MULT=8        # no creator credited with more than 8x followers in views

def rate(f):
    base = 8 if f<10000 else (10 if f<50000 else 12)
    return max(60, min((f/1000.0)*base*1.4, 2500))

rows=[]
for x in d:
    f=x["followers"]; posts=max(1,x["posts_found"]); views=x.get("views") or 0
    raw = views/posts
    if raw < 100: raw = f*0.12
    vpp = min(raw*HAIRCUT, f*CAP_MULT)
    c = rate(f)
    rows.append({**x,"cost":round(c),"views_per_post":round(vpp),"cpm":round(c/(vpp/1000),2) if vpp else None})
rows.sort(key=lambda r:r["cpm"])
for i,r in enumerate(rows,1): r["value_rank"]=i
json.dump(rows,open("budget50.json","w"),indent=1)

def pack(n):
    p=rows[:n]; c=sum(x["cost"] for x in p); v=sum(x["views_per_post"] for x in p)
    return p,c,v
print("PACKS (ranked by cost-efficiency, after 40% haircut + 8x-followers cap)\n")
print(f"{'pack':>10}{'creators':>10}{'cost':>10}{'est views':>13}{'CPM':>8}")
for n in (10,20,35,50):
    p,c,v=pack(n)
    print(f"{'top-'+str(n):>10}{n:>10}{'$'+format(c,','):>10}{v:>13,}{'$'+format(c/(v/1000),'.2f'):>8}")

p,c,v=pack(20)
print(f"\n=== BREAK-EVEN on the top-20 pack: ${c:,} buying ~{v:,} views ===")
print("Revenue needed per paying user for the pack to wash its face:\n")
print(f"{'CTR':>7}{'visits':>9}{'signups':>9}" + "".join(f"{'pay '+str(int(cv*100))+'%':>10}" for cv in (0.02,0.05,0.10)))
for ctr in (0.005,0.01,0.02):
    visits=v*ctr; su=visits*0.25
    line=f"{ctr*100:>6.1f}%{visits:>9,.0f}{su:>9,.0f}"
    for cv in (0.02,0.05,0.10):
        payers=su*cv
        line+=f"{'$'+format(c/payers,'.2f'):>10}" if payers>=1 else f"{'—':>10}"
    print(line)
print("\ntop-20 roster:")
for r in rows[:20]:
    print(f"  {r['value_rank']:>2} @{r['handle'][:20]:21s}{r['followers']:>9,}{r['views_per_post']:>10,}{'$'+str(r['cost']):>8}{'$'+format(r['cpm'],'.2f'):>9}")
