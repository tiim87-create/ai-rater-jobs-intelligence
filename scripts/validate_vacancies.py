#!/usr/bin/env python3
"""Validate the unified vacancy feed before publication."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
jobs_doc = json.loads((DATA / "jobs.json").read_text(encoding="utf-8"))
summary_doc = json.loads((DATA / "summary.json").read_text(encoding="utf-8"))
history_doc = json.loads((DATA / "history.json").read_text(encoding="utf-8"))
jobs = jobs_doc.get("jobs")
sources = summary_doc.get("sources")
assert isinstance(jobs, list) and jobs, "Vacancy feed is empty"
assert isinstance(sources, dict) and sources, "Missing source diagnostics"
assert isinstance(history_doc.get("events"), list), "Invalid history"
ids = [j.get("id") for j in jobs]
assert all(isinstance(i, str) and i for i in ids), "Missing vacancy IDs"
assert len(ids) == len(set(ids)), "Duplicate vacancy IDs"
assert all(j.get("vendor") and j.get("title") and j.get("url") for j in jobs), "Incomplete vacancy"
assert set(sources) >= {"RWS", "Welo Data", "TELUS Digital", "Meridial"}, "Missing source status"
assert all(s.get("status") in ("ok", "stale", "warning") for s in sources.values()), "Fatal source error"
assert sources["TELUS Digital"]["status"] != "stale" or any(j["vendor"] == "TELUS Digital" for j in jobs), "Stale TELUS without retained records"
print(json.dumps({"validation": "ok", "total_jobs": len(jobs), "sources": {k:v["status"] for k,v in sources.items()}}))
