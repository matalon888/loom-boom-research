VIEWS = 57_812_300
SPEND = 4550

S = {
 "pessimistic": dict(ctr=.002, play=.40, signup=.03, install=.005, active=.30, prem=.02, credit=.01, aov=8),
 "base":        dict(ctr=.005, play=.60, signup=.08, install=.020, active=.40, prem=.04, credit=.03, aov=12),
 "optimistic":  dict(ctr=.015, play=.75, signup=.15, install=.050, active=.50, prem=.08, credit=.08, aov=18),
}
rows=[]
for name,a in S.items():
    clicks  = VIEWS*a["ctr"]
    plays   = clicks*a["play"]
    signups = plays*a["signup"]
    installs= signups*a["install"]
    active  = installs*a["active"]
    prem    = active*a["prem"]
    buyers  = signups*a["credit"]
    rev     = buyers*a["aov"]
    rows.append((name,clicks,plays,signups,installs,active,prem,buyers,rev))

hdr=("scenario","clicks","plays","signups","desktop\ninstalls","active\nrecorders","premium\nsubs","credit\nbuyers","credit rev")
print(f"{'scenario':13s}{'clicks':>10s}{'plays':>10s}{'signups':>9s}{'installs':>10s}{'active':>9s}{'premium':>9s}{'buyers':>9s}{'credit $':>11s}")
print("-"*90)
for r in rows:
    print(f"{r[0]:13s}{r[1]:>10,.0f}{r[2]:>10,.0f}{r[3]:>9,.0f}{r[4]:>10,.0f}{r[5]:>9,.0f}{r[6]:>9,.0f}{r[7]:>9,.0f}{'$'+format(r[8],',.0f'):>11s}")

print(f"\nSPEND ${SPEND:,}  ·  cost per outcome")
print(f"{'scenario':13s}{'/active recorder':>20s}{'/premium sub':>16s}{'/credit buyer':>16s}{'credit ROI':>12s}")
print("-"*80)
for r in rows:
    cpa = SPEND/r[5] if r[5]>=1 else None
    cps = SPEND/r[6] if r[6]>=1 else None
    cpb = SPEND/r[7] if r[7]>=1 else None
    roi = r[8]/SPEND
    print(f"{r[0]:13s}{('$'+format(cpa,',.0f')) if cpa else 'n/a':>20s}{('$'+format(cps,',.0f')) if cps else 'n/a':>16s}{('$'+format(cpb,',.2f')) if cpb else 'n/a':>16s}{roi:>11.2f}x")

print("\nBENCHMARK: Google implied cost per paying customer = $1,335")
