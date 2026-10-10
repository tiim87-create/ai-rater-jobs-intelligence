#!/usr/bin/env python3
"""Read-only TELUS Digital AI Community collector prototype.
Writes an isolated candidate feed; never modifies data/jobs.json.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://jobs.telusdigital.com"
SEARCH = BASE + "/search/cfm5/ai-community/jobs"
OUT = Path("data/telus_test.json")
MAX_PAGES = 20
HEADERS = {"User-Agent": "AI-Rater-Insider-Research/0.1 (public job listings)"}


def extract(html):
    soup = BeautifulSoup(html, "html.parser")
    records = []
    for a in soup.select('a[href*="/jobs/"]'):
        href = urljoin(BASE, a.get("href", ""))
        if not re.search(r"/jobs/\d{5,}", href):
            continue
        container = a
        for _ in range(4):
            if container.parent:
                container = container.parent
        raw = " ".join(container.stripped_strings)
        title = " ".join(a.stripped_strings).strip()
        if not title or len(title) > 180:
            continue
        match = re.search(r"\b(?:ReqEG-\d+|Req_\w+|\d{4,})\b", raw)
        records.append({"title": title, "url": href, "job_id": match.group(0) if match else None, "raw": raw[:500]})
    return records


def main():
    session = requests.Session()
    session.headers.update(HEADERS)
    jobs = {}
    page_counts = []
    for page in range(1, MAX_PAGES + 1):
        response = session.get(SEARCH, params={"page": page}, timeout=30)
        response.raise_for_status()
        batch = extract(response.text)
        page_counts.append(len(batch))
        if not batch:
            if page == 1:
                raise RuntimeError("No TELUS listings parsed on page 1; HTML selectors need inspection")
            break
        for item in batch:
            jobs[item["url"]] = item
        if len(batch) < 25:
            break
    if not jobs:
        raise RuntimeError("No jobs found")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": SEARCH,
        "page_counts": page_counts,
        "jobs": list(jobs.values()),
        "note": "Prototype: raw fields only; geography and project classification not validated"
    }, ensure_ascii=False, indent=2) + "\n")
    print(f"TELUS test: {len(jobs)} unique jobs; pages: {page_counts}; output: {OUT}")
    if len(jobs) < 50:
        raise RuntimeError("Incomplete TELUS crawl (<50 records): inspect output and pagination")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"TELUS test failed: {exc}", file=sys.stderr)
        sys.exit(1)
