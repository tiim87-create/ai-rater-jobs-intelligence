#!/usr/bin/env python3
"""Find the TELUS CMP API client implementing getJobPosts and getPublicJobPost."""
import json,re,urllib.request
base="https://www.telusinternational.ai/cmp/assets/"
files=["JobList-DOnTXtSO.js","useJobPostPreview-DQvLKGcc.js"]
for f in files:
 try:
  with urllib.request.urlopen(urllib.request.Request(base+f),timeout=25) as r: s=r.read(2000000).decode("utf-8","replace")
  print(json.dumps({"file":f,"imports":re.findall(r'import[^;]{0,900}?from["\'][^"\']+["\']',s)[:18],"header":s[:2200]},ensure_ascii=False))
 except Exception as e:print(json.dumps({"file":f,"error":str(e)}))
