#!/usr/bin/env python3
"""Official-source job collector; standard library only. Partial coverage is labeled."""
import datetime as dt
import html
import json
import pathlib
import re
import urllib.request
from urllib.parse import urljoin, urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
HEADERS = {"User-Agent": "AI-Rater-Insider/1.0 (public job research)", "Accept": "application/json,text/html;q=0.9"}
COUNTRIES = {"united states":"United States","usa":"United States","united kingdom":"United Kingdom","uk":"United Kingdom","india":"India","germany":"Germany","france":"France","canada":"Canada","australia":"Australia","japan":"Japan","south africa":"South Africa","brazil":"Brazil","mexico":"Mexico","spain":"Spain","italy":"Italy","netherlands":"Netherlands","ireland":"Ireland","poland":"Poland","sweden":"Sweden","malaysia":"Malaysia","philippines":"Philippines","singapore":"Singapore","thailand":"Thailand","indonesia":"Indonesia","south korea":"South Korea","new zealand":"New Zealand","bangladesh":"Bangladesh","egypt":"Egypt","israel":"Israel","bulgaria":"Bulgaria","czechia":"Czechia","ukraine":"Ukraine","russia":"Russia"}
def request(url, accept=None):
    headers = dict(HEADERS)
    if accept: headers["Accept"] = accept
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=35) as response:
        return response.read().decode("utf-8",errors="replace")
CITY_COUNTRIES = {"kuala lumpur":"Malaysia","riyadh":"Saudi Arabia","jeddah":"Saudi Arabia","dubai":"United Arab Emirates","abu dhabi":"United Arab Emirates","florida":"United States","california":"United States","new york":"United States","london":"United Kingdom","manila":"Philippines","bangkok":"Thailand","amsterdam":"Netherlands","berlin":"Germany","paris":"France","toronto":"Canada","sydney":"Australia","singapore":"Singapore"}
def country_for(location):
    s = str(location or "").lower()
    hits = {canonical for name,canonical in COUNTRIES.items() if re.search(r"(?<![a-z])"+re.escape(name)+r"(?![a-z])",s)}
    if len(hits)==1: return next(iter(hits))
    if len(hits)>1: return "Unmapped"
    city_hits={canonical for name,canonical in CITY_COUNTRIES.items() if re.search(r"(?<![a-z])"+re.escape(name)+r"(?![a-z])",s)}
    return next(iter(city_hits)) if len(city_hits)==1 else "Unmapped"
def read(name,default):
    try: return json.loads((DATA/name).read_text(encoding="utf-8"))
    except (OSError,ValueError): return default
def write(name,value):
    (DATA/name).write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
def lever(vendor,slug):
    source="https://api.lever.co/v0/postings/"+slug+"?mode=json"
    payload=json.loads(request(source,"application/json"))
    if not isinstance(payload,list) or not payload: raise ValueError("Empty or invalid Lever response")
    out=[]
    for p in payload:
        if not isinstance(p,dict) or not p.get("id") or not p.get("text"): continue
        cat=p.get("categories") or {}
        loc=cat.get("location") or ""
        link=p.get("hostedUrl") or "https://jobs.lever.co/"+slug+"/"+str(p["id"])
        if urlparse(link).hostname!="jobs.lever.co": continue
        out.append({"id":vendor+":"+str(p["id"]),"vendor":vendor,"source_id":str(p["id"]),"title":p["text"],"country":country_for(loc),"location_raw":loc,"category":cat.get("department") or cat.get("team") or "Other","url":link,"source":source,"coverage":"full_board"})
    if not out: raise ValueError("No valid Lever records")
    return out
TELUS_URL="https://jobs.telusdigital.com/search/cfm5/ai-community/jobs"
def telus():
    page=request(TELUS_URL,"text/html")
    if len(page)<2000: raise ValueError("Unexpectedly short TELUS page")
    matches=re.findall(r'(?:href|url)\s*[=:]\s*["\']([^"\']*?/jobs/\d+[^"\']*)["\']',page,re.I)
    out={}
    for raw in matches:
        link=urljoin(TELUS_URL,html.unescape(raw).replace("\\/","/"))
        parsed=urlparse(link)
        if parsed.hostname!="jobs.telusdigital.com": continue
        m=re.search(r"/jobs/(\d+)(?:-([^/?#]+))?",parsed.path)
        if not m: continue
        ident,slug=m.groups()
        out[ident]={"id":"TELUS Digital:"+ident,"vendor":"TELUS Digital","source_id":ident,"title":(slug or "TELUS Digital role").replace("-"," ").title(),"country":"Unmapped","location_raw":"","category":"AI Community","url":"https://jobs.telusdigital.com"+parsed.path,"source":TELUS_URL,"coverage":"partial_search_page"}
    if not out: raise ValueError("No TELUS detail links found; site may render client-side")
    return list(out.values())
def main():
    previous=read("jobs.json",{"jobs":[]})
    state={j["id"]:j for j in previous.get("jobs",[]) if isinstance(j,dict) and j.get("id")}
    events=read("history.json",{"events":[]}).get("events",[])
    sources={}
    for vendor,collector,complete in [("RWS",lambda:lever("RWS","rws"),True),("Welo Data",lambda:lever("Welo Data","weloglobal"),True),("TELUS Digital",telus,False)]:
        try:
            fresh=collector()
            seen=set()
            for job in fresh:
                ident=job["id"];seen.add(ident)
                old=state.get(ident)
                job.update(first_seen=old.get("first_seen",NOW) if old else NOW,last_seen=NOW,status="active",missed_complete_scans=0)
                if not old: events.append({"at":NOW,"type":"new","id":ident})
                elif any(old.get(k)!=job.get(k) for k in ("title","country","location_raw","category","url")): events.append({"at":NOW,"type":"changed","id":ident})
                state[ident]=job
            if complete:
                for ident,job in state.items():
                    if job.get("vendor")!=vendor or ident in seen or job.get("status")=="archived": continue
                    job["missed_complete_scans"]=job.get("missed_complete_scans",0)+1
                    job["status"]="archived" if job["missed_complete_scans"]>=2 else "needs_recheck"
                    if job["status"]=="archived": events.append({"at":NOW,"type":"archived","id":ident})
            sources[vendor]={"status":"ok","count":len(fresh),"coverage":"full_board" if complete else "partial","checked_at":NOW}
        except Exception as exc:
            sources[vendor]={"status":"error","error":str(exc)[:250],"coverage":"unknown","checked_at":NOW}
    jobs=sorted(state.values(),key=lambda j:(j.get("vendor",""),j.get("country",""),j.get("title","")))
    write("jobs.json",{"schema_version":1,"generated_at":NOW,"jobs":jobs})
    write("history.json",{"events":events[-10000:]})
    write("summary.json",{"generated_at":NOW,"sources":sources,"counts":{vendor:sum(j.get("vendor")==vendor and j.get("status")=="active" for j in jobs) for vendor in sources},"note":"Vendor totals are not directly comparable. TELUS discovery is partial; Lever boards include jobs outside rating."})
    print(json.dumps(sources,ensure_ascii=False))
    if all(s["status"]=="error" for s in sources.values()): raise SystemExit("All sources failed; retained old jobs")
if __name__=="__main__": main()
