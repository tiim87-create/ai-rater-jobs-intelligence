import json,tempfile
from pathlib import Path
import collect_unified as c
from normalize_telus_manual import normalize

def test():
    with tempfile.TemporaryDirectory() as tmp:
        c.ROOT=Path(tmp)
        rows=[dict(page=1,title="Online Data Analyst - South Africa",url="https://jobs.telusdigital.com/jobs/1",fields=["","English","Part time","Req1"])]
        doc=dict(date="2026-11-27",reported_total=1,jobs=rows)
        c.save("telus_manual_latest.json",doc)
        c.save("jobs.json",{"jobs":[dict(id="TELUS:old",vendor="TELUS Digital",coverage="telus_ai_public_portal",status="active")]})
        c.fetch_rws=lambda *a:[{}]
        c.transform_rws=lambda x:dict(id="1",vendor="RWS",title="Test",url="https://example.com/rws",countries=["US"])
        c.validate_rws=lambda *a:([],None)
        c.lever=lambda *a:[dict(id="Welo:1",vendor="Welo Data",title="Test",url="https://example.com/welo",location_raw="United States")]
        c.fetch_meridial=lambda:[dict(id="Meridial:1",vendor="Meridial",title="Test",url="https://example.com/meridial")]
        def forbidden(): raise AssertionError("Old TELUS API called")
        c.fetch_telus=forbidden
        assert c.run()==0
        jobs=c.load("jobs.json",{})["jobs"]
        telus=[j for j in jobs if j["vendor"]=="TELUS Digital" and j["status"]=="active"]
        assert len(telus)==1 and telus[0]["countries"]==["ZA"]
        assert c.run()==0
        assert c.load("jobs.json",{})["jobs"]==jobs
        assert c.load("summary.json",{})["sources"]["TELUS Digital"]["status"]=="stale"
        print("PASS: manual source priority, repeat import, old API excluded")
if __name__=="__main__":test()
