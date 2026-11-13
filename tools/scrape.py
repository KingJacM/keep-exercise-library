import urllib.request, urllib.parse, json, re, time, html as ihtml, pathlib, sys

CATS=[
 ("54826e417fb786000069ad81","全身"),
 ("54826e417fb786000069ad82","胸部"),
 ("54826e417fb786000069ad83","肩部"),
 ("54826e417fb786000069ad84","背部"),
 ("54826e417fb786000069ad85","腿部"),
 ("54826e417fb786000069ad86","腹部"),
 ("54826e417fb786000069ad87","臀部"),
 ("54826e417fb786000069ad88","手臂"),
 ("55cb1b72bfbf17f934371eba","颈部"),
 ("55cb1ca06fe674f94036d581","腰部"),
]
HDR={"User-Agent":"Mozilla/5.0","Accept":"application/json","X-Requested-With":"XMLHttpRequest"}
def fetch(url):
    req=urllib.request.Request(url, headers=HDR)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")

ENTRY=re.compile(r'href=\\?"?/exercises/([0-9a-f]{24})\?gender=([fm])\\?"?[^>]*>.*?data-background=\\?"?([^"\\ ]+)\\?"?.*?<div class=\\?"?name\\?"?>([^<]+)</div><div class=\\?"?level\\?"?>(.*?)</div>', re.S)
def parse_entries(chunk):
    out=[]
    for m in ENTRY.finditer(chunk):
        eid, gender, img, name, levelhtml = m.groups()
        level = levelhtml.count('keep-icon-train') - levelhtml.count('keep-icon-train no')
        out.append({"id":eid,"name":ihtml.unescape(name).strip(),"image":img,"gender":gender,"level":level})
    return out

all_cats={}
for cid, kw in CATS:
    base=f"https://www.calorietech.com/trainingpoint/{cid}"
    first_url=base+"?"+urllib.parse.urlencode({"keyword":kw})
    raw=fetch(first_url); time.sleep(0.3)
    m=re.search(r'共\s*(\d+)\s*个动作', raw)
    total=int(m.group(1)) if m else None
    entries=parse_entries(raw)
    sm=re.search(r'scrollId=([A-Za-z0-9=_%+.-]+)', raw)
    scroll=urllib.parse.unquote(sm.group(1)) if sm else None
    pages=1
    while scroll:
        url=base+"?"+urllib.parse.urlencode({"keyword":kw,"gender":"f","scrollId":scroll})
        try:
            data=json.loads(fetch(url))
        except Exception as e:
            print(f"{kw}: ERROR at page {pages+1}: {e}", flush=True); break
        time.sleep(0.25)
        d=data.get("data",{})
        chunk=d.get("html","")
        new=parse_entries(chunk)
        entries.extend(new); pages+=1
        if not d.get("hasMore"): break
        scroll=d.get("scrollId")
        if not new:
            print(f"{kw}: empty page {pages}, stop", flush=True); break
    # dedupe within cat
    seen={}
    for e in entries: seen[e["id"]]=e
    entries=list(seen.values())
    all_cats[kw]={"category_id":cid,"declared_total":total,"fetched":len(entries),"entries":entries}
    print(f"{kw}: declared={total} fetched_unique={len(entries)} pages={pages}", flush=True)

pathlib.Path("/tmp/keep/by_category.json").write_text(json.dumps(all_cats, ensure_ascii=False, indent=1))
merged={}
for kw, c in all_cats.items():
    for e in c["entries"]:
        if e["id"] in merged:
            merged[e["id"]]["categories"].append(kw)
        else:
            merged[e["id"]]=dict(e); merged[e["id"]]["categories"]=[kw]
print("MERGED unique exercises:", len(merged))
pathlib.Path("/tmp/keep/merged.json").write_text(json.dumps(list(merged.values()), ensure_ascii=False, indent=1))
