import json
from pathlib import Path
from datetime import datetime,timezone
from normalize_telus_manual import normalize
DATA=Path(__file__).resolve().parents[1]/"data"
def read(n): return json.loads((DATA/n).read_text())
def write(n,d): (DATA/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
def main():
    doc=normalize(read("telus_manual_latest.json"))
    assert all(j["countries"] for j in doc["jobs"])
    jobs=read("jobs.json"); summary=read("summary.json"); history=read("history.json")
    prior=summary["sources"].get("TELUS Digital",{})
    if prior.get("snapshot_date","")>=doc["date"]:
        print("Already imported or older snapshot"); return
    now=datetime.now(timezone.utc).isoformat()
    state={j["id"]:j for j in jobs["jobs"]}
    seen={j["id"] for j in doc["jobs"]}
    oldmanual=[j for j in state.values() if j.get("coverage")=="telus_ai_community_manual"]
    if oldmanual and len(seen)<0.65*sum(j["status"]=="active" for j in oldmanual):
        raise ValueError("Unexpected count drop")
    for j in doc["jobs"]:
        old=state.get(j["id"],{})
        if not old or old.get("status")=="archived":
            history["events"].append(dict(at=now,id=j["id"],type=("reopened" if old else "new" if oldmanual else "baseline")))
        state[j["id"]]={**old,**j,"first_seen":old.get("first_seen",now),"last_seen":now,"missed_complete_scans":0}
    for j in state.values():
        if j["vendor"]!="TELUS Digital" or j["id"] in seen or j["status"]=="archived": continue
        if j.get("coverage")!="telus_ai_community_manual":
            j.update(status="archived",archive_reason="source_scope_superseded")
        else:
            misses=j.get("missed_complete_scans",0)+1
            j.update(missed_complete_scans=misses,status="archived" if misses>=2 else "needs_recheck")
            if misses==2: history["events"].append(dict(at=now,id=j["id"],type="archived"))
    jobs.update(generated_at=now,jobs=sorted(state.values(),key=lambda j:j["id"]))
    summary["generated_at"]=now
    summary["sources"]["TELUS Digital"]=dict(status="ok",count=len(seen),coverage="telus_ai_community_manual",snapshot_date=doc["date"],last_successful_at=now)
    for n,d in [("jobs.json",jobs),("summary.json",summary),("history.json",history)]: write(n,d)
    print("Published TELUS",len(seen))
if __name__=="__main__":main()
