#!/usr/bin/env python3
"""Inspect public TELUS job list frontend chunk for exact network routes."""
import json,re,urllib.request
base="https://www.telusinternational.ai/cmp/assets/"
for file in ["JobList-DOnTXtSO.js","useJobPostPreview-DQvLKGcc.js"]:
 try:
  with urllib.request.urlopen(urllib.request.Request(base+file,headers={"User-Agent":"AI-Rater-Insider/1.0"}),timeout=30) as r: s=r.read(5000000).decode("utf-8","replace")
  terms=["/jobs","job-post","job_post","jobPost","CMP_API_URL","axios","fetch(","/available","/search","/public"]
  out=[]
  for term in terms:
   ms=list(re.finditer(re.escape(term),s,re.I))
   out.append({"term":term,"count":len(ms),"contexts":[s[max(0,m.start()-180):m.end()+250] for m in ms[:5]]})
  print(json.dumps({"file":file,"length":len(s),"results":out},ensure_ascii=False))
 except Exception as e: print(json.dumps({"file":file,"error":str(e)}))
