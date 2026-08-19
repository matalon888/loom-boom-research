import json, time
from google_play_scraper import reviews, Sort

PID = "com.loom.android"
all_rv = {}
countries = ["us","gb","ca","au","in","de","br","nl","sg","za","ie","nz","fr","es","ph"]
for c in countries:
    for sort, cnt in [(Sort.NEWEST, 200), (Sort.MOST_RELEVANT, 200), (Sort.RATING, 200)]:
        try:
            rs, _ = reviews(PID, lang="en", country=c, sort=sort, count=cnt)
            for r in rs:
                all_rv[r['reviewId']] = {
                    "src": f"play:{c}",
                    "score": r['score'],
                    "at": str(r['at']),
                    "thumbs": r.get('thumbsUpCount', 0),
                    "ver": r.get('reviewCreatedVersion'),
                    "content": (r.get('content') or "").strip(),
                    "reply": (r.get('replyContent') or "")[:300],
                }
        except Exception as e:
            print("err", c, sort, type(e).__name__)
        time.sleep(0.3)
    print(c, len(all_rv), flush=True)

# also pull low-star specifically by filtering score
for c in ["us","gb","in","ca","au"]:
    for star in [1,2,3]:
        try:
            rs, _ = reviews(PID, lang="en", country=c, sort=Sort.NEWEST, count=200, filter_score_with=star)
            for r in rs:
                all_rv[r['reviewId']] = {
                    "src": f"play:{c}:s{star}", "score": r['score'], "at": str(r['at']),
                    "thumbs": r.get('thumbsUpCount',0), "ver": r.get('reviewCreatedVersion'),
                    "content": (r.get('content') or "").strip(),
                    "reply": (r.get('replyContent') or "")[:300],
                }
        except Exception as e:
            print("err2", c, star, type(e).__name__)
        time.sleep(0.3)

out = [v for v in all_rv.values() if v['content']]
json.dump(out, open("play_reviews.json","w"), indent=1)
print("TOTAL", len(out))
from collections import Counter
print(Counter(r['score'] for r in out))
