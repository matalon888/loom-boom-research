import urllib.request, re, gzip, io, json, collections, ssl
UA={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"}
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

def get(u, t=25):
    r=urllib.request.Request(u, headers=UA)
    d=urllib.request.urlopen(r, timeout=t, context=ctx).read()
    if d[:2]==b'\x1f\x8b': d=gzip.decompress(d)
    return d.decode('utf-8','ignore')

def urls_from(x):
    return re.findall(r'<loc>\s*([^<]+?)\s*</loc>', x)

def crawl(domain, maxmaps=14):
    found=set(); maps=[]
    for cand in [f"https://{domain}/sitemap.xml", f"https://{domain}/sitemap_index.xml",
                 f"https://{domain}/sitemap-index.xml", f"https://{domain}/robots.txt"]:
        try:
            body=get(cand)
        except Exception:
            continue
        if cand.endswith('robots.txt'):
            maps += re.findall(r'(?i)sitemap:\s*(\S+)', body)
        else:
            u=urls_from(body)
            if any(s.endswith('.xml') or '.xml' in s for s in u): maps += u
            else: found.update(u)
        if maps or found: break
    seen=set()
    for m in maps[:maxmaps]:
        if m in seen: continue
        seen.add(m)
        try: body=get(m)
        except Exception: continue
        u=urls_from(body)
        if any('.xml' in s for s in u):
            for m2 in u[:maxmaps]:
                try: found.update(urls_from(get(m2)))
                except Exception: pass
        else:
            found.update(u)
    return found

TARGETS=["tella.com","cap.so","screen.studio","veed.io","descript.com","vidyard.com",
         "supademo.com","arcade.software","guidde.com","scribehow.com","zight.com","loom.com"]
report={}
for d in TARGETS:
    try:
        u=crawl(d)
    except Exception as e:
        u=set(); print("ERR",d,e)
    segs=collections.Counter()
    for x in u:
        p=re.sub(r'^https?://[^/]+','',x).strip('/')
        parts=p.split('/')
        segs['/'+(parts[0] if parts and parts[0] else '(home)')]+=1
    report[d]={"total":len(u),"top":segs.most_common(12)}
    print(f"\n=== {d}  ({len(u)} urls indexed in sitemaps)")
    for k,v in segs.most_common(12): print(f"   {v:6d}  {k}")
json.dump(report, open('sitemap_recon.json','w'), indent=1)
