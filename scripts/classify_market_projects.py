import re
VERSION = "1.0"
def classify(job):
    t = re.sub(r"[^\w]+", " ", job.get("title","").casefold())
    v = job.get("vendor","")
    rules = [
        ("Ads Quality Rating", r"\b(ads quality|ads assessor|ad quality|ads evaluator)\b"),
        ("Internet Safety", r"\binternet safety\b"),
        ("Maps & Local", r"\b(maps analyst|maps evaluator|maps personalization|maps relevance)\b"),
        ("Media Search", r"\bmedia search analyst\b"),
        ("Search Quality Rating", r"\b(search engine evaluator|search quality rater|search quality evaluator|personalized internet assessor)\b"),
    ]
    if v == "TELUS Digital":
        rules += [("Search Quality Rating",r"\bcontent reviewer\b"),("Internet Safety",r"\bcontent evaluator\b"),("Maps & Local",r"\bonline data analyst\b")]
    if v == "RWS":
        rules += [("Search Quality Rating",r"\bcallisto rater\b")]
    if v == "Welo Data":
        rules += [("Search Quality Rating",r"\bscout rater\b")]
    rules += [
        ("Speech & Audio",r"\b(speech ai evaluation|audio evaluation|voice recording|speech data|audio transcription)\b"),
        ("Translation & Localization",r"\b(translation|localization|localisation|translator)\b"),
        ("Data Annotation & Collection",r"\b(data annotation|data labeling|data labelling|data collection|image collection)\b"),
        ("AI Training & Evaluation",r"\b(ai trainer|ai training|ai response evaluator|ai data specialist|ai evaluator|prompt engineer|subject matter expert)\b"),
    ]
    for family,pattern in rules:
        if re.search(pattern,t):
            return family
    return "Other / Unclassified"
