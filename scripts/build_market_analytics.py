#!/usr/bin/env python3
"""Publish coverage-aware analytics from the historical archive."""
import json
from datetime import datetime, timedelta
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / "data"

def build(archive):
    snapshots = sorted(archive["snapshots"], key=lambda s:s["at"])
    if not snapshots:
        return {"schema_version":1,"latest":None,"weekly_pulse":{},"trends":[]}
    latest = snapshots[-1]
    end = datetime.fromisoformat(latest["at"])
    start = end - timedelta(days=7)
    pulse = {}
    for vendor in latest["vendors"]:
        rows = [s for s in snapshots if start < datetime.fromisoformat(s["at"]) <= end and vendor in s["vendors"]]
        verified = [s for s in rows if s["vendors"][vendor]["source_status"]=="ok"]
        baseline = any(datetime.fromisoformat(s["at"]) <= start and vendor in s["vendors"] and s["vendors"][vendor]["source_status"]=="ok" for s in snapshots)
        legacy = any(s.get("legacy_event_semantics") for s in verified)
        usable = bool(verified) and baseline and not legacy and latest["vendors"][vendor]["source_status"]=="ok"
        pulse[vendor] = {"verified_scans":len(verified),"observed_scans":len(rows),
                         "status":"observed" if usable else "insufficient_history",
                         "events":{k:sum(s["vendors"][vendor]["events"].get(k,0) for s in verified) for k in ("new","archived","reopened")} if usable else None}
    return {"schema_version":1,"as_of":latest["at"],"latest":latest,
            "weekly_window":{"start_exclusive":start.isoformat(),"end_inclusive":end.isoformat()},
            "weekly_pulse":pulse,
            "trends":[{"at":s["at"],"complete":s["complete"],"vendors":{v:d["active_listings"] for v,d in s["vendors"].items()}} for s in snapshots]}

def main():
    archive=json.loads((DATA/"market_snapshots.json").read_text())
    target=DATA/"market_analytics.json"
    tmp=target.with_suffix(".tmp")
    tmp.write_text(json.dumps(build(archive),ensure_ascii=False,indent=2)+"\n")
    tmp.replace(target)
if __name__=="__main__":
    main()
