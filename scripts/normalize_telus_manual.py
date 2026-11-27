import json, sys, re
from collections import Counter
from pathlib import Path
from collect_telus import COUNTRY_CODES

CODES={k.casefold():v for k,v in COUNTRY_CODES.items()}
CODES.update({"el salvador":"SV","tanzania, united republic of":"TZ","kyrgyzstan":"KG","korea, republic of":"KR"})
def normalize(doc):
    rows=doc["jobs"]
    if len(rows)!=doc["reported_total"] or not rows:
        raise ValueError("Incomplete snapshot")
    result=[]
    for row in rows:
        location,language,employment,req=row["fields"]
        if not req or not row["title"] or not row["url"].startswith("https://jobs.telusdigital.com/jobs/"):
            raise ValueError("Invalid listing")
        raw=location.strip().casefold()
        code=next((v for k,v in sorted(CODES.items(),key=lambda x:-len(x[0])) if raw==k or raw.endswith(", "+k)),None)
        evidence="location"
        if not raw:
            matches={v for k,v in CODES.items() if re.search(r"(?<!\w)"+re.escape(k)+r"(?!\w)",row["title"].casefold())}
            if len(matches)==1:
                code=matches.pop()
                evidence="title"
        result.append({"id":"TELUS-CAREERS:"+req,"source_id":req,"job_req_id":req,"vendor":"TELUS Digital","category":"TELUS Digital","title":row["title"],"url":row["url"],"location_raw":location,"language":language,"employment_type":employment,"countries":[code] if code else [],"country":code,"geography_status":"mapped" if code else "unmapped","geography_evidence":evidence if code else None,"coverage":"telus_ai_community_manual","source":"https://jobs.telusdigital.com/search/cfm5/ai-community/jobs/in","status":"active","source_page":row["page"]})
    for key in ("id","url"):
        if len({r[key] for r in result})!=len(result): raise ValueError("Duplicate "+key)
    return {"date":doc["date"],"reported_total":doc["reported_total"],"jobs":result}
if __name__=="__main__":
    doc=normalize(json.loads(Path(sys.argv[1]).read_text()))
    Path(sys.argv[2]).write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
    print(Counter(r["geography_status"] for r in doc["jobs"]))
