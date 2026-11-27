import re
VERSION = "1.1"
def classify(job):
    t = re.sub(r"[^\w]+", " ", job.get("title","").casefold())
    v = job.get("vendor","")
    if re.search(r"\b(talent pool|future opportunities)\b",t):
        return "Talent Pool"
    rules = [
        ("Ads Quality Rating", r"\b(ads quality|ads assessor|ad quality|ads evaluator)\b"),
        ("Internet Safety", r"\binternet safety\b"),
        ("Maps & Local", r"\b(maps analyst|maps evaluator|maps personalization|maps relevance)\b"),
        ("Media Search", r"\bmedia search analyst\b"),
        ("Search Quality Rating", r"\b(search engine evaluator|search quality rater|search quality evaluator|personalized internet assessor)\b"),
    ]
    if v == "TELUS Digital":
        rules += [("Search Quality Rating",r"\b(content reviewer|us raters)\b"),("Internet Safety",r"\bcontent evaluator\b"),("Maps & Local",r"\bonline data analyst\b")]
    if v == "RWS":
        rules += [("Search Quality Rating",r"\bcallisto rater\b")]
    if v == "Welo Data":
        rules += [("Search Quality Rating",r"\bscout rater\b")]
    rules += [
        ("Speech & Audio",r"\b(speech ai evaluation|audio evaluation|voice recording|speech data|audio transcription|audio recording|voice contributor|voice actor|ai conversation recording contributor)\b"),
        ("Translation & Localization",r"\b(translation|localization|localisation|translator|linguist|review lead for ui)\b"),
        ("Data Annotation & Collection",r"\b(data annotation|data labeling|data labelling|data collection|image collection|legal annotators|video recording)\b"),
        ("AI Training & Evaluation",r"\b(ai trainers?|ai qa trainer|ai generalist|ai linguistic quality evaluator|ai linguistic evaluator|linguistic ai auditor|ai data quality rater|ai training|ai response evaluator|ai data specialist|ai evaluator|prompt engineer|subject matter expert)\b"),
    ]
    for family,pattern in rules:
        if re.search(pattern,t):
            return family
    return "Other / Unclassified"
