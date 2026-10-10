#!/usr/bin/env python3
"""TELUS AI public jobs collector: isolated snapshot, no production writes."""
import argparse,datetime as dt,json,pathlib,time,urllib.request
API="https://api.telusinternational.ai/apapi/v1/list-job-posts"
BASE="https://www.telusinternational.ai/cmp/contributor/jobs/available/"
def fetch(page,limit):
    body=json.dumps({"filters":{},"page":page,"limit":limit}).encode("utf-8")
    req=urllib.request.Request(API,data=body,method="POST",headers={"Content-Type":"application/json","Accept":"application/json","X-Caller-Service":"experts-explorer","User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=40) as r:
        if r.status!=200: raise RuntimeError("Unexpected HTTP status")
        return json.load(r)
def collect(limit=50):
    first=fetch(1,limit)
    pagination=first.get("pagination")
    if not isinstance(pagination,dict): raise ValueError("Missing pagination")
    total= pagination.get("total")
    pages=pagination.get("pages")
    if not isinstance(total,int) or not isinstance(pages,int) or total<1 or pages<1 or pages>100: raise ValueError("Invalid pagination")
    results=[]
    for page in range(1,pages+1):
        payload=first if page==1 else fetch(page,limit)
        meta=payload.get("pagination") or {}
        if meta.get("page")!=page or meta.get("total")!=total: raise ValueError("Inconsistent pagination")
        items=payload.get("data")
        if not isinstance(items,list): raise ValueError("Missing data array")
        results.extend(items)
        if page<pages: time.sleep(0.3)
    ids=[str(item.get("id")) for item in results]
    if len(ids)!=len(set(ids)) or len(results)!=total or any(not x or x=="None" for x in ids): raise ValueError("Incomplete or duplicate TELUS listing")
    return results,pagination
def transform(item,now):
    ident=str(item["id"])
    location=item.get("location")
    compensation=item.get("compensation") or {}
    language=item.get("hiring_language") or {}
    return {"id":"TELUS:"+ident,"source_id":ident,"vendor":"TELUS Digital","category":"TELUS Digital","title":str(item.get("title") or "").strip(),"url":BASE+ident,"source":API,"status":"active","coverage":"telus_ai_public_portal","first_seen":now,"last_seen":now,"missed_complete_scans":0,"location_raw":location or "","country":None,"countries":[],"geography_status":"unmapped","workplace_type":item.get("job_type"),"employment_type":item.get("employment_type"),"job_req_id":item.get("job_req_id"),"project_id":item.get("project_id"),"language":language.get("name") if isinstance(language,dict) else None,"language_iso2":language.get("iso2") if isinstance(language,dict) else None,"compensation":compensation if isinstance(compensation,dict) else None,"description":item.get("description")}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="data/telus_jobs_test.json")
    args=p.parse_args()
    raw,pagination=collect()
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    jobs=[transform(item,now) for item in raw]
    if any(not job["title"] for job in jobs): raise ValueError("Blank title")
    doc={"generated_at":now,"source":API,"coverage":"telus_ai_public_portal","pagination":pagination,"jobs":jobs}
    output=pathlib.Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"result":"ok","count":len(jobs),"pages":pagination["pages"],"output":str(output),"mapped":sum(j["geography_status"]=="mapped" for j in jobs),"unmapped":sum(j["geography_status"]=="unmapped" for j in jobs)},ensure_ascii=False))
if __name__=="__main__": main()
