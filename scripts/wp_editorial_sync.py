#!/usr/bin/env python3
"""Replace one managed section in an existing WordPress page, preserving other content."""
import os, sys, json, pathlib, urllib.request, urllib.error, base64, difflib, re
SITE = "https://timallen87-zwkba.wpcomstaging.com"
PAGE_ID = int(os.environ.get("WP_PAGE_ID", "81"))
SLUG = os.environ.get("BLOCK_SLUG", "vendor-antifraud-comparison")
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() != "false"
path = pathlib.Path("editorial/blocks") / (SLUG + ".html")
if not path.is_file(): sys.exit("Missing managed block: " + str(path))
block = path.read_text(encoding="utf-8").strip()
start = "<!-- AI-RATER-INSIDER:START " + SLUG + " -->"
end = "<!-- AI-RATER-INSIDER:END " + SLUG + " -->"
if start in block or end in block: sys.exit("Block file must not include management markers")
user, password = os.environ.get("WP_USER", ""), os.environ.get("WP_APP_PASSWORD", "")
if not user or not password: sys.exit("Set WP_USER and WP_APP_PASSWORD GitHub Actions secrets")
auth = base64.b64encode((user + ":" + password).encode()).decode()
url = SITE + "/wp-json/wp/v2/pages/" + str(PAGE_ID)
def request(method, data=None):
    payload = None if data is None else json.dumps(data).encode()
    headers = {"Authorization": "Basic " + auth, "Content-Type": "application/json", "Accept": "application/json"}
    with urllib.request.urlopen(urllib.request.Request(url + "?context=edit", data=payload, headers=headers, method=method), timeout=30) as resp:
        return json.load(resp)
page = request("GET")
original = page["content"]["raw"]
if original.count(start) != original.count(end) or original.count(start) > 1:
    sys.exit("Malformed or duplicated managed markers; refusing to update")
replacement = start + "\n" + block + "\n" + end
if SLUG == "ios-tables-style":
    if start in original:
        a = original.index(start); b = original.index(end, a) + len(end)
        updated = original[:a] + replacement + original[b:]
    else:
        updated = original + "\\n" + replacement
    # Scope the shared CSS to all tables in this article, without changing table data.
    updated = re.sub(r'<table(\\s|>)', r'<table class="ari-ios-table"\\1', updated) if False else updated
elif start in original:
    a = original.index(start); b = original.index(end, a) + len(end)
    updated = original[:a] + replacement + original[b:]
else:
    anchor = "<h2>Layer 1: Identity — are you really the applicant?</h2>"
    if original.count(anchor) != 1:
        sys.exit("Expected insertion anchor not found exactly once; refusing to update")
    updated = original.replace(anchor, replacement + "\n" + anchor, 1)
pathlib.Path("wp-page-backup.html").write_text(original, encoding="utf-8")
pathlib.Path("wp-page-preview.html").write_text(updated, encoding="utf-8")
print("Page:", PAGE_ID, "dry run:", DRY_RUN, "original length:", len(original), "updated length:", len(updated))
print("".join(list(difflib.unified_diff(original.splitlines(True), updated.splitlines(True), fromfile="before", tofile="after"))[:180]))
if updated == original: sys.exit(0)
if DRY_RUN:
    print("Dry run only. Review backup and preview artifacts before publishing.")
    sys.exit(0)
# Verify content did not change between read and write; no silent overwrites.
fresh = request("GET")
if fresh["content"]["raw"] != original: sys.exit("Page changed during run; aborting")
result = request("POST", {"content": updated})
if start not in result.get("content", {}).get("raw", ""):
    verified = request("GET")
    if start not in verified["content"]["raw"]: sys.exit("Update response did not confirm marker")
print("Published:", result.get("link", url))
