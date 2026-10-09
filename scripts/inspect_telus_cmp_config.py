#!/usr/bin/env python3
"""Inspect TELUS CMP public frontend config and JS asset references."""
import json,re,urllib.request
base="https://www.telusinternational.ai"
for path in ["/cmp/env.js","/cmp/public/jobs/available/"]:
 try:
  with urllib.request.urlopen(urllib.request.Request(base+path,headers={"User-Agent":"AI-Rater-Insider/1.0"}),timeout=25) as r: s=r.read(120000).decode("utf-8","replace")
  if path.endswith(".js"): print(json.dumps({"url":base+path,"body":s[:9000]}))
  else:
   scripts=re.findall(r'<script[^>]+src=["\']([^"\']+)["\']',s,re.I)
   print(json.dumps({"url":base+path,"scripts":scripts,"html_size":len(s)}))
 except Exception as e: print(json.dumps({"url":base+path,"error":str(e)}))
