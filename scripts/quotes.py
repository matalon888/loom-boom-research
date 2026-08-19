import json, re
b = json.load(open("buckets.json"))
THEMES = json.load(open("themes.json")) if False else None
PATS = {
 "PRICE / PAYWALL / CAPS": r"(expensive|pricey|paywall|subscription|\$\d|free tier|5 minute|five minute|25 video|video limit|rip.?off|charge|paid plan|premium)",
 "CRASHES / BUGS": r"\b(crash|crashes|crashing|buggy|broken|freeze|glitch|force close|keeps closing)",
 "UPLOAD / PROCESSING / LOST VIDEO": r"(uploading|processing|stuck at|takes forever|never finishes|failed to upload|didn.t save|lost my (video|recording)|disappeared|still uploading)",
 "LOGIN / ACCOUNT": r"(can.t log ?in|cannot log ?in|won.t let me sign|login (loop|fail)|verification|sso|logged out)",
 "EXPORT / DOWNLOAD / OWNERSHIP": r"(download|export|camera roll|save to (my )?(phone|gallery|device)|local copy|mp4|offline)",
 "MOBILE RECORDING UX": r"(record my screen|screen record|phone screen|front camera|selfie|orientation|portrait|landscape|face ?cam)",
 "AUDIO": r"(no sound|out of sync|desync|mic (doesn|not)|audio (issue|problem|cut))",
 "EDITING": r"\b(trim|edit(ing)?|cut out|caption|subtitle|zoom)",
 "AI": r"\b(ai\b|transcript|summary|chapter|filler word|translate)",
 "WHAT THEY LOVE": r"(love|amazing|game changer|life ?saver|so easy|best app|saves me|no more meetings|instantly)",
}
for label, pat in PATS.items():
    rx = re.compile(pat, re.I)
    pool = b['neg'] if label != "WHAT THEY LOVE" else b['pos']
    hits = [r for r in pool if rx.search(r['content'])]
    hits.sort(key=lambda r: (-r.get('thumbs',0), -len(r['content'])))
    print("\n" + "#"*80)
    print("##", label, f"({len(hits)} reviews)")
    for r in hits[:14]:
        c = re.sub(r'\s+',' ', r['content'])[:420]
        print(f"  [{r['score']}★ {r['src']} ↑{r.get('thumbs',0)}] {c}")
