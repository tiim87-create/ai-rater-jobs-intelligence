#!/usr/bin/env python3
"""Read-only check of candidate public TELUS job listing endpoint."""
import json, urllib.request, urllib.error
url="https://api.telusinternational.ai/apapi/v1/list-job-posts"
for method in ("GET",):
    req=urllib.request.Request(url,method=method,headers={"Accept":"application/json","User-Agent":"AI-Rater-Insider-Research/0.1"})
    try:
        with urllib.request.urlopen(req,timeout=25) as r:
            body=r.read(20000).decode("utf-8","replace")
            print(json.dumps({"method":method,"status":r.status,"content_type":r.headers.get("content-type"),"sample":body[:1800]}))
    except urllib.error.HTTPError as e:
        print(json.dumps({"method":method,"status":e.code,"content_type":e.headers.get("content-type"),"sample":e.read(1200).decode("utf-8","replace")}))
    except Exception as e:
        print(json.dumps({"method":method,"error":str(e)[:300]}))
