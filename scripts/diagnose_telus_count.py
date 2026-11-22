#!/usr/bin/env python3
"""Read-only TELUS API diagnostics: pagination, source identity, count drift."""
import datetime as dt,json,sys
from pathlib import Path
from collect_telus import collect,API
root=Path(__file__).resolve().parents[1]/"data"
report={"checked_at":dt.datetime.now(dt.timezone.utc).isoformat(),"api":API}
try:
    jobs,meta=collect()
    report["api_total"]=len(jobs)
    report["pagination"]=meta
    report["unique_ids"]=len({str(j["id"]) for j in jobs})
    report["sample_titles"]=[j.get("title") for j in jobs[:10]]
    report["hiring_countries"]=sorted({str(j.get("hiring_country")) for j in jobs})
    previous=json.loads((root/"jobs.json").read_text(encoding="utf-8"))["jobs"]
    retained=[j for j in previous if j.get("vendor")=="TELUS Digital" and j.get("status")!="archived"]
    report["retained_count"]=len(retained)
    report["retained_missing_from_api"]=len({j["source_id"] for j in retained}-{str(j["id"]) for j in jobs})
    report["new_ids"]=len({str(j["id"]) for j in jobs}-{j["source_id"] for j in retained})
    report["result"]="api_consistent" if len(jobs)==meta["total"] else "api_inconsistent"
except Exception as e:
    report["result"]="error"
    report["error"]=str(e)
out=root/"telus_count_diagnostic.json"
out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
if report["result"]=="error": sys.exit(1)
