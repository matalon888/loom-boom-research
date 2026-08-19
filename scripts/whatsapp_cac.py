SPEND=10_000
ILS_USD=3.65
# From Daniel's OWN Recepte CTWA campaign, 2026-07-06: 105 ILS -> 107 conversations
cpc_ils = 105/107
CPCONV = cpc_ils/ILS_USD
print(f"YOUR OWN DATA — Recepte CTWA, 6 Jul 2026: 105 ILS spend -> 107 conversations")
print(f"  = {cpc_ils:.2f} ILS per conversation = ${CPCONV:.2f} per WhatsApp conversation\n")
print("  (that was small-business-owner targeting in Brazil for a receptionist product.")
print("   a memory game to a broad consumer audience should be cheaper, not dearer.)\n")

print("="*84)
print("CHANNEL COMPARISON — click-through on the 'go to desktop' message\n")
print(f"{'channel':28s}{'CTR':>14s}{'cost to send':>18s}{'notes':>22s}")
print("-"*84)
for n,ctr,cost,note in [
  ("Email",".01 - .03","free","benchmark 1-3%"),
  ("SMS",".01 - .06","$0.01-0.05/msg","barely beats email, costs money"),
  ("Push notification",".02 - .07","free","needs app install first (CPI)"),
  ("WhatsApp + buttons",".45 - .60","free in 72h window","Forrester/Infobip, 11,400 campaigns")]:
    print(f"{n:28s}{ctr:>14s}{cost:>18s}{note:>22s}")
print("\n  WhatsApp with interactive buttons: median CTR 58.3% across 11,400 campaigns.")
print("  Messages inside the 72-hour Click-to-WhatsApp window cost NOTHING.\n")

print("="*84)
print(f"FUNNEL — Click-to-WhatsApp -> game -> desktop.  ${SPEND:,} spend\n")
convs = SPEND/CPCONV
print(f"{'scenario':14s}{'convos':>10s}{'play':>10s}{'click desktop':>15s}{'install':>10s}{'CAC/desktop':>14s}")
print("-"*74)
for lab,play,click,inst in [("conservative",.40,.30,.20),("base",.60,.45,.30),("optimistic",.75,.58,.40)]:
    p=convs*play; c=p*click; i=c*inst
    print(f"{lab:14s}{convs:>10,.0f}{p:>10,.0f}{c:>15,.0f}{i:>10,.0f}{'$'+format(SPEND/i,',.2f'):>14s}")

print("\n" + "="*84)
print("VERSUS THE EMAIL ROUTE I GAVE YOU LAST TIME\n")
print(f"{'route':44s}{'CAC per desktop install':>22s}")
print("-"*68)
for n,v in [("Meta -> iOS app -> email -> desktop  (US)",1519),
            ("Meta -> iOS app -> email -> desktop  (Brazil)",315),
            ("Meta -> iOS app -> email -> desktop  (India)",156),
            ("Meta -> web game -> email -> desktop (India)",93)]:
    print(f"{n:44s}{'$'+format(v,',.0f'):>22s}")
base_cac = SPEND/(convs*.60*.45*.30)
print(f"{'Click-to-WhatsApp -> game -> desktop':44s}{'$'+format(base_cac,',.2f'):>22s}   <-- base case")
print(f"\n  That is {156/base_cac:,.0f}x cheaper than the best email route,")
print(f"  and {1519/base_cac:,.0f}x cheaper than the US email route.")
