# TELUS Digital AI Community: source integration decision (2026-11-22)

## Verified evidence
- Official AI Community catalog: https://jobs.telusdigital.com/search/cfm5/ai-community/jobs (78 positions shown in browser-accessible listing at investigation time; dynamic count).
- Separate public TELUS AI API: https://api.telusinternational.ai/apapi/v1/list-job-posts (31 unique positions, page 1/1, total 31 at 2026-11-22 08:16 UTC).
- GitHub-hosted HTML collector against the official catalog returned HTTP 403 on page 1 in run 45002168332. This is an access refusal, not a parsing/pagination failure.
- The two sources have different scopes; neither can substitute for the other without an ID-level comparison.
- The production collector retains the last valid TELUS snapshot as stale when a count anomaly occurs. Other vendors continue publishing.

## Decision
Do not circumvent the 403 with spoofed identities, proxies or unauthorized endpoints. Keep the official AI Community catalog as a distinct source with coverage=ai_community and provenance=official_career_site. Keep the public API as coverage=telus_ai_public_portal. Do not add their counts.

## Safe next ingestion path
1. Obtain an authorized structured export or official API access for the AI Community catalog, or manually archive the four public results pages as HTML for offline parsing.
2. Parse candidate records into a separate file; preserve original job IDs (ReqEG, Req_, numeric), canonical URLs, title, locale and country evidence.
3. Compare against existing TELUS records by verified requisition ID or canonical URL only; never merge by title alone.
4. Validate count, pagination, ID uniqueness, geography and links; publish only after a complete scan.
5. Mark absent records as closed only after two complete scans of the *same* source, never across source families.
6. Record retrieval method, timestamp, count, and source scope in summary.json.

## Current status
Official catalog integration is **blocked pending an authorized machine-readable feed or offline snapshots**. Production data is intentionally unchanged. A successful HTTP response to the API does not prove completeness of the separate AI Community career catalog.
