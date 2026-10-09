#!/usr/bin/env python3
"""Inspect public frontend source near TELUS job API references."""
import re,urllib.request,json
urls=["https://www.telusinternational.ai/landing/env.js","https://www.telusinternational.ai/landing/index.536d933b.js"]
for url in urls:
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"AI-Rater-Insider/1.0"}),timeout=30) as r: body=r.read(12000000).decode("utf-8","replace")
  terms=["/public/jobs/available/","apapi/v1","baseURL","apiUrl","jobs/available","/jobs/search"]
  output=[]
  for term in terms:
   matches=list(re.finditer(re.escape(term),body,re.I))
   for m in matches[:4]:
    output.append({"term":term,"context":body[max(0,m.start()-260):min(len(body),m.end()+300)]})
  print(json.dumps({"url":url,"length":len(body),"matches":output},ensure_ascii=False))
 except Exception as e: print(json.dumps({"url":url,"error":str(e)}))
