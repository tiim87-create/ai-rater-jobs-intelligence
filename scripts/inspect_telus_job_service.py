#!/usr/bin/env python3
"""Extract public TELUS JobEntryService network method definitions."""
import json,re,urllib.request
url="https://www.telusinternational.ai/cmp/assets/JobEntryService-D7kTfxuQ.js"
try:
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AI-Rater-Insider/1.0"}),timeout=30) as r:s=r.read(2500000).decode("utf-8","replace")
 terms=["getJobPosts","getPublicJobPost","getJobPost","/job-posts","/public","CMP_API_URL"]
 out=[]
 for term in terms:
  ms=list(re.finditer(re.escape(term),s,re.I))
  out.append({"term":term,"count":len(ms),"examples":[s[max(0,m.start()-350):m.end()+480] for m in ms[:5]]})
 print(json.dumps({"url":url,"length":len(s),"matches":out},ensure_ascii=False))
except Exception as e:print(json.dumps({"error":str(e)}))
