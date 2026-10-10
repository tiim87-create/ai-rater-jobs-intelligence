#!/usr/bin/env python3
"""Inspect public TELUS job-list module and report request structure without credentials."""
import json,re,urllib.request
base="https://www.telusinternational.ai/landing/"
def fetch(name):
    with urllib.request.urlopen(urllib.request.Request(base+name,headers={"User-Agent":"AI-Rater-Insider-Research/0.1"}),timeout=30) as r:
        body=r.read(12000000).decode("utf-8","replace")
        print("FILE",json.dumps({"name":name,"status":r.status,"mime":r.headers.get("content-type"),"size":len(body)}))
        return body
body=fetch("index.5475cef3.js")
for term in ("listJobPosts","list-job-posts","listJob","Ts.post","Ts.get","pageSize","page_size","pageNumber","pagination","filter","search","jobPosts","jobs-entry","/api/","/list"):
    hits=list(re.finditer(re.escape(term),body,re.I))
    print("TERM",term,"COUNT",len(hits))
    for m in hits[:6]:
        print("CONTEXT",json.dumps({"offset":m.start(),"snippet":body[max(0,m.start()-750):min(len(body),m.end()+1250)]},ensure_ascii=False))
print("IMPORTS",json.dumps(re.findall(r'from["\\\']([^"\\\']+)',body)[:30]))
