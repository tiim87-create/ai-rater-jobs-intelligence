#!/usr/bin/env python3
"""Inspect the exact public JS call site for listJobPosts. No API calls."""
import re, urllib.request, json
url="https://www.telusinternational.ai/landing/index.536d933b.js"
req=urllib.request.Request(url,headers={"User-Agent":"AI-Rater-Insider-Research/0.1"})
with urllib.request.urlopen(req,timeout=30) as r:
    js=r.read(12000000).decode("utf-8","replace")
for term in ("listJobPosts","/list-job-posts","TP.listJobPosts","list-job-posts"):
    matches=list(re.finditer(re.escape(term),js))
    print("TERM",term,"COUNT",len(matches))
    for m in matches[:12]:
        excerpt=js[max(0,m.start()-1100):min(len(js),m.end()+1400)]
        print("CONTEXT",json.dumps({"offset":m.start(),"snippet":excerpt},ensure_ascii=False))
# Inspect lazy-loaded Jobs bundle for payload construction.
for path in ("Jobs.fe444fde.js",):
    asset="https://www.telusinternational.ai/landing/"+path
    try:
        with urllib.request.urlopen(urllib.request.Request(asset,headers={"User-Agent":"AI-Rater-Insider-Research/0.1"}),timeout=30) as r:
            body=r.read(12000000).decode("utf-8","replace")
        print("CHUNK",path,"SIZE",len(body))
        for term in ("listJobPosts","list-job-posts","pageSize","page_size","filters"):
            matches=list(re.finditer(re.escape(term),body,re.I))
            print("TERM",term,"COUNT",len(matches))
            for m in matches[:5]:
                print("CONTEXT",json.dumps({"offset":m.start(),"snippet":body[max(0,m.start()-700):min(len(body),m.end()+900)]},ensure_ascii=False))
    except Exception as e:
        print("CHUNK_ERROR",str(e)[:300])
