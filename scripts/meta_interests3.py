import sys, json, time, urllib.parse, urllib.request
sys.path.insert(0,'/Users/danielmatalon/content-machine')
import config
TOK=config.META_TOKEN; V="v21.0"
def search(q, limit=6):
    url=(f"https://graph.facebook.com/{V}/search?type=adinterest"
         f"&q={urllib.parse.quote(q)}&limit={limit}&locale=en_US&access_token={TOK}")
    try: return json.load(urllib.request.urlopen(url, timeout=25)).get("data",[])
    except Exception as e: return [{"name":f"ERROR {e}","id":""}]
out={}
for q in ["Slack (software)","Notion","Zoom Video Communications","Asana","Trello",
          "Google Workspace","Productivity software","Project management"]:
    r=search(q); out[q]=r
    print(f"\n### {q}")
    for i in r[:4]:
        lo=i.get("audience_size_lower_bound") or 0; hi=i.get("audience_size_upper_bound") or 0
        print(f"   {str(i.get('id')):>18s}  {i.get('name','')[:38]:38s} {lo:>13,} - {hi:<13,}")
    time.sleep(2.5)
json.dump(out, open("meta_interests3.json","w"), indent=1)
