#!/usr/bin/env python3
"""Unified vendor collection: source failures preserve old records; two misses archive."""
import datetime as dt,json,pathlib,sys
from collect import lever
from collect_rws import fetch as fetch_rws,transform as transform_rws,validate as validate_rws
from collect_meridial import collect as fetch_meridial
ROOT=pathlib.Path(__file__).resolve().parents[1]/"data"
NOW=dt.datetime.now(dt.timezone.utc).isoformat()
def load(name,default):
 p=ROOT/name
 return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default
def save(name,obj):
 p=ROOT/name
 tmp=p.with_suffix(".tmp")
 tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 tmp.replace(p)
def run(selected=None):
 existing=load("jobs.json",{"jobs":[]})
 state={j["id"]:j for j in existing["jobs"]}
 history=load("history.json",{"events":[]}).get("events",[])
 summary=load("summary.json",{}).get("sources",{})
 selected=set(selected or ['RWS','Welo Data','Meridial'])
 def ingest(vendor,items,coverage):
  previous={k:v for k,v in state.items() if v.get("vendor")==vendor}
  if not items or len({x["id"] for x in items})!=len(items): raise ValueError("Empty/duplicate source")
  prior_count=sum(j.get("status")=="active" for j in previous.values())
  if prior_count and len(items)<min(prior_count,max(5,int(prior_count*0.65))): raise ValueError("Unexpected source count drop")
  seen=set()
  for item in items:
   ident=item["id"];seen.add(ident)
   old=state.get(ident,{})
   if vendor=="Welo Data" and old.get("location_raw")==item.get("location_raw") and old.get("countries"):
    item["countries"]=old["countries"]
    item["geography_status"]=old.get("geography_status","mapped")
   merged={**old,**item,"first_seen":old.get("first_seen",NOW),"last_seen":NOW,"status":"active","missed_complete_scans":0}
   if not old: history.append({"at":NOW,"type":"new","id":ident})
   elif any(old.get(k)!=merged.get(k) for k in ("title","url","countries","location_raw","country")):
    history.append({"at":NOW,"type":"changed","id":ident})
   state[ident]=merged
  for ident,old in previous.items():
   if ident in seen or old.get("status")=="archived": continue
   missed=int(old.get("missed_complete_scans") or 0)+1
   old["missed_complete_scans"]=missed
   old["status"]="archived" if missed>=2 else "needs_recheck"
   if missed==2: history.append({"at":NOW,"type":"archived","id":ident})
  summary[vendor]={"status":"ok","count":len(items),"coverage":coverage,"last_successful_at":NOW}
 if "RWS" in selected:
  try:
   raw=fetch_rws("rws")
   mapped=[transform_rws(x) for x in raw]
   prior=[x for x in state.values() if x.get("vendor")=="RWS" and x.get("status")=="active"]
   errors,_=validate_rws(mapped,prior,1,.20,.35)
   geography_warnings=[e for e in errors if e=="Unmapped share exceeds threshold"]
   fatal_errors=[e for e in errors if e not in geography_warnings]
   if fatal_errors: raise ValueError("; ".join(fatal_errors))
   normalized=[]
   for j in mapped:
    codes=j["countries"]
    normalized.append({**j,"id":"RWS:"+j["id"],"source_id":j["id"],"category":"RWS","country":", ".join(codes) if codes else "Unmapped","coverage":"full_board","source":"https://api.lever.co/v0/postings/rws?mode=json"})
   ingest("RWS",normalized,"full_board")
   if geography_warnings:
    summary["RWS"]["warning"]="Unmapped geography exceeds 20%; records retained without inferred countries"
    summary["RWS"]["unmapped_count"]=sum(not j["countries"] for j in mapped)
  except Exception as e: summary["RWS"]={"status":"error","error":str(e)[:200]}
 if "Welo Data" in selected:
  try:
   jobs=lever("Welo Data","weloglobal")
   # Keep historic enriched geography if source location has not changed.
   from collect_rws import country as infer_country
   for j in jobs:
    code=infer_country(j.get("location_raw"))
    j["countries"]=[code] if code else []
    j["geography_status"]="mapped" if code else "unmapped"
    j["status"]="active"
   ingest("Welo Data",jobs,"full_board")
  except Exception as e: summary["Welo Data"]={"status":"error","error":str(e)[:200]}
 # TELUS is maintained by its independent publication workflow.
 summary["TELUS Digital"]=load("summary.json",{}).get("sources",{}).get("TELUS Digital",{"status":"stale","coverage":"telus_ai_community_manual"})
 if "Meridial" in selected:
  try:
   jobs=fetch_meridial()
   ingest("Meridial",jobs,"full_board")
  except Exception as e:
   # Keep existing vendors publishing when this new Greenhouse source is unavailable.
   summary["Meridial"]={"status":"warning","error":str(e)[:200],"coverage":"unavailable"}
 for vendor in selected:
  if summary[vendor]["status"] in ("error","warning") and "error" in summary[vendor]:
   prior=load("summary.json",{}).get("sources",{}).get(vendor,{})
   summary[vendor]={**prior,**summary[vendor],"status":"stale","last_attempt_at":NOW}
 output=sorted(state.values(),key=lambda j:j["id"])
 assert len(output)==len(set(j["id"] for j in output))
 save("jobs.json",{"generated_at":NOW,"jobs":output})
 save("history.json",{"events":history})
 save("summary.json",{"generated_at":NOW,"sources":summary})
 print(json.dumps(summary))
 return 0
if __name__=="__main__":sys.exit(run(sys.argv[1:]))
