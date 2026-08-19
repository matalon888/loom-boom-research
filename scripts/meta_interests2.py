import sys, json, time, urllib.parse, urllib.request
sys.path.insert(0,'/Users/danielmatalon/content-machine')
import config
TOK=config.META_TOKEN; V="v21.0"
def search(q, typ="adinterest", limit=6, extra=""):
    url=(f"https://graph.facebook.com/{V}/search?type={typ}{extra}"
         f"&q={urllib.parse.quote(q)}&limit={limit}&locale=en_US&access_token={TOK}")
    try: return json.load(urllib.request.urlopen(url, timeout=25)).get("data",[])
    except Exception as e: return [{"name":f"ERROR {e}","id":""}]
def show(title, rows):
    print(f"\n### {title}")
    for i in rows[:5]:
        lo=i.get("audience_size_lower_bound") or 0; hi=i.get("audience_size_upper_bound") or 0
        print(f"   {str(i.get('id')):>18s}  {i.get('name','')[:38]:38s} {lo:>13,} - {hi:<13,}")

out={}
for q in ["Upwork","Fiverr","Video editing","Telecommuting","Graphic design","Loom"]:
    r=search(q); out[q]=r; show(q,r); time.sleep(2.5)

print("\n\n=== BEHAVIORS (class=behaviors) ===")
for q in ["business","small business owner","technology early adopter"]:
    r=search(q, typ="adTargetingCategory", extra="&class=behaviors"); out["BEHAVIOR:"+q]=r; show("behavior: "+q, r); time.sleep(2.5)
json.dump(out, open("meta_interests2.json","w"), indent=1)
