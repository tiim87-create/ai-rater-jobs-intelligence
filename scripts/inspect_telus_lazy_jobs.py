#!/usr/bin/env python3
"""Inspect lazy-loaded public TELUS Jobs bundle and locate API call sites. Read only."""
import json,re,urllib.request,urllib.parse
base="https://www.telusinternational.ai/landing/"
headers={"User-Agent":"AI-Rater-Insider-Research/0.1"}
def get(path):
    url=urllib.parse.urljoin(base,path)
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=25) as r:
        return r.status,r.url,r.headers.get("content-type",""),r.read(12000000).decode("utf-8","replace")
status,url,ctype,main=get("index.536d933b.js")
print("MAIN",json.dumps({"status":status,"size":len(main)}))
for m in list(re.finditer(r'Jobs\.[a-f0-9]+\.js',main))[:5]:
    name=m.group()
    print("BUNDLE_REF",json.dumps({"name":name,"context":main[max(0,m.start()-200):m.end()+200]}))
    for path in (name,"assets/"+name):
        try:
            code,final,mime,body=get(path)
            print("BUNDLE",json.dumps({"path":path,"status":code,"url":final,"mime":mime,"bytes":len(body),"preview":body[:100]}))
            if "javascript" not in mime and not body.lstrip().startswith(("import ","const ","var ","function ","(()=>","!function")):
                continue
            for term in ("listJobPosts","list-job-posts","/jobs-entry/","pageSize","page_size","searchParams","jobPosts"):
                matches=list(re.finditer(re.escape(term),body,re.I))
                print("TERM",json.dumps({"term":term,"count":len(matches),"samples":[body[max(0,x.start()-600):x.end()+850] for x in matches[:4]]}))
        except Exception as e:
            print("ERROR",json.dumps({"path":path,"error":str(e)[:200]}))
