print("=== A. BUILD (one-time) ===")
build=[("Tier 0 web game — curated board, score, share",3),
       ("Mobile app tier 1 — photo picker + on-device play",5),
       ("Email / desktop bridge",1),
       ("Anti-fraud port from Boom Match",2),
       ("Tracked links, attribution, analytics",1)]
tot=sum(w for _,w in build)
for n,w in build: print(f"   {w:>2} dev-weeks   {n}")
print(f"   {'-'*60}\n   {tot:>2} dev-weeks total  = {tot/4:.0f} dev-months  = ~{tot/2:.0f} calendar weeks with 2 devs")
for rate,lab in [(6000,"lean / PT rates"),(9000,"senior / PT rates"),(14000,"US contract")]:
    print(f"      at ${rate:,}/dev-month  ->  ${tot/4*rate:,.0f}")

print("\n\n=== B. MEDIA — same 57.8M impressions, four ways ===")
IMPR=57_812_300
opts=[("TikTok creators (10, the wave-1 pack)",0.08),
      ("Meta — India",1.36),("Meta — Philippines",3.40),("Meta — Brazil",4.20),
      ("Meta — emerging avg",8.00),("Meta — US",20.48)]
print(f"{'channel':38s}{'CPM':>8s}{'cost for 57.8M impressions':>28s}")
print("-"*76)
for n,cpm in opts:
    print(f"{n:38s}{'$'+format(cpm,'.2f'):>8s}{'$'+format(IMPR/1000*cpm,',.0f'):>28s}")
print(f"\n   creators are {20.48/0.08:,.0f}x cheaper per impression than Meta US,")
print(f"   and {1.36/0.08:.0f}x cheaper than the cheapest Meta market.")

print("\n\n=== C. INFRASTRUCTURE — the cost nobody has mentioned ===")
signups=100_000; rec_share=.30; recs_pm=4; mb=150; views_per=3
recorders=signups*rec_share
recs=recorders*recs_pm
store_tb=recs*mb/1_000_000
egress_tb=recs*views_per*mb/1_000_000
print(f"   assume {signups:,} signups, {rec_share:.0%} ever record, {recs_pm} recordings/mo, {mb}MB each, watched {views_per}x")
print(f"   -> {recorders:,.0f} recorders, {recs:,.0f} recordings/mo")
print(f"   -> storage ADDED  {store_tb:,.1f} TB/month")
print(f"   -> egress         {egress_tb:,.1f} TB/month\n")
print(f"{'provider':28s}{'$/GB egress':>13s}{'egress/mo':>13s}{'storage mo6':>14s}{'total mo6':>12s}")
print("-"*82)
for prov,eg,st in [("Cloudflare R2",0.000,0.015),("Bunny (volume)",0.005,0.010),
                   ("Bunny (standard)",0.010,0.010),("AWS CloudFront + S3",0.085,0.023)]:
    e=egress_tb*1000*eg
    s6=store_tb*6*1000*st
    print(f"{prov:28s}{'$'+format(eg,'.3f'):>13s}{'$'+format(e,',.0f'):>13s}{'$'+format(s6,',.0f'):>14s}{'$'+format(e+s6,',.0f'):>12s}")
print("\n   CloudFront vs R2 at this scale: the difference is a full-time engineer's salary.")

print("\n\n=== D. TOTAL — first 6 months, mobile approach ===")
print(f"{'line':46s}{'low':>13s}{'high':>13s}")
print("-"*74)
rows=[("Build (12 dev-weeks)",18000,42000),
      ("TikTok creator waves 1+3 (media)",4550,19812),
      ("Meta test budget (cheap markets, 3 mo)",3000,15000),
      ("CDN + storage, 6 months",3200,33000),
      ("Transcoding / encoding",600,3000),
      ("Affiliate bounties (variable, paid on revenue)",0,8000),
      ("Prize pool (you set this)",0,0)]
lo=hi=0
for n,a,b in rows:
    lo+=a; hi+=b
    print(f"{n:46s}{'$'+format(a,',.0f'):>13s}{'$'+format(b,',.0f'):>13s}")
print("-"*74)
print(f"{'TOTAL, 6 months':46s}{'$'+format(lo,',.0f'):>13s}{'$'+format(hi,',.0f'):>13s}")
print("\n   Prize pool excluded — it is your lever, not a cost I can estimate.")
