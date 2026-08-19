import json, re
from collections import Counter
rel=json.load(open("reddit_rel.json"))
wins=[]
for x in rel:
    t=x['text']
    for m in re.finditer(r'\bloom\b', t, re.I):
        s=max(0,m.start()-260); e=min(len(t), m.end()+320)
        w=t[s:e]
        wins.append({"sub":x['sub'],"date":x['date'],"url":x['url'],"w":w})
# dedupe overlapping
seen=set(); W=[]
for x in wins:
    k=(x['sub'],x['w'][:80])
    if k in seen: continue
    seen.add(k); W.append(x)
print("loom mention windows:", len(W))
PATS={
 "5-MIN / 25-VIDEO CAP": r"(5.?min|five.?minute|25 video|video limit|cap(ped)? at|hit the limit|free plan only|limits on the free)",
 "PRICE / SEATS / BILLING": r"(\$\d+|too expensive|pricey|per seat|per user|billing|charged|subscription|paywall|cheaper|price)",
 "DOWNLOAD / OWN FILE / SELF-HOST": r"(download|export|mp4|own (the|your) (file|data)|local(-| )first|self.?host|raw file|offline)",
 "AUTO-ZOOM / POLISH / STUDIO LOOK": r"(auto.?zoom|zoom (on|from) click|cursor|smooth|studio look|polish|professional|template|background)",
 "AI EDIT / CAPTIONS / DUB": r"(filler word|remove silence|silence trim|caption|subtitle|transcript|dub|translat|ai edit|summar)",
 "VIEWER FRICTION / SIGN-IN / SHARING": r"(sign ?in to (view|watch)|account to (view|watch)|viewer|share.{0,20}link|embed|password)",
 "PRIVACY / GDPR / EU DATA": r"(gdpr|privacy|schrems|data resid|confidential|compliance|eu infrastructure)",
 "RELIABILITY / CRASH / UPLOAD": r"(crash|buggy|unreliable|stuck|fail(ed|s)? to upload|lost (the|my) (video|recording)|slow)",
 "JOB TO BE DONE": r"(onboarding|walkthrough|training|sop|client|support ticket|bug report|handoff|standup|demo|tutorial|course|cold (email|outreach)|sales)",
}
for label,pat in PATS.items():
    rx=re.compile(pat,re.I); hits=[x for x in W if rx.search(x['w'])]
    print("\n"+"="*80);print("##",label,f"({len(hits)})")
    for x in hits[:14]:
        txt = re.sub(r"\s+", " ", x["w"])[:360]
        print("  [r/%s %s] ...%s" % (x["sub"], x["date"], txt))
