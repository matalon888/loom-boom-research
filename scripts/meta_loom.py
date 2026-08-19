import sys, json, time, urllib.parse, urllib.request
sys.path.insert(0,'/Users/danielmatalon/content-machine')
import config
TOK=config.META_TOKEN; V="v21.0"
def search(q, limit=8):
    url=(f"https://graph.facebook.com/{V}/search?type=adinterest"
         f"&q={urllib.parse.quote(q)}&limit={limit}&locale=en_US&access_token={TOK}")
    try: return json.load(urllib.request.urlopen(url, timeout=25)).get("data",[])
    except Exception as e: return [{"name":f"ERR {e}","id":""}]
out={}
for q in ["Atlassian","Jira","Confluence","Screencast","Camtasia","Wistia",
          "Vidyard","Loom video","Web conferencing","Videotelephony"]:
    r=search(q); out[q]=r
    hits=[i for i in r if i.get("id")]
    print(f"\n### {q}   {'(nothing)' if not hits else ''}")
    for i in hits[:4]:
        lo=i.get("audience_size_lower_bound") or 0; hi=i.get("audience_size_upper_bound") or 0
        print(f"   {str(i.get('id')):>18s}  {i.get('name','')[:36]:36s} {lo:>13,} - {hi:<13,}")
    time.sleep(2.5)
json.dump(out, open("meta_loom.json","w"), indent=1)
