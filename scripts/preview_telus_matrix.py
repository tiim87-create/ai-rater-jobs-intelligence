#!/usr/bin/env python3
"""Stage TELUS snapshot into a COPY of the multi-vendor feed; never write jobs.json."""
import argparse,datetime as dt,json,pathlib
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--existing",default="data/jobs.json")
 p.add_argument("--telus",default="data/telus_jobs_test.json")
 p.add_argument("--output",default="data/jobs_telus_preview.json")
 a=p.parse_args()
 existing=json.loads(pathlib.Path(a.existing).read_text(encoding="utf-8"))
 telus=json.loads(pathlib.Path(a.telus).read_text(encoding="utf-8"))
 old=existing["jobs"]; fresh=telus["jobs"]
 if not isinstance(old,list) or not isinstance(fresh,list) or len(fresh)<10: raise ValueError("Unexpected feed")
 if len({j["id"] for j in fresh})!=len(fresh): raise ValueError("Duplicate TELUS IDs")
 if any(j.get("vendor")!="TELUS Digital" or not j.get("url") or not j.get("title") for j in fresh): raise ValueError("Invalid TELUS record")
 prior={j["id"]:j for j in old if j.get("vendor")=="TELUS Digital"}
 now=dt.datetime.now(dt.timezone.utc).isoformat()
 updated=[]
 for item in fresh:
  before=prior.get(item["id"],{})
  record={**before,**item}
  record["first_seen"]=before.get("first_seen",now)
  record["last_seen"]=now
  updated.append(record)
 retained=[j for j in old if j.get("vendor")!="TELUS Digital"]
 if len(retained)!=len([j for j in old if j.get("vendor")!="TELUS Digital"]): raise ValueError("Retention failure")
 combined=retained+updated
 if len({j["id"] for j in combined})!=len(combined): raise ValueError("Cross-vendor duplicate ID")
 out={"generated_at":now,"jobs":sorted(combined,key=lambda j:j["id"])}
 dest=pathlib.Path(a.output)
 if dest.resolve()==pathlib.Path(a.existing).resolve(): raise ValueError("Refusing to overwrite production")
 dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"result":"ok","existing_total":len(old),"existing_other_vendors":len(retained),"telus_added":len(updated),"preview_total":len(combined),"output":str(dest)},ensure_ascii=False))
if __name__=="__main__":main()
