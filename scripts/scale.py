print("=== 1. THE LOOP — the only channel with no ceiling ===\n")
print("K = (viewers per recording) x (share of viewers who sign up)")
print("K > 1 means every user brings more than one more. That is exponential, forever, free.\n")
print(f"{'viewers/rec':>12s}{'signup %':>10s}{'K':>7s}{'  what happens'}")
print("-"*72)
for v,c,lab in [(2.5,.02,"today, guess: login wall + slow page"),
                (2.5,.08,"no login wall"),
                (3.0,.20,"+ short link, instant play"),
                (3.0,.35,"+ 'reply with your own Boom' button"),
                (4.0,.35,"+ viewers never billed, so links get forwarded")]:
    K=v*c
    tag = "DIES OUT" if K<1 else "EXPONENTIAL"
    print(f"{v:>12.1f}{c*100:>9.0f}%{K:>7.2f}   {tag:12s} {lab}")

print("\n  starting from 1,000 users sending 4 recordings/month, after 12 months:")
for K in (0.05,0.20,0.60,1.05,1.40):
    u=1000.0
    for m in range(12): u = u + u*K
    print(f"    K={K:.2f}  ->  {u:,.0f} users")

print("\n\n=== 2. AFFILIATES — pay only on result, so the ceiling is how many you recruit ===\n")
print(f"{'affiliates':>11s}{'each sends/mo':>15s}{'signups/mo':>12s}{'payers @5%':>12s}{'cost @$20':>11s}")
print("-"*64)
for n in (10,50,200,1000):
    signups=n*40
    payers=signups*.05
    print(f"{n:>11,}{40:>15}{signups:>12,}{payers:>12,.0f}{'$'+format(payers*20,',.0f'):>11s}")
print("\n  Screen Studio did $17,000 of affiliate sales in ONE month off 50,000 clicks.")
print("  You pay after the money arrives. Risk is zero, ceiling is recruitment.")

print("\n\n=== 3. CHROME WEB STORE — the channel nobody in this thread has mentioned ===\n")
print("  Loom's extension: 8,000,000 users.")
print("  Web Store search is intent-driven and AI Overviews cannot touch it.")
print("  'screen recorder' in the Web Store is a ranked list. Ranking there is free distribution.")

print("\n\n=== 4. META — your own Boom Match research already concluded this ===\n")
print("  Boom Match verdict: 'Meta becomes primary volume engine.'")
print("  Google was capped at $3-4K/mo because search intent didn't match product intent.")
print("  Same logic applies to Boom Share: the audience is on Meta, not typing into Google.")
