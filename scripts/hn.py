import json, urllib.request, urllib.parse, time, re, html
Q = ["loom video","loom screen recording","screen recorder alternative","loom.com","async video","screen studio","loom alternative"]
out = {}
for q in Q:
    for tags in ["comment","story"]:
        for page in range(0,4):
            u = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(q)}&tags={tags}&hitsPerPage=100&page={page}"
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"research"}), timeout=20))
            except Exception as e:
                print("err", q, e); break
            if not d['hits']: break
            for h in d['hits']:
                txt = h.get('comment_text') or h.get('story_text') or h.get('title') or ""
                txt = html.unescape(re.sub(r'<[^>]+>',' ', txt)).strip()
                if not txt or 'loom' not in txt.lower(): continue
                out[h['objectID']] = {"src":"hn","q":q,"type":tags,"points":h.get('points'),
                                      "date":h.get('created_at','')[:10],
                                      "url":f"https://news.ycombinator.com/item?id={h['objectID']}",
                                      "text":re.sub(r'\s+',' ',txt)[:2000]}
            time.sleep(0.2)
json.dump(list(out.values()), open("hn_items.json","w"), indent=1)
print("HN items:", len(out))
