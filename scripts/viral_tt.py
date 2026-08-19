import json, os, requests, time
TOKEN=os.environ["APIFY_TOKEN"]
ACTOR="clockworks~tiktok-scraper"
TERMS=["memory game","test your memory","brain test","can you beat my score",
       "memory challenge","screen recording tutorial","vibe coding","brain teaser challenge"]
url=f"https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items?token={TOKEN}&timeout=420"
body={"searchQueries":TERMS,"resultsPerPage":45,"searchSection":"/video",
      "shouldDownloadCovers":False,"shouldDownloadVideos":False,"shouldDownloadSlideshowImages":False}
try:
    r=requests.post(url,json=body,timeout=460)
    print("http",r.status_code,flush=True)
    items=r.json() if r.ok else []
    print("items",len(items),flush=True)
    json.dump(items,open("viral_tt.json","w"))
except Exception as e:
    print("EXC",e,flush=True)
