import json, re
from collections import Counter, defaultdict

play = json.load(open("play_reviews.json"))
ios = json.load(open("ios_reviews.json"))
for r in ios: r['content'] = (r.get('title','')+'. '+r['content'])
all_r = play + ios
print("total reviews:", len(all_r), "| play", len(play), "| ios", len(ios))
print("rating dist:", sorted(Counter(r['score'] for r in all_r).items()))

THEMES = {
 "price/paywall": r"\b(expensive|pricey|price|pricing|paywall|subscription|subscribe|\$\d|cost|free tier|freemium|5 ?min|five minute|25 video|video limit|limit of \d|rip.?off|money grab|charge)",
 "5-min & video caps": r"(5 minute|five minute|5-minute|25 video|video limit|only \d+ videos|time limit|limited to \d)",
 "app crashes/bugs": r"\b(crash|crashes|crashing|bug|buggy|broken|freeze|frozen|glitch|force close|keeps closing|error)",
 "upload/processing slow": r"(upload|uploading|processing|stuck at|takes forever|slow to process|never finishes|failed to upload|didn.t save|lost my (video|recording)|disappeared)",
 "audio problems": r"\b(audio|sound|mic|microphone|no sound|out of sync|desync|echo|volume)",
 "video quality": r"(quality|blurry|pixel|resolution|1080|4k|720|grainy|compress)",
 "editing/trim": r"\b(edit|editing|trim|trimming|cut|splice|crop|zoom|caption|subtitle)",
 "mobile recording UX": r"(record my screen|screen record|phone screen|mobile record|camera|selfie|front camera|orientation|portrait|landscape)",
 "login/account": r"(log ?in|login|sign ?in|sign ?up|password|account|sso|verify|verification|can.t access)",
 "sharing/link": r"(link|share|sharing|url|embed|permission|access denied|private|password protect)",
 "AI features": r"\b(ai|transcript|transcription|summary|summar|chapter|filler word|auto ?edit|translate|dub)",
 "storage/export/download": r"(download|export|save to|camera roll|storage|gallery|mp4|local copy|offline)",
 "support": r"(support|customer service|no reply|ticket|help desk|contact them|refund)",
 "speed/lightweight": r"(fast|quick|easy|simple|seamless|effortless|intuitive|lightweight)",
 "viewer analytics": r"(view|viewer|watched|analytics|engagement|who watched|notification)",
 "atlassian/enterprise": r"(atlassian|jira|acquired|enterprise|team plan|workspace|admin)",
}

def bucket(rows, label):
    print("\n" + "="*70)
    print(label, "| n =", len(rows))
    counts = []
    for t, pat in THEMES.items():
        rx = re.compile(pat, re.I)
        hits = [r for r in rows if rx.search(r['content'])]
        counts.append((len(hits), t))
    for n, t in sorted(counts, reverse=True):
        print(f"  {n:5d}  {100*n/max(1,len(rows)):5.1f}%  {t}")

neg = [r for r in all_r if r['score'] <= 2]
pos = [r for r in all_r if r['score'] >= 4]
mid = [r for r in all_r if r['score'] == 3]
bucket(neg, "NEGATIVE (1-2 star)")
bucket(pos, "POSITIVE (4-5 star)")
bucket(mid, "MIXED (3 star)")

json.dump({"neg":neg,"pos":pos,"mid":mid}, open("buckets.json","w"))
