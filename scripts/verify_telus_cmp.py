#!/usr/bin/env python3
"""Probe actual TELUS CMP public jobs URL extracted from frontend."""
import urllib.request,urllib.error,json
urls=["https://www.telusinternational.ai/cmp/public/jobs/available/","https://www.telusinternational.ai/cmp/public/jobs/available/111713"]
for url in urls:
 try:
  req=urllib.request.Request(url,headers={"Accept":"application/json, text/html;q=0.8","User-Agent":"AI-Rater-Insider/1.0"})
  with urllib.request.urlopen(req,timeout=20) as r:
   body=r.read(4000).decode("utf-8","replace")
   print(json.dumps({"url":url,"status":r.status,"content_type":r.headers.get("Content-Type"),"sample":body[:1400]}))
 except urllib.error.HTTPError as e:print(json.dumps({"url":url,"status":e.code,"error":str(e)}))
 except Exception as e:print(json.dumps({"url":url,"error":str(e)[:200]}))
