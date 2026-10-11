#!/usr/bin/env python3
"""Migrate referenced legacy WordPress images to AI Rater Insider.

Dry-run by default. Only URLs in editorial/pages/*.html are considered.
Requires WP_USER and WP_APP_PASSWORD for --apply. No source-site credentials.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, unquote
from urllib.request import Request, urlopen
from urllib.error import HTTPError

SOURCE_HOST = "leapforceexamhelp.wordpress.com"
TARGET = "https://timallen87-zwkba.wpcomstaging.com"
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "editorial" / "media-migration.json"
PAGES = ROOT / "editorial" / "pages"
PATTERN = re.compile(r'https://(?:i[0-9]\.wp\.com/)?leapforceexamhelp\.wordpress\.com/wp-content/uploads/[^"\'<>\s]+', re.I)

def fetch(url, headers=None, data=None, method=None):
    request = Request(url, data=data, headers=headers or {}, method=method)
    with urlopen(request, timeout=75) as response:
        return response.read(), dict(response.headers)

def source_url(url):
    parts = urlsplit(url.replace("&amp;", "&"))
    path = parts.path
    if parts.hostname and re.fullmatch(r"i[0-9]\.wp\.com", parts.hostname):
        path = "/" + path.lstrip("/").split("/", 1)[1]
    return "https://" + SOURCE_HOST + path

def auth_headers():
    user = os.environ["WP_USER"]
    password = os.environ["WP_APP_PASSWORD"]
    token = base64.b64encode((user + ":" + password).encode()).decode()
    return {"Authorization": "Basic " + token}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Upload and replace links")
    parser.add_argument("--allow-sensitive", action="store_true", help="Allow all legacy images; only use after checking ID masking/cropping")
    args = parser.parse_args()
    mapping = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    pages = sorted(PAGES.glob("*.html"))
    pending = {}
    for page in pages:
        for match in PATTERN.findall(page.read_text()):
            canonical = source_url(match)
            pending.setdefault(canonical, []).append(page.name)
    print(json.dumps({"found": len(pending), "already_mapped": sum(k in mapping for k in pending), "files": pending}, indent=2))
    if not args.apply:
        return
    if not args.allow_sensitive:
        print("Refusing to upload screenshots before explicit review. Use --allow-sensitive after verifying redactions/crops.", file=sys.stderr)
        sys.exit(2)
    headers = auth_headers()
    for old in sorted(pending):
        if old in mapping:
            continue
        try:
            payload, metadata = fetch(old)
            mime = metadata.get("Content-Type", "application/octet-stream").split(";")[0]
            if not mime.startswith("image/"):
                raise ValueError("Not an image: " + mime)
            filename = unquote(urlsplit(old).path.rsplit("/", 1)[-1])
            digest = hashlib.sha256(payload).hexdigest()[:12]
            upload_headers = dict(headers, **{"Content-Type": mime, "Content-Disposition": 'attachment; filename="' + digest + "-" + filename.replace('"', "") + '"'})
            result, _ = fetch(TARGET + "/wp-json/wp/v2/media", upload_headers, payload, "POST")
            media = json.loads(result)
            mapping[old] = {"url": media["source_url"], "media_id": media["id"], "sha256": hashlib.sha256(payload).hexdigest()}
            MANIFEST.parent.mkdir(parents=True, exist_ok=True)
            MANIFEST.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n")
            print("Uploaded", old, "=>", media["source_url"])
        except (HTTPError, OSError, ValueError, KeyError) as error:
            print("FAILED", old, str(error), file=sys.stderr)
    for page in pages:
        html = page.read_text()
        new_html = PATTERN.sub(lambda m: mapping.get(source_url(m.group()), {}).get("url", m.group()), html)
        if new_html != html:
            page.write_text(new_html)
            print("Updated", page)
    print("Review changes and publish through existing editorial workflow; this script does not update WordPress pages.")

if __name__ == "__main__":
    main()
