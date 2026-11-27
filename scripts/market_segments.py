CORE = {"Search Quality Rating","Ads Quality Rating","Internet Safety","Maps & Local","Media Search"}
EXTENDED = {"AI Training & Evaluation","Data Annotation & Collection","Speech & Audio","Translation & Localization"}
def segment(family):
    if family in CORE: return "Core AI Rating"
    if family in EXTENDED: return "Extended candidate"
    if family == "Talent Pool": return "Talent Pool"
    return "Unresolved"
