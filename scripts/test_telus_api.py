#!/usr/bin/env python3
"""Test documented-by-frontend public TELUS API paths; no authentication."""
import json,urllib.request,urllib.error
urls=[
"https://api.telusinternational.ai/apapi/v1/public/jobs/available/",
"https://api.telusinternational.ai/apapi/v1/public/jobs/available/111713",
]
for url in urls:
 try:
  req=urllib.request.Request(url,headers={"Accept":"application/json","User-Agent":"AI-Rater-Insider/1.0"})
  with urllib.request.urlopen(req,timeout=20) as r:
   data=r.read(3500).decode("utf-8","replace")
   print(json.dumps({"url":url,"status":r.status,"content_type":r.headers.get("Content-Type"),"sample":data[:1800]}))
 except urllib.error.HTTPError as e: print(json.dumps({"url":url,"status":e.code,"error":str(e)}))
 except Exception as e: print(json.dumps({"url":url,"error":str(e)[:220]}))
