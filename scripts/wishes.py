import json, re
from collections import Counter
play=json.load(open("play_reviews.json")); ios=json.load(open("ios_reviews.json"))
for r in ios: r['content']=(r.get('title','')+'. '+r['content'])
all_r=play+ios
rx=re.compile(r"(i wish|would love|would be (great|nice|amazing|better) if|please add|hope (they|you) add|needs? (a|an|to)|missing|should (be )?(able|have|add)|if only|can you add)", re.I)
hits=[r for r in all_r if rx.search(r['content'])]
print("WISH/REQUEST reviews:", len(hits))
hits.sort(key=lambda r:-r.get('thumbs',0))
for r in hits[:45]:
    c=re.sub(r'\s+',' ',r['content'])
    m=rx.search(c); s=max(0,m.start()-90)
    print(f"[{r['score']}* {r['src']} ^{r.get('thumbs',0)}] ...{c[s:s+300]}")
print("\n=== COMPETITORS NAMED IN APP REVIEWS ===")
comp=["screenrec","obs","bombbomb","vidyard","zoom","screencastify","screenpal","screencast-o-matic","az screen","xrecorder","mobizen","quicktime","camtasia","descript","tella","screen studio","clipchamp","canva","veed","riverside","cleanshot","cap ","vimeo","youtube","google meet","teams","whatsapp","marco polo","scrcpy"]
c=Counter()
for r in all_r:
    t=r['content'].lower()
    for x in comp:
        if x in t: c[x.strip()]+=1
for k,v in c.most_common(25): print(f"  {v:4d}  {k}")
