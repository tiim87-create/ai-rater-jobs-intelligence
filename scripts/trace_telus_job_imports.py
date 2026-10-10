#!/usr/bin/env python3
"""Trace TELUS public Jobs module imports into the main JS bundle (read-only)."""
import json,re,urllib.request
base="https://www.telusinternational.ai/landing/"
def fetch(name):
    with urllib.request.urlopen(urllib.request.Request(base+name,headers={"User-Agent":"AI-Rater-Insider-Research/0.1"}),timeout=30) as r:
        return r.read(12000000).decode("utf-8","replace")
jobs=fetch("Jobs.fe444fde.js")
main=fetch("index.536d933b.js")
print("JOBS_MODULE",jobs)
print("MAIN_SIZE",len(main))
# Resolve minified exports by parsing main bundle's terminal export declaration.
for term in ('export{','export {','listJobPosts','TP.listJobPosts','TP.','C_1','/list-job-posts'):
    matches=list(re.finditer(re.escape(term),main))
    print("TERM",term,"COUNT",len(matches))
    chosen=matches[-3:] if term.startswith("export") else matches[:5]
    for m in chosen:
        print("SNIPPET",json.dumps({"offset":m.start(),"value":main[max(0,m.start()-650):min(len(main),m.end()+1600)]},ensure_ascii=False))
# Find all usages of the endpoint map and APAPI base, rather than just its definition.
for term in ('listJobPosts:', 'listJobPosts)', 'listJobPosts]', 'TP[', 'TP.', 'C_1+'):
    print("REFERENCE_COUNT",term,len(list(re.finditer(re.escape(term),main))))
