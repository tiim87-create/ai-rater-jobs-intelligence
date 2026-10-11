#!/usr/bin/env python3
"""Idempotent, guarded publication polish for AI Rater Insider article 81."""
import base64
import json
import os
import pathlib
import urllib.request

URL = "https://timallen87-zwkba.wpcomstaging.com/wp-json/wp/v2/pages/81?context=edit"
user, password = os.environ["WP_USER"], os.environ["WP_APP_PASSWORD"]
auth = base64.b64encode(f"{user}:{password}".encode()).decode()
headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
def request(method, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    with urllib.request.urlopen(urllib.request.Request(URL, data=data, method=method, headers=headers), timeout=40) as resp:
        return json.load(resp)
page = request("GET")
original = page["content"]["raw"]
updated = original
def replace_once(old, new, label):
    global updated
    count = updated.count(old)
    if count == 0 and new in updated:
        print(f"Already applied: {label}")
        return
    if count != 1:
        raise RuntimeError(f"Unsafe match for {label}: {count}")
    updated = updated.replace(old, new, 1)
    print(f"Updated: {label}")

replace_once(
    '<h2>Why identity became an AI-quality problem</h2>',
    '<p><strong>Key findings:</strong> Identity verification, qualification and ongoing account integrity are separate controls. Public vendor materials establish some of their capabilities, but do not disclose universal detection thresholds. A quality review, temporary task shortage or account suspension is not proof of fraud. This article labels first-hand observations and unresolved hypotheses separately from documented vendor practices.</p>\n<h2>Why identity became an AI-quality problem</h2>',
    "reader summary",
)
replace_once(
    '<h3>Counterexample — A suspension unrelated to quality</h3>',
    '<h3>Case 4 — A suspension unrelated to quality</h3>',
    "case numbering",
)
replace_once(
    '<p><em>This article combines public vendor documentation, academic research and clearly labeled first-hand industry observations. Internal or confidential vendor material is not cited as public evidence. Additional cross-vendor evidence and a redacted TELUS onboarding visual will be considered before publication.</em></p>',
    '<p><em>Evidence standard: this article combines public vendor documentation, academic research and clearly labeled first-hand industry observations. A published TELUS Ads Assessor permissions screenshot documents one qualification flow, not a universal vendor policy. Undisclosed internal rules, detection thresholds and cross-vendor data sharing are not asserted as established facts.</em></p>',
    "outdated prepublication note",
)
replace_once(
    'Research in development. This article distinguishes public documentation, first-hand industry observations and analytical interpretation. Models and possible operational mechanisms should not be treated as verified internal client or vendor policies unless independently documented. Publication and content edits do not imply that every factual claim has been reverified.',
    'Version 1.0 · October 2026. This is a living research article. Public documentation, first-hand industry observations and analytical interpretation are labeled separately. Vendor controls may vary by project, country and date. Future additions will be incorporated as new evidence becomes available; a vendor capability must not be mistaken for a universally enabled policy.',
    "version and evidence notice",
)
replace_once(
    '<h2>Why human provenance matters</h2>\n<p>The long-term direction may be bigger than identity verification. As AI makes automation, synthetic identities and imitation of human work easier, frontier AI systems simultaneously need increasingly trustworthy human feedback.</p>\n<p>The important question therefore evolves from:</p>\n<blockquote>\n<p><strong>“Is this label correct?”</strong></p>\n</blockquote>\n<p>to:</p>\n<blockquote>\n<p><strong>“Who produced this judgment, were they qualified to produce it, was it genuinely produced by that human, and can its provenance be trusted?”</strong></p>\n</blockquote>\n<p>That is the emerging <strong>human provenance layer</strong> of AI evaluation.</p>\n<hr>',
    '<hr>',
    "duplicate provenance conclusion",
)
pathlib.Path("wp-page-backup.html").write_text(original, encoding="utf-8")
pathlib.Path("wp-page-preview.html").write_text(updated, encoding="utf-8")
if updated == original:
    print("No changes needed")
    raise SystemExit(0)
if request("GET")["content"]["raw"] != original:
    raise RuntimeError("Page changed during update; aborting")
result = request("POST", {"content": updated})
verified = request("GET")["content"]["raw"]
if "Version 1.0 · October 2026" not in verified:
    raise RuntimeError("Publication verification failed")
print("Published and verified:", result.get("link"), "length:", len(verified))
