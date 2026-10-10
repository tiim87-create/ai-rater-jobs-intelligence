#!/usr/bin/env python3
"""Unified vendor collection: source failures preserve old records; two misses archive."""
import datetime as dt,json,pathlib,sys
from collect import lever
from collect_rws import fetch as fetch_rws,transform as transform_rws,validate as validate_rws
from collect_telus import collect as fetch_telus,transform as transform_telus
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
def run():
 existing=load("jobs.json",{"jobs":[]})
 state={j["id"]:j for j in existing["jobs"]}
 history=load("history.json",{"events":[]}).get("events",[])
 summary={}
 def ingest(vendor,items,coverage):
  previous={k:v for k,v in state.items() if v.get("vendor")==vendor}
  if not items or len({x["id"] for x in items})!=len(items): raise ValueError("Empty/duplicate source")
  if previous and len(items)<max(5,int(len(previous)*0.65)): raise ValueError("Unexpected source count drop")
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
  summary[vendor]={"status":"ok","count":len(items),"coverage":coverage}
 try:
  raw=fetch_rws("rws")
  mapped=[transform_rws(x) for x in raw]
  prior=[x for x in state.values() if x.get("vendor")=="RWS" and x.get("status")=="active"]
  errors,_=validate_rws(mapped,prior,1,.20,.35)
  if errors: raise ValueError("; ".join(errors))
  normalized=[]
  for j in mapped:
   codes=j["countries"]
   normalized.append({**j,"id":"RWS:"+j["id"],"source_id":j["id"],"category":"RWS","country":", ".join(codes) if codes else "Unmapped","coverage":"full_board","source":"https://api.lever.co/v0/postings/rws?mode=json"})
  ingest("RWS",normalized,"full_board")
 except Exception as e: summary["RWS"]={"status":"error","error":str(e)[:200]}
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
 try:
  raw,_=fetch_telus()
  jobs=[transform_telus(x,NOW) for x in raw]
  ingest("TELUS Digital",jobs,"telus_ai_public_portal")
 except Exception as e: summary["TELUS Digital"]={"status":"error","error":str(e)[:200]}
 if any(v["status"]=="error" for v in summary.values()):
  print(json.dumps(summary),file=sys.stderr)
  return 1
 output=sorted(state.values(),key=lambda j:j["id"])
 assert len(output)==len(set(j["id"] for j in output))
 save("jobs.json",{"generated_at":NOW,"jobs":output})
 save("history.json",{"events":history[-10000:]})
 save("summary.json",{"generated_at":NOW,"sources":summary})
 print(json.dumps(summary))
 return 0
if __name__=="__main__":sys.exit(run())
