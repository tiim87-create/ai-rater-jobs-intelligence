#!/usr/bin/env python3
"""Inspect public TELUS CMP bundle for job API route patterns."""
import json,re,urllib.request
url="https://www.telusinternational.ai/cmp/assets/index-Dm2dRa0U.js"
try:
 req=urllib.request.Request(url,headers={"User-Agent":"AI-Rater-Insider/1.0"})
 with urllib.request.urlopen(req,timeout=35) as r: data=r.read(18000000).decode("utf-8","replace")
 terms=["CMP_API_URL","/jobs/available","/public/jobs","jobs/available","job-postings","job_postings","/jobs/search","/public/"]
 out=[]
 for term in terms:
  matches=list(re.finditer(re.escape(term),data,re.I))
  out.append({"term":term,"count":len(matches),"examples":[data[max(0,m.start()-200):m.end()+260] for m in matches[:5]]})
 print(json.dumps({"url":url,"length":len(data),"results":out},ensure_ascii=False))
except Exception as e: print(json.dumps({"error":str(e)}))
