#!/usr/bin/env python3
"""Extract exact public TELUS CMP JobEntryService list request and base URL."""
import urllib.request,json,re
url="https://www.telusinternational.ai/cmp/assets/JobEntryService-D7kTfxuQ.js"
with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AI-Rater-Insider/1.0"}),timeout=30) as r:s=r.read().decode("utf-8","replace")
terms=["Y=async","Y=(", "E=", "u=", "jobs-entry/job-posts","job-posts/search","job-posts?","getJobPosts:Y"]
for term in terms:
 ms=list(re.finditer(re.escape(term),s))
 print(json.dumps({"term":term,"count":len(ms),"contexts":[s[max(0,m.start()-450):m.end()+1000] for m in ms[:4]]},ensure_ascii=False))
print(json.dumps({"prefix":s[:2300]},ensure_ascii=False))
