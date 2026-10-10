#!/usr/bin/env python3
"""Inspect geographic evidence in TELUS raw API responses without making assumptions."""
import collections,json,re
from collect_telus import collect
KEYS=re.compile(r"location|country|region|geo|eligib|residen|territor|market|remote|restrict",re.I)
def main():
 rows,_=collect()
 key_counts=collections.Counter()
 examples={}
 for row in rows:
  for key,val in row.items():
   if KEYS.search(key):
    key_counts[key]+=1
    examples.setdefault(key,[])
    if len(examples[key])<5: examples[key].append({"id":row.get("id"),"value":str(val)[:350]})
 print("RAW_GEO_FIELDS",json.dumps(dict(key_counts),ensure_ascii=False))
 print("RAW_GEO_SAMPLES",json.dumps(examples,ensure_ascii=False))
 print("LOCATION_COUNTS",json.dumps(dict(collections.Counter(str(r.get("location")) for r in rows)),ensure_ascii=False))
 print("DESCRIPTION_GEO_SNIPPETS")
 count=0
 for row in rows:
  desc=re.sub("<[^>]+>"," ",str(row.get("description") or ""))
  matches=list(re.finditer(r"(?i)\b(?:based in|resid(?:e|ing|ent)|located in|must live in|eligible countries|work from|country|countries|region|location|worldwide|globally|remote)\b",desc))
  if matches:
   excerpts=[desc[max(0,m.start()-80):m.end()+125].replace("\n"," ") for m in matches[:4]]
   print(json.dumps({"id":row.get("id"),"title":row.get("title"),"snippets":excerpts},ensure_ascii=False))
   count+=1
 print("DESCRIPTIONS_WITH_GEO_TERMS",count,"TOTAL",len(rows))
if __name__=="__main__":main()
