import json, re
d = json.load(open("hn_items.json"))
c = [x for x in d if x['type']=='comment']
# drop ones where loom only appears as a link
strong = []
for x in c:
    t = x['text']
    if not re.search(r'\bloom\b', t, re.I): continue
    # remove url-only mentions
    t2 = re.sub(r'https?://\S*loom\S*', ' ', t, flags=re.I)
    if not re.search(r'\bloom\b', t2, re.I): continue
    if re.search(r'(weaving|weave|textile|jacquard|handloom|power ?loom|loom band|looming)', t2, re.I) and not re.search(r'(screen|record|video|async|saas|app)', t2, re.I): continue
    x['clean']=re.sub(r'\s+',' ',t2).strip()
    strong.append(x)
print("opinionated loom comments:", len(strong))
json.dump(strong, open("hn_comments.json","w"), indent=1)
PATS = {
 "PRICE / SEAT COST": r"(expensive|pricey|\$\d+ ?/? ?(a )?(mo|month|user|seat|year)|per seat|too expensive|price|pricing|paid plan|free tier|5 ?min|25 video)",
 "SELF-HOST / PRIVACY / OWNERSHIP": r"(self.?host|privacy|confidential|don.t want to upload|own server|on.?prem|open.?source|my own file|local)",
 "ATLASSIAN / DECLINE": r"(atlassian|acquir|enshittif|went downhill|got worse|bloat)",
 "POLISH / ZOOM / SCREEN STUDIO": r"(auto.?zoom|zoom|screen studio|cursor|polish|professional looking|editing)",
 "SHARE / VIEW FRICTION": r"(sign ?in to view|sign ?up to (watch|view)|account to watch|permission|link|embed|expire)",
 "WHY LOVED / JOB TO BE DONE": r"(instead of a meeting|replace(d|s)? (a )?meeting|async|faster than writing|bug report|onboarding|handoff|code review|support|tutorial|walkthrough|demo)",
 "AI": r"(transcript|summar|chapters|filler word|auto.?edit|dub|translate|ai\b)",
 "ALTERNATIVES NAMED": r"(obs|quicktime|screen studio|tella|cap\b|descript|screenflow|camtasia|vidyard|zight|cloudapp|kap\b|shottr|screenrec|guidde|scribe|supademo|arcade|jumpshare|claap|gemoo|screenapp|awesome screenshot)",
}
for label, pat in PATS.items():
    rx = re.compile(pat, re.I)
    hits = [x for x in strong if rx.search(x['clean'])]
    print("\n"+"="*80); print("##", label, f"({len(hits)})")
    hits.sort(key=lambda x: -len(x['clean']))
    for x in hits[:12]:
        print(f"  [{x['date']}] {x['clean'][:400]}")
