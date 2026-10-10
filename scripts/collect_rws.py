#!/usr/bin/env python3
"""Fetch RWS Lever vacancies; publish only after validation."""
import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import urllib.request

API = "https://api.lever.co/v0/postings/{site}?mode=json&limit=100&skip={skip}"
COUNTRIES = {"united states":"US","usa":"US","us":"US","united kingdom":"GB","uk":"GB","india":"IN","bangladesh":"BD","canada":"CA","australia":"AU","germany":"DE","france":"FR","italy":"IT","spain":"ES","poland":"PL","portugal":"PT","brazil":"BR","japan":"JP","south korea":"KR","philippines":"PH","vietnam":"VN","indonesia":"ID","thailand":"TH","malaysia":"MY","singapore":"SG","netherlands":"NL","ireland":"IE","mexico":"MX","argentina":"AR","south africa":"ZA","egypt":"EG","turkey":"TR","pakistan":"PK","nigeria":"NG","kenya":"KE","romania":"RO","czech republic":"CZ","hungary":"HU","greece":"GR","sweden":"SE","norway":"NO","denmark":"DK","finland":"FI","belgium":"BE","switzerland":"CH","austria":"AT","new zealand":"NZ","taiwan":"TW","hong kong":"HK","colombia":"CO","chile":"CL","peru":"PE","united arab emirates":"AE","saudi arabia":"SA","israel":"IL","ukraine":"UA"}
CITY = {"london":"GB","new york":"US","san francisco":"US","boston":"US","dublin":"IE","berlin":"DE","paris":"FR","mumbai":"IN","delhi":"IN","bengaluru":"IN","bangalore":"IN","hyderabad":"IN","kolkata":"IN","dhaka":"BD","toronto":"CA","vancouver":"CA","sydney":"AU","melbourne":"AU","manila":"PH","warsaw":"PL","lisbon":"PT","amsterdam":"NL","singapore":"SG","tokyo":"JP"}
def country(value):
    if not isinstance(value,str): return None
    value=value.lower().strip()
    for term,code in sorted(COUNTRIES.items(),key=lambda x:-len(x[0])):
        if re.search(r"(?<![a-z])"+re.escape(term)+r"(?![a-z])",value): return code
    for term,code in CITY.items():
        if re.search(r"(?<![a-z])"+re.escape(term)+r"(?![a-z])",value): return code
    return None
def fetch(site):
    result=[]
    for skip in range(0,10000,100):
        req=urllib.request.Request(API.format(site=site,skip=skip),headers={"User-Agent":"AI-Rater-Insider/1.0"})
        with urllib.request.urlopen(req,timeout=30) as response: page=json.load(response)
        if not isinstance(page,list): raise ValueError("Unexpected Lever response")
        result.extend(page)
        if len(page)<100: return result
    raise ValueError("Pagination safety limit exceeded")
def transform(post):
    categories=post.get("categories") or {}
    location=categories.get("location") or ""
    all_locations=categories.get("allLocations") or []
    if isinstance(all_locations,str): all_locations=[all_locations]
    explicit=[location]+all_locations
    codes=sorted(set(filter(None,(country(v) for v in explicit))))
    # Title/language never establish eligibility; geography in description requires review.
    workplace=(post.get("workplaceType") or "").lower()
    if workplace not in ("remote","hybrid","on-site"): workplace="unknown"
    return {"id":str(post["id"]),"vendor":"RWS","title":post.get("text",""),"url":post.get("hostedUrl",""),"location_raw":location,"all_locations_raw":all_locations,"countries":codes,"geography_status":"mapped" if codes else "unmapped","workplace_type":workplace,"updated_at":post.get("updatedAt"),"source":"lever"}
def validate(items,old,minimum,unmapped_limit,drop_limit):
    ids=[x["id"] for x in items]
    errors=[]
    if len(items)<minimum: errors.append("Too few vacancies: "+str(len(items)))
    if len(ids)!=len(set(ids)): errors.append("Duplicate Lever IDs")
    if not items: errors.append("Empty feed")
    unmapped=sum(x["geography_status"]=="unmapped" for x in items)
    if items and unmapped/len(items)>unmapped_limit: errors.append("Unmapped share exceeds threshold")
    if old and len(items)<len(old)*(1-drop_limit): errors.append("Unexpected vacancy count drop")
    return errors,unmapped
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--site",default=os.getenv("RWS_LEVER_SITE","rws"))
    p.add_argument("--output",default="data/jobs.json")
    p.add_argument("--report",default="data/quality-report.json")
    p.add_argument("--min-count",type=int,default=1)
    p.add_argument("--max-unmapped",type=float,default=.20)
    p.add_argument("--max-drop",type=float,default=.35)
    a=p.parse_args()
    path=pathlib.Path(a.output)
    old=[]
    if path.exists():
        existing=json.loads(path.read_text())
        old=existing.get("jobs",[]) if isinstance(existing,dict) else existing
    try:
        raw=fetch(a.site)
        items=[transform(x) for x in raw]
        errors,unmapped=validate(items,old,a.min_count,a.max_unmapped,a.max_drop)
    except Exception as exc:
        items=[];unmapped=0;errors=[str(exc)]
    report={"checked_at":dt.datetime.now(dt.timezone.utc).isoformat(),"site":a.site,"count":len(items),"unmapped":unmapped,"errors":errors,"status":"fail" if errors else "pass"}
    reportpath=pathlib.Path(a.report);reportpath.parent.mkdir(parents=True,exist_ok=True)
    reportpath.write_text(json.dumps(report,indent=2)+"\n")
    if errors:
        print(json.dumps(report),file=sys.stderr)
        return 1
    payload={"generated_at":report["checked_at"],"source":"RWS Lever","count":len(items),"jobs":sorted(items,key=lambda x:x["id"])}
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n")
    temporary.replace(path)
    print(json.dumps(report))
    return 0
if __name__=="__main__": sys.exit(main())
