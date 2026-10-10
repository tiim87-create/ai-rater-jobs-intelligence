#!/usr/bin/env python3
"""Find likely public job API paths in TELUS AI client bundle, without calling APIs."""
import re, json, urllib.request
root="https://www.telusinternational.ai/landing/"
for asset in ("env.js","index.536d933b.js"):
    req=urllib.request.Request(root+asset,headers={"User-Agent":"AI-Rater-Insider-Research/0.1"})
    with urllib.request.urlopen(req,timeout=25) as response:
        body=response.read(12000000).decode("utf-8","replace")
    print("ASSET",asset,"size",len(body))
    terms=["/jobs","/job","job-search","jobSearch","searchJobs","availableJobs","apapi","opportunities","vacancies"]
    for term in terms:
        hits=list(re.finditer(re.escape(term),body,re.I))
        snippets=[]
        for match in hits[:5]:
            context=body[max(0,match.start()-110):min(len(body),match.end()+150)]
            context=re.sub(r'(?i)(authorization|bearer|token|secret|apikey)[^,; ]{0,120}',"[redacted]",context)
            snippets.append(context[:260])
        print(json.dumps({"term":term,"count":len(hits),"samples":snippets},ensure_ascii=False))
