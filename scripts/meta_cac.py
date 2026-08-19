SPEND=10_000
CPI={"US":4.10,"Brazil":0.85,"India":0.42,"Philippines":0.60}
CPC={"US":1.20,"Brazil":0.35,"India":0.20,"Philippines":0.28}

# funnel rates
LOW  = dict(activate=.60, email=.20, click=.04, install=.25)
BASE = dict(activate=.60, email=.25, click=.06, install=.30)
HIGH = dict(activate=.70, email=.40, click=.15, install=.40)

def chain(n,r): return n*r["activate"]*r["email"]*r["click"]*r["install"]

print("FUNNEL A — Meta -> iOS APP install -> play -> email -> desktop")
print(f"$10,000 spend. Real 2026 casual-game iOS CPI.\n")
print(f"{'market':12s}{'CPI':>7s}{'app installs':>14s}{'desktop (low)':>15s}{'desktop (base)':>16s}{'desktop (high)':>16s}")
print("-"*82)
A={}
for m,cpi in CPI.items():
    n=SPEND/cpi
    A[m]=(n,chain(n,LOW),chain(n,BASE),chain(n,HIGH))
    print(f"{m:12s}{'$'+format(cpi,'.2f'):>7s}{n:>14,.0f}{A[m][1]:>15,.0f}{A[m][2]:>16,.0f}{A[m][3]:>16,.0f}")

print(f"\n{'market':12s}{'CAC per desktop install':>30s}")
print("-"*44)
for m in CPI:
    n,l,b,h=A[m]
    f=lambda x: '$'+format(SPEND/x,',.0f') if x>=1 else 'n/a'
    print(f"{m:12s}{f(h)+'  ..  '+f(b)+'  ..  '+f(l):>30s}")
print("   (high-case .. base .. low-case)")

print("\n\nFUNNEL B — Meta -> WEB game (no app install) -> email -> desktop")
print("Skips the CPI entirely. Cost is a click, not an install.\n")
print(f"{'market':12s}{'CPC':>7s}{'landing views':>15s}{'desktop (low)':>15s}{'desktop (base)':>16s}{'desktop (high)':>16s}")
print("-"*84)
B={}
for m,cpc in CPC.items():
    n=SPEND/cpc*0.8
    B[m]=(n,chain(n,LOW),chain(n,BASE),chain(n,HIGH))
    print(f"{m:12s}{'$'+format(cpc,'.2f'):>7s}{n:>15,.0f}{B[m][1]:>15,.0f}{B[m][2]:>16,.0f}{B[m][3]:>16,.0f}")

print(f"\n{'market':12s}{'CAC/desktop (base)':>22s}{'  vs app route':>16s}")
print("-"*52)
for m in CPI:
    cb=SPEND/B[m][2]; ca=SPEND/A[m][2]
    print(f"{m:12s}{'$'+format(cb,',.0f'):>22s}{'  '+format(ca/cb,'.1f')+'x cheaper':>16s}")

print("\n\nWHERE IT DIES")
r=BASE; n=1000
print(f"   1,000 app installs ->")
print(f"     {n*r['activate']:>7,.0f}  play a round        ({r['activate']:.0%})")
print(f"     {n*r['activate']*r['email']:>7,.0f}  give email          ({r['email']:.0%})")
print(f"     {n*r['activate']*r['email']*r['click']:>7,.1f}  click desktop link  ({r['click']:.0%})  <-- email CTR benchmark is 1-3%")
print(f"     {chain(n,r):>7,.1f}  install desktop     ({r['install']:.0%})")
print(f"\n   0.27% of app installs become desktop installs. The email step kills it.")
