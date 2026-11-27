#!/usr/bin/env python3
"""Aggregate independent source observations into UTC Friday ISO-week endpoints."""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / "data"
VENDORS = ("RWS", "Welo Data", "Meridial", "TELUS Digital")

def utc(value):
    d = datetime.fromisoformat(value)
    if d.tzinfo is None:
        raise ValueError("Observation timestamp must include timezone")
    return d.astimezone(timezone.utc)

def build(archive):
    weeks = {}
    for snap in sorted(archive["snapshots"], key=lambda s: utc(s["at"])):
        for vendor, row in snap["vendors"].items():
            if vendor not in VENDORS or row.get("source_status") != "ok":
                continue
            if row.get("fresh_observation") is not True:
                continue
            at = row.get("source_observed_at")
            if not at:
                continue
            d = utc(at)
            if d.weekday() != 4:
                continue
            year, week, _ = d.isocalendar()
            key = f"{year}-W{week:02d}"
            w = weeks.setdefault(key, {"week":key, "friday":d.date().isoformat(), "vendors":{}})
            old = w["vendors"].get(vendor)
            if old and utc(old["observed_at"]) >= d:
                continue
            w["vendors"][vendor] = {
                "observed_at":at, "coverage":row.get("coverage"),
                "count":row.get("reported_count") if row.get("reported_count") is not None else row.get("active_listings"),
                "listing_ids":row.get("listing_ids"), "countries":row.get("countries"),
                "country_associations":row.get("country_associations"),
                "project_families":row.get("project_families"),
                "provenance":snap.get("provenance", {"kind":"snapshot","at":snap["at"]})
            }
    result = []
    for key,w in sorted(weeks.items()):
        prior = next((p for p in reversed(result) if p["friday"] == (datetime.fromisoformat(w["friday"])-timedelta(days=7)).date().isoformat()), None)
        for v in VENDORS:
            row = w["vendors"].setdefault(v, None)
            if row is None:
                continue
            prev = prior["vendors"].get(v) if prior else None
            row["change"] = None
            if prev and row["coverage"] and row["coverage"] == prev["coverage"] and row["listing_ids"] is not None and prev["listing_ids"] is not None:
                a,b = set(row["listing_ids"]),set(prev["listing_ids"])
                if len(a)==row["count"] and len(b)==prev["count"]:
                    row["change"]={"added":len(a-b),"removed":len(b-a),"net":len(a)-len(b)}
        w["missing_sources"]=[v for v in VENDORS if w["vendors"][v] is None]
        w["complete"]=not w["missing_sources"]
        w["observed_total"]=sum(row["count"] or 0 for row in w["vendors"].values() if row is not None)
        result.append(w)
    return {"schema_version":1,"cadence":"weekly_friday_utc","weeks":result}

if __name__ == "__main__":
    archive=json.loads((DATA/"market_snapshots.json").read_text())
    target=DATA/"market_weekly.json"
    tmp=target.with_suffix(".tmp")
    tmp.write_text(json.dumps(build(archive),ensure_ascii=False,indent=2)+"\n")
    tmp.replace(target)
