import sys, json, time, urllib.parse, urllib.request
sys.path.insert(0,'/Users/danielmatalon/content-machine')
import config
TOK=config.META_TOKEN
V="v21.0"
def search(q, typ="adinterest", limit=8):
    url=(f"https://graph.facebook.com/{V}/search?type={typ}"
         f"&q={urllib.parse.quote(q)}&limit={limit}&locale=en_US&access_token={TOK}")
    try:
        d=json.load(urllib.request.urlopen(url, timeout=25))
        return d.get("data",[])
    except Exception as e:
        return [{"name":f"ERROR {e}","id":"","audience_size_lower_bound":0}]

QUERIES=["Freelancer","Advertising agency","Small business","Entrepreneurship",
         "Startup company","Screen recording","Software development","Puzzle video game"]
out={}
for q in QUERIES:
    r=search(q)
    out[q]=r
    print(f"\n### {q}")
    for i in r[:6]:
        lo=i.get("audience_size_lower_bound") or i.get("audience_size") or 0
        hi=i.get("audience_size_upper_bound") or 0
        path=" > ".join(i.get("path") or [])
        print(f"   {str(i.get('id')):>18s}  {i.get('name','')[:36]:36s} {lo:>13,} - {hi:<13,} {path[:44]}")
    time.sleep(2.5)
json.dump(out, open("meta_interests.json","w"), indent=1)
