#!/usr/bin/env python3
"""Single read-only public API request. Never writes production jobs."""
import json,urllib.request,urllib.error
url="https://api.telusinternational.ai/apapi/v1/list-job-posts"
payload=json.dumps({"filters":{},"page":1,"limit":10}).encode()
req=urllib.request.Request(url,data=payload,method="POST",headers={"Content-Type":"application/json","Accept":"application/json","X-Caller-Service":"experts-explorer","User-Agent":"Mozilla/5.0"})
try:
    with urllib.request.urlopen(req,timeout=30) as r:
        raw=r.read(250000)
        print("HTTP_STATUS",r.status)
        data=json.loads(raw)
        print("RESPONSE_KEYS",list(data) if isinstance(data,dict) else type(data).__name__)
        if isinstance(data,dict):
            items=data.get("data",[])
            print("PAGINATION",json.dumps(data.get("pagination",{})))
            print("JOBS_COUNT_PAGE",len(items) if isinstance(items,list) else "unexpected")
            for item in (items[:3] if isinstance(items,list) else []):
                print("JOB_SAMPLE",json.dumps({k:item.get(k) for k in ("id","title","location","job_type","employment_type","job_req_id","hiring_language","project_id","compensation")},ensure_ascii=False))
        else: print("RESPONSE_TYPE",type(data).__name__)
except urllib.error.HTTPError as e:
    print("HTTP_STATUS",e.code)
    print("ERROR_BODY",e.read(1000).decode("utf-8","replace"))
except Exception as e:
    print("REQUEST_ERROR",str(e)[:500])
