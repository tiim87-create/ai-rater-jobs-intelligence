#!/usr/bin/env python3
"""Recover verified historical snapshots from local Git history (full clone required)."""
import json
import subprocess
from pathlib import Path
from build_market_snapshots import build_snapshot

ROOT = Path(__file__).resolve().parents[1]
def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True)
def read_at(commit, name):
    return json.loads(git("show", f"{commit}:data/{name}"))
def main():
    if git("rev-parse", "--is-shallow-repository").strip() == "true":
        raise RuntimeError("Full Git history required")
    commits = git("log", "--first-parent", "--reverse", "--format=%H", "origin/main", "--", "data/jobs.json").splitlines()
    path = ROOT / "data/market_snapshots.json"
    archive = json.loads(path.read_text()) if path.exists() else {"schema_version":1,"snapshots":[]}
    existing = {s["at"]:s for s in archive["snapshots"]}
    skipped = []
    for commit in commits:
        try:
            jobs = read_at(commit,"jobs.json")
            summary = read_at(commit,"summary.json")
            history = read_at(commit,"history.json")
            if jobs["generated_at"] != summary["generated_at"]:
                raise ValueError("Mismatched timestamps")
            if not isinstance(jobs["jobs"],list) or not jobs["jobs"]:
                raise ValueError("Empty feed")
            if not summary["sources"] or any(s["status"] not in ("ok","stale","warning") for s in summary["sources"].values()):
                raise ValueError("Unverified sources")
            s = build_snapshot(jobs["jobs"],summary,history["events"])
            if s["at"] not in existing:
                s["provenance"] = {"kind":"historical_git","commit":commit}
                s["legacy_event_semantics"] = True
                existing[s["at"]] = s
        except (KeyError,TypeError,ValueError,subprocess.CalledProcessError) as e:
            skipped.append({"commit":commit,"reason":str(e)})
    archive["snapshots"] = sorted(existing.values(),key=lambda s:s["at"])
    path.write_text(json.dumps(archive,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"snapshots":len(existing),"skipped":skipped},indent=2))
if __name__ == "__main__":
    main()
