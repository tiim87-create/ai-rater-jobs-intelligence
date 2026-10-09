#!/usr/bin/env python3
"""Inspect public TELUS CMP app module references for job list chunk names."""
import json,re,urllib.request
base="https://www.telusinternational.ai/cmp/assets/"
for file in ["App-60nZzUH5.js","AmplitudeProvider-Cxk72iIs.js"]:
 try:
  with urllib.request.urlopen(urllib.request.Request(base+file,headers={"User-Agent":"AI-Rater-Insider/1.0"}),timeout=25) as r: data=r.read(2000000).decode("utf-8","replace")
  assets=sorted(set(re.findall(r'["\']([^"\']+\.js)["\']',data)))
  selected=[a for a in assets if any(x in a.lower() for x in ["job","opportun","vacan","search","list","public"])]
  terms=["JOB_LIST","JOBS_LIST","AVAILABLE_JOBS","/contributor/jobs","public/jobs/available"]
  matches=[]
  for term in terms:
   for m in list(re.finditer(re.escape(term),data,re.I))[:3]:
    matches.append({"term":term,"context":data[max(0,m.start()-160):m.end()+240]})
  print(json.dumps({"file":file,"candidate_chunks":selected[:100],"contexts":matches},ensure_ascii=False))
 except Exception as e:print(json.dumps({"file":file,"error":str(e)}))
