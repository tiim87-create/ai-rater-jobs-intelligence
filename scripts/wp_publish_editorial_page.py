#!/usr/bin/env python3
"""Publish versioned editorial pages from GitHub to WordPress, with a drift guard."""
import base64
import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = "https://timallen87-zwkba.wpcomstaging.com/wp-json/wp/v2/pages"
PAGES = {
    "11": "editorial/pages/google-search-quality-rating-general-pool.html",
    "28": "editorial/pages/projects.html",
    "81": "editorial/pages/ai-rater-identity-verification-antifraud.html",
}
page_id = os.environ["WP_PAGE_ID"]
if page_id not in PAGES:
    raise SystemExit("Unrecognized page ID")
source = Path(PAGES[page_id]).read_text(encoding="utf-8")
token = base64.b64encode((os.environ["WP_USER"] + ":" + os.environ["WP_APP_PASSWORD"]).encode()).decode()
headers = {"Authorization": "Basic " + token, "Content-Type": "application/json"}
url = ROOT + "/" + page_id
def api(method, payload=None):
    body = json.dumps(payload).encode() if payload is not None else None
    with urlopen(Request(url + "?context=edit", data=body, headers=headers, method=method), timeout=45) as resp:
        return json.load(resp)
page = api("GET")
live = page["content"]["raw"]
if live == source:
    print("Already synchronized:", page_id)
    raise SystemExit(0)
# Fail closed if the live page was changed outside GitHub after its last known publication.
state_path = Path("editorial/state") / (page_id + ".sha256")
if not state_path.exists():
    raise SystemExit("Missing baseline. Explicit reconciliation required before publishing.")
expected = state_path.read_text().strip()
actual = hashlib.sha256(live.encode()).hexdigest()
if actual != expected:
    raise SystemExit("WordPress drift detected: refusing to overwrite untracked edits.")
if os.environ.get("DRY_RUN", "true").lower() != "false":
    print("Dry run: content differs; safe to publish after approval.")
    raise SystemExit(0)
updated = api("POST", {"content": source})
if updated["content"]["raw"] != source:
    raise SystemExit("WordPress modified the submitted content; inspect the saved page.")
print("Published page:", page_id, updated["link"])
