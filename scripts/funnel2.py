VIEWS=57_812_300; SPEND=4550
def run(ctr,play,signup,install,active,prem,credit,aov,dau_days=0):
    c=VIEWS*ctr; p=c*play; s=p*signup; i=s*install; a=i*active; pr=a*prem
    b=s*credit; rev=b*aov
    return dict(clicks=c,plays=p,signups=s,installs=i,active=a,prem=pr,buyers=b,rev=rev)

print("STEP 4 IS THE LEVER — everything else held at base case\n")
print(f"{'desktop install rate':>22s}{'installs':>10s}{'active recorders':>18s}{'$/active':>10s}{'premium':>9s}{'$/premium':>11s}")
print("-"*82)
for ins,label in [(.005,'0.5%  (pessimistic)'),(.02,'2%  (base, "install our recorder")'),
                  (.06,'6%  (with the work-break pitch)'),(.10,'10%  (if it really lands)')]:
    r=run(.005,.60,.08,ins,.40,.04,.03,12)
    cpa=SPEND/r['active'] if r['active']>=1 else None
    cps=SPEND/r['prem'] if r['prem']>=1 else None
    print(f"{label:>22s}{r['installs']:>10,.0f}{r['active']:>18,.0f}"
          f"{('$'+format(cpa,',.0f')) if cpa else 'n/a':>10s}{r['prem']:>9,.0f}{('$'+format(cps,',.0f')) if cps else 'n/a':>11s}")

print("\n\nWHAT THE WORK-BREAK FRAME CHANGES — base vs reframed\n")
base=run(.005,.60,.08,.02,.40,.04,.03,12)
new =run(.005,.60,.08,.06,.55,.04,.03,12)   # higher install AND higher active: a daily game retains better than a weekly recorder
for k,lab in [('installs','desktop installs'),('active','active on desktop'),('prem','premium subs')]:
    print(f"  {lab:22s}{base[k]:>10,.0f}  ->{new[k]:>10,.0f}   ({new[k]/base[k]:.1f}x)")
print(f"  {'cost per active':22s}{'$'+format(SPEND/base['active'],',.0f'):>10s}  ->{'$'+format(SPEND/new['active'],',.0f'):>10s}")

print("\n\nRETENTION: what a daily game is worth vs a weekly recorder")
for label,sessions in [("screen recorder alone","~4 sessions/month"),("+ work-break game","~20 sessions/month")]:
    print(f"  {label:24s}{sessions}")
print("\n  ad impressions on free tier scale with sessions, not signups —")
print("  5x sessions is ~5x free-tier ad revenue from the same user.")
