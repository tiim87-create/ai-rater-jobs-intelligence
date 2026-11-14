# AI Rater Insider — Unified Article Design Standard v2.0

**Adopted:** 2026-11-14
**Status:** Canonical for all new and revised editorial pages
**Scope:** Knowledge, Research, Projects, Vendors, Onboarding Lab, and other long-form WordPress pages.
**Related:** ../../EDITORIAL_STANDARDS.md; DESIGN_SYSTEM.md; ../CARD_DESIGN_STANDARD.md; ../EDITORIAL_ATTRIBUTION_STANDARD.md

## 1. Single source of truth
This document is the implementation contract for editorial page appearance. Existing design documents remain useful for rationale; where older numeric recommendations conflict, **this standard takes precedence for article components**. All new editorial pages and substantive revisions MUST use the shared component classes and tokens. Do not introduce page-specific visual systems (such as ari-research-v1 versus ari-nta-v1) for the same component.

## 2. Tokens
Use theme-level or shared-stylesheet CSS variables, with these fallback values:
- `--ari-bg: #ffffff`; `--ari-subtle: #f7f8fa`
- `--ari-text: #1d2939`; `--ari-heading: #0f172a`; `--ari-muted: #667085`
- `--ari-border: #e2e8f0`; `--ari-accent: #2563eb`
- `--ari-radius-card: 12px`; `--ari-radius-control: 10px`
- `--ari-shadow: 0 2px 12px rgba(15,23,42,.035)`
- `--ari-space: 8px`
Use blue for links, focus, compact numeric eyebrows, and key data emphasis—not colored card borders or decorative badges. Default links are not underlined; show underline on hover/focus with a visible keyboard focus ring.

## 3. Layout and type
- Main long-form content wrapper: `.ari-article`, max-width **920px**, width 100%, centered. Wide data tables/charts can extend to **1100px** via a reusable wide component, without altering body measure.
- Eyebrow: 11–12px, semibold/bold, uppercase, subtle tracking, blue.
- Intro/lead: 17–19px, muted, max-width 820px.
- Body: 16px, line-height ~1.7–1.8, dark text; paragraphs with 16–20px bottom spacing.
- H2: responsive 24–30px, line-height ~1.25, margin-top ~44–52px; H3: ~20px, clear subordinate spacing. Use one WordPress post title/H1; no duplicate H1 in article body.
- Whitespace and hierarchy over decoration. Avoid excessive banners, nested colored panels, and badge-heavy layouts.

## 4. Shared component contract
**Cards:** `.ari-card` = white surface, 1px solid var(--ari-border), 12px radius, **24px padding**, 12–16px gap, no colored top stripe. Optional compact eyebrow → heading → brief body → metadata/link. Consistent height where grid calls for it. On narrow screens use 20px padding.

**Card grid:** `.ari-card-grid` uses responsive grid: 3 columns only when cards have enough room (min-width about 220px), 2 on medium screens, 1 on phones. Five-stage frameworks should appear 3+2 / 2+2+1 / stacked, never five narrow columns.

**Metrics:** `.ari-metric` uses the same card surface, with restrained numeric emphasis, descriptive label, unit, period and scope. Do not style uncertainty as a verified success/warning badge.

**Tables:** `.ari-table-wrap` has 1px neutral border, 12px radius, horizontal overflow on phones. Semantic `table`/`thead`/`th scope="col"`/`tbody`, muted header, row separators, readable 13–14px type. Never shrink to unreadability.

**Images/charts:** `.ari-figure` has consistent neutral border/radius and responsive media; use meaningful alt, visible caption, source/date/scope and whether original, redacted, or illustrative. Graph values should be accessible in prose/table.

**Evidence notes:** `.ari-note` uses neutral subtle surface and border, not colorful status boxes; explicitly label Verified, Corroborated, First-hand, Inference, or Unverified in text when needed.

**Jump navigation:** `.ari-jump-nav` uses plain accessible links to semantic heading IDs; it may be omitted on short articles. Do not use decorative cards in place of content.

**Research methodology:** shared `.ari-methodology` with source, coverage, unit of measurement, missing data, limitations, last-reviewed date.

## 5. Editorial structures
- Knowledge / Research: reader question and key finding → evidence and interpretation → practical meaning → limitations/methodology → dated sources → relevant internal links. Use natural headings rather than forcing a generic numbered report, except when a numbered analytical framework itself is the subject.
- Projects: actual rater work → project/client/vendor/platform → tasks → qualification and quality → markets and work terms → sources and related pages.
- Vendors: role and history → project relationships → recruitment/contract/pay → evidence and related pages.
- Onboarding: reader task → practical stages → verification, risks and boundaries → sources.
Preserve useful original material, sources, URLs, and unique visualizations.

## 6. Gutenberg and deployment
Prefer shared WordPress theme/global CSS and registered Gutenberg patterns, not per-post `<style>` blocks. Reusable HTML fallback is allowed temporarily only when a shared pattern cannot express the content; it must use the canonical classes/tokens, have valid Gutenberg serialization and be tracked for migration. CSS source belongs in GitHub. Keep CSS scoped to `.ari-article` or component class; do not change all WordPress tables/site elements globally without QA.

## 7. Accessibility and responsiveness (required)
Check desktop, tablet, phone portrait and landscape; no clipped content. Keyboard-visible focus, accessible link names, sufficient contrast, meaningful headings, non-color-only status, table headers, alt text, and tap targets. Check actual WordPress front-end and editor, including dark/light theme where applicable. Code inspection alone is not visual QA.

## 8. Evidence and SEO (required)
Apply EDITORIAL_STANDARDS.md and EDITORIAL_ATTRIBUTION_STANDARD.md: cite material claims near their text, distinguish operational data from inference, protect personnel and confidential source material. One canonical topic/page, descriptive headings, meta description, meaningful internal cross-links, no fake sources or filler. Do not publish placeholders or duplicate research summaries.

## 9. Definition of done
For every article: (1) content/evidence reviewed; (2) shared tokens/classes used; (3) no custom parallel card/table design; (4) responsive visual check; (5) editor serialization check; (6) link and media check; (7) metadata and related reading; (8) status and revision logged. A saved CSS string alone does NOT count as a passed visual QA.

## 10. Migration and governance
- New articles: mandatory immediately.
- Existing published pages: inventory and migrate **one page at a time**, preserving content and URLs; take backup, preview, QA, then update. Never bulk-overwrite all pages without review.
- Initial known migration candidates: post 958 (Geographic Redistribution, `ari-research-design-v1`), post 826 (RaterHub NTA, `ari-nta-research-v1`). Both have local CSS and should move to shared `.ari-article` components.
- Changes to the design contract require a GitHub revision with version, date, rationale, and compatibility notes. Avoid silent page-specific exceptions.

**Changelog:** v2.0 (2026-11-14) — Consolidated editorial, card, token, responsive and QA requirements into one mandatory cross-site article standard.
