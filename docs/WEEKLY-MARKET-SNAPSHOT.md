# Weekly Market Snapshot — approved architecture

Decision: 2026-11-27. Weekly Friday snapshots are the primary public Market Intelligence cadence, synchronized with the manual TELUS catalog capture. Daily RWS, Welo Data and Meridial collectors remain unchanged for the operational Job Intelligence Matrix.

## Observation model
- Preserve independent source observations and source timestamps (`last_successful_at`); do not count retained state as a new observation.
- Weekly key: ISO year/week (e.g. 2026-W48), UTC Friday as reference day.
- First prospective baseline: 2026-11-27 (2026-W48).
- A complete weekly snapshot requires a successful Friday observation for all four sources. Otherwise publish a partial snapshot with explicit missing/stale sources; never substitute zero or silently carry forward a previous observation.
- Finalize after the Friday TELUS capture and successful automatic source observations; exact cutoff and late-arrival revision policy remain implementation decisions.
- Preserve source observation timestamps, coverage, provenance and listing IDs for reproducibility. Compare only compatible source scopes.

## Metrics
Per vendor: observed listing count, additions/removals relative to the preceding comparable weekly snapshot (set differences, not confirmed hires or closures), net change, mapped countries and country associations, project-family distribution, coverage and freshness. Separate all catalog listings from classified AI-rating vacancies. Missing comparable baseline yields null, not zero. Daily event activity is distinct from weekly endpoint differences.

## History and publication
Retain all recovered historical observations; derive historical weekly points only where evidence supports them, explicitly label partial or non-Friday historical observations and scope breaks. Do not fabricate missing weeks. Monthly, quarterly and annual trends derive from weekly observations. Store durable snapshots and methodology in GitHub. Analytics runs independently of operational collection and must not block or modify the vacancy feed.

## Implementation status
Approved design, not yet deployed. Next: weekly aggregation, historical compatibility, source freshness and coverage tests, independent analytics workflow, then site publication.
