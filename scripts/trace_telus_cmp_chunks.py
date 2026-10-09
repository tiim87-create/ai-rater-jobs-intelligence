#!/usr/bin/env python3
"""Follow public TELUS CMP JS imports to locate relevant frontend chunks."""
import json,re,urllib.request
from urllib.parse import urljoin,urlparse
root="https://www.telusinternational.ai/cmp/assets/index-Dm2dRa0U.js"
seen=set(); queue=[root]
for depth in range(3):
 nxt=[]
 for url in queue[:25]:
  if url in seen:continue
  seen.add(url)
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AI-Rater-Insider/1.0"}),timeout=30) as r: body=r.read(8000000).decode("utf-8","replace")
   candidates=set(re.findall(r'["\']([^"\']+\.js(?:\?[^"\']*)?)["\']',body))
   imports=[urljoin(url,x) for x in candidates if (x.startswith("./") or x.startswith("/cmp/")) and urlparse(urljoin(url,x)).hostname=="www.telusinternational.ai"]
   keys=["CMP_API_URL","/jobs/available","/public/jobs","jobPostings","job_postings","/jobs/search"]
   matches=[]
   for key in keys:
    m=re.search(re.escape(key),body,re.I)
    if m:matches.append({"key":key,"context":body[max(0,m.start()-160):m.end()+230]})
   print(json.dumps({"depth":depth,"url":url,"size":len(body),"imports":imports[:30],"matches":matches},ensure_ascii=False))
   nxt.extend(imports)
  except Exception as e: print(json.dumps({"url":url,"error":str(e)}))
 queue=nxt
