#!/usr/bin/env python3
"""Inspect public TELUS AI landing JS for potential job-feed endpoints.
Diagnostic only: no authentication, no protected API requests, no changes to jobs.json.
"""
import json
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ROOT = "https://www.telusinternational.ai/landing/jobs"
HEADERS = {"User-Agent": "AI-Rater-Insider-Research/0.1", "Accept": "text/html,application/javascript,*/*"}

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=25) as response:
        data = response.read(4000000)
        return response.status, response.headers.get("content-type", ""), data.decode("utf-8", "replace")

class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        if tag != "script":
            return
        a = dict(attrs)
        if a.get("src"):
            self.scripts.append(urllib.parse.urljoin(ROOT, a["src"]))

status, ctype, html = fetch(ROOT)
parser = Assets()
parser.feed(html)
print("landing", json.dumps({"status": status, "bytes": len(html), "scripts": parser.scripts}))
if not parser.scripts:
    raise RuntimeError("No script assets found; inspect landing HTML")
for url in parser.scripts[:12]:
    try:
        code, mime, js = fetch(url)
        # Print short, de-duplicated candidate URL strings; no credential material.
        candidates = sorted(set(re.findall(r'(?:(?:https?:)?//[^\\\s\"\x27<>]{8,180}|/api/[A-Za-z0-9_/?=&.\\-]{3,130})', js)))
        candidates = [x for x in candidates if any(w in x.lower() for w in ("job", "career", "api", "graphql", "posting"))]
        tokens = {term: js.lower().count(term) for term in ("graphql", "/api/", "joblisting", "jobsearch", "availablejobs", "jobid")}
        print("asset", json.dumps({"url": url, "status": code, "bytes": len(js), "tokens": tokens, "candidate_urls": candidates[:35]}))
    except Exception as exc:
        print("asset_error", json.dumps({"url": url, "error": str(exc)[:220]}))
