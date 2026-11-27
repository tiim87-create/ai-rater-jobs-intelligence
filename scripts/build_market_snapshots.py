#!/usr/bin/env python3
"""Build durable per-scan snapshots from validated vacancy data."""
import json
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta

DATA = Path(__file__).resolve().parents[1] / "data"

def build_snapshot(jobs, summary, events):
    at = summary["generated_at"]
    vendors = {}
    countries = set()
    for vendor, source in summary["sources"].items():
        rows = [j for j in jobs if j["vendor"] == vendor and j.get("status") == "active"]
        observed = source["status"] == "ok"
        source_at = source.get("last_successful_at")
        fresh = observed and (source_at == at if source_at else not any(s.get("last_successful_at") for s in summary["sources"].values()))
        codes = {c for j in rows for c in (j.get("countries") or [])}
        if observed:
            countries.update(codes)
        vendors[vendor] = {
            "source_status": source["status"],
            "source_observed_at": source_at or (at if fresh else None),
            "fresh_observation": fresh,
            "reported_count": source.get("count"),
            "coverage": source.get("coverage"),
            "active_listings": len(rows) if observed else None,
            "retained_active_listings": len(rows),
            "countries": sorted(codes) if observed else None,
            "country_associations": dict(Counter(c for j in rows for c in set(j.get("countries") or []))) if observed else None,
            "project_families": dict(Counter(j.get("project_family") or j.get("family") or "Unclassified" for j in rows)) if observed else None,
            "events": dict(Counter(e["type"] for e in events if e["at"] == at and e["id"] in {j["id"] for j in jobs if j["vendor"] == vendor})) if fresh else None,
        }
    complete = all(v["source_status"] == "ok" for v in vendors.values())
    return {"at": at, "complete": complete, "vendors": vendors,
            "observed_active_listings": sum(v["active_listings"] or 0 for v in vendors.values()),
            "observed_countries": sorted(countries)}

def main():
    def read(name):
        return json.loads((DATA / name).read_text(encoding="utf-8"))
    jobs = read("jobs.json")
    summary = read("summary.json")
    assert jobs["generated_at"] == summary["generated_at"]
    snapshot = build_snapshot(jobs["jobs"], summary, read("history.json")["events"])
    path = DATA / "market_snapshots.json"
    archive = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schema_version": 1, "snapshots": []}
    prior = {s["at"]: s for s in archive["snapshots"]}
    if snapshot["at"] in prior:
        assert prior[snapshot["at"]] == snapshot, "Conflicting snapshot"
    else:
        archive["snapshots"].append(snapshot)
    archive["snapshots"].sort(key=lambda s: s["at"])
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(archive, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)

if __name__ == "__main__":
    main()
