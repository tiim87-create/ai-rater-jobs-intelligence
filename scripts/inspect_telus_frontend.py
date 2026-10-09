#!/usr/bin/env python3
"""Discover public frontend bundle URLs and candidate API paths. No auth or bypass."""
import json,re,urllib.request
from urllib.parse import urljoin,urlparse
BASE="https://www.telusinternational.ai/landing/jobs"
req=urllib.request.Request(BASE,headers={"User-Agent":"AI-Rater-Insider/1.0"})
with urllib.request.urlopen(req,timeout=25) as r: page=r.read().decode("utf-8","replace")
assets=[]
for p in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']',page,re.I):
    url=urljoin(BASE,p)
    if urlparse(url).hostname=="www.telusinternational.ai" and url.endswith(".js"): assets.append(url)
print("Script bundles:",json.dumps(assets))
patterns=[r'https?://[^"\'\\\s<>]{8,180}',r'[/][a-zA-Z0-9_/-]*(?:jobs|search|graphql|vacanc|openings)[a-zA-Z0-9_/?=&-]{0,110}']
for asset in assets[:8]:
    try:
        with urllib.request.urlopen(urllib.request.Request(asset,headers={"User-Agent":"AI-Rater-Insider/1.0"}),timeout=30) as r: js=r.read(5000000).decode("utf-8","replace")
        hits=[]
        for pattern in patterns:
            hits.extend(re.findall(pattern,js,re.I))
        filtered=sorted({x[:170] for x in hits if any(k in x.lower() for k in ("api","jobs","search","graphql","vacanc","openings"))})
        print(json.dumps({"asset":asset,"bytes":len(js),"candidates":filtered[:75]},ensure_ascii=False))
    except Exception as exc: print(json.dumps({"asset":asset,"error":str(exc)[:180]}))
