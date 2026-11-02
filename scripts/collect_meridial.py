#!/usr/bin/env python3
"""Meridial / Invisible official Greenhouse job board collector."""
import json
import urllib.request
from urllib.parse import urlparse
from collect_rws import country as infer_country

BOARD = "https://job-boards.eu.greenhouse.io/agency"
APIS = (
    "https://boards-api.eu.greenhouse.io/v1/boards/agency/jobs?content=false",
    "https://boards-api.greenhouse.io/v1/boards/agency/jobs?content=false",
)

def fetch():
    failures = []
    for url in APIS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"AI-Rater-Insider/1.0 (public vacancy research)","Accept":"application/json"})
            with urllib.request.urlopen(req, timeout=40) as response:
                data = json.load(response)
            jobs = data.get("jobs")
            if not isinstance(jobs, list) or len(jobs) < 20:
                raise ValueError("Incomplete Greenhouse board")
            return jobs, url
        except Exception as exc:
            failures.append("%s: %s" % (url, str(exc)[:100]))
    raise RuntimeError("; ".join(failures))

def transform(job, source):
    ident = str(job["id"])
    title = str(job["title"]).strip()
    location = str((job.get("location") or {}).get("name") or "").strip()
    url = str(job.get("absolute_url") or "")
    if not url.startswith("https://job-boards.eu.greenhouse.io/agency/jobs/"):
        raise ValueError("Unexpected job URL: "+url)
    # Remote/global is a scope, not a country; never infer a country from the job title.
    remote = any(term in location.lower() for term in ("world wide","worldwide","global","latam","remote")) and not any(term in location.lower() for term in ("united states","united kingdom","canada","india","australia"))
    code = None if remote else infer_country(location)
    codes = [code] if code else []
    departments = job.get("departments") or []
    category = ", ".join(str(d.get("name","")) for d in departments if isinstance(d,dict)) or "Expert AI training"
    return {"id":"Meridial:"+ident,"vendor":"Meridial","source_id":ident,"title":title,"url":url,
            "location_raw":location,"countries":codes,"country":code or ("Global" if remote else "Unmapped"),
            "geography_status":"global" if remote else ("mapped" if code else "unmapped"),
            "category":category,"coverage":"full_board","source":source,"status":"active"}

def collect():
    raw,source=fetch()
    items=[transform(job,source) for job in raw]
    if len(items)!=len({j["id"] for j in items}): raise ValueError("Duplicate Greenhouse job IDs")
    return items
