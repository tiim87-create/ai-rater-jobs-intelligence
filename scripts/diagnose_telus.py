#!/usr/bin/env python3
"""Probe public TELUS career URLs without bypassing access restrictions."""
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone

URLS = {
    "ai_community": "https://jobs.telusdigital.com/search/jobs?cfm5=AI+Community&ns_category=ai-community",
    "ai_community_alt": "https://jobs.telusdigital.com/search/cfm5/ai-community/jobs",
    "telus_ai_jobs": "https://www.telusinternational.ai/landing/jobs",
    "telus_ai_example": "https://www.telusinternational.ai/cmp/contributor/jobs/available/111713",
}
results = {"checked_at": datetime.now(timezone.utc).isoformat(), "probes": {}}
for name, url in URLS.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AI-Rater-Insider/1.0", "Accept": "text/html"})
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read(300000).decode("utf-8", "replace")
            results["probes"][name] = {
                "http_status": r.status, "final_url": r.url, "bytes_sampled": len(body),
                "contains_job_keywords": any(s in body.lower() for s in ("media search analyst", "internet safety evaluator", "online data analyst")),
                "html_title_excerpt": body[:120].replace("\n", " ")
            }
    except urllib.error.HTTPError as exc:
        results["probes"][name] = {"http_status": exc.code, "error": str(exc)}
    except Exception as exc:
        results["probes"][name] = {"error": str(exc)[:250]}
print(json.dumps(results, indent=2))
