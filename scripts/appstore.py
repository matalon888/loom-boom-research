import json, urllib.request, time
APPID = "1474480829"
countries = ["us","gb","ca","au","in","de","br","nl","sg","za","ie","nz","fr","es","ph","jp","mx","it","se","pl"]
out = {}
for c in countries:
    for page in range(1, 11):
        url = f"https://itunes.apple.com/{c}/rss/customerreviews/page={page}/id={APPID}/sortby=mostrecent/json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            d = json.load(urllib.request.urlopen(req, timeout=20))
            entries = d.get("feed", {}).get("entry", [])
            if not entries: break
            for e in entries:
                if "im:rating" not in e: continue
                rid = e["id"]["label"]
                out[rid] = {
                    "src": f"ios:{c}",
                    "score": int(e["im:rating"]["label"]),
                    "title": e["title"]["label"],
                    "content": e["content"]["label"].strip(),
                    "ver": e.get("im:version",{}).get("label"),
                }
        except Exception as ex:
            break
        time.sleep(0.15)
    print(c, len(out), flush=True)
json.dump(list(out.values()), open("ios_reviews.json","w"), indent=1)
print("TOTAL", len(out))
from collections import Counter
print(Counter(r['score'] for r in out.values()))
