# AI Rater Insider — Design System

**Version:** 1.0 (2026-10-11)  
**Status:** Approved direction; individual components require WordPress visual QA before site-wide rollout.  
**Canonical editorial policy:** [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md)

## Design principles
- Premium minimal, Apple/iOS-inspired, editorial and evidence-first; not a pixel-for-pixel copy of Apple UI.
- Consistent across Projects, Vendors, Knowledge, Jobs Matrix and deep research pages.
- Clear typography, whitespace, quiet neutral colors, restrained blue focus/interactive accents.
- Responsive and accessible; no content hidden behind decorative interaction.
- Prefer reusable CSS classes and WordPress theme styles over per-article inline overrides.

## Design tokens (proposed baseline)
| Token | Value | Usage |
|---|---|---|
| `--ari-bg` | `#ffffff` | Content surface |
| `--ari-subtle` | `#f7f8fa` | Secondary surface, table header |
| `--ari-text` | `#1d2939` | Primary text |
| `--ari-muted` | `#667085` | Supporting metadata |
| `--ari-border` | `#e5e7eb` | Hairline borders |
| `--ari-accent` | `#2563eb` | Links/focus/selection |
| `--ari-radius-card` | `16px` | Tables/cards |
| `--ari-radius-control` | `10px` | Interactive controls |
| `--ari-shadow` | `0 2px 12px rgba(15,23,42,.035)` | Quiet elevation |
| `--ari-space` | `8px` | Spacing base |

These are documented design targets; the existing table CSS currently uses literal values. Migrate to tokens after compatibility QA.

## Table component v1
**Source code:** [editorial/blocks/ios-tables-style.html](../blocks/ios-tables-style.html)

- Rounded 16px outer frame, neutral hairline border, subtle shadow.
- Muted header background, readable compact type, generous cell spacing.
- Thin row separators; hover highlight on hover-capable devices.
- Horizontal touch scrolling for wide tables on phones; never shrink text to fit.
- Prefer semantic `<table>`, `<thead>`, `<th scope="col">`, `<tbody>`, with meaningful accessible headers.
- Preserve exact evidence language, qualifiers and source links inside cells.
- Dark-theme styling is experimental and must be checked against the actual WordPress theme; `prefers-color-scheme` alone does not reveal the site's theme state.
- **Interaction currently implemented:** hover + touch scrolling. Sorting, filtering, column pinning and expansion are *not* implemented; do not describe the current tables as sortable.
- **Scope warning:** v1 selectors target all tables inside `.entry-content` and `.wp-block-post-content`; for a site-wide rollout, replace with a dedicated component class and shared stylesheet.
- **Publishing status:** stored in GitHub; verify WordPress sanitization and front-end rendering before declaring deployed.

## Unified content cards
- Shared anatomy: optional eyebrow → title → concise description → structured metadata → plain-text destination link.
- Consistent border, radius, spacing and type hierarchy across Vendors and Projects.
- Metadata fields must remain semantically distinct: client, vendor, project family, workflow, aliases, geography, contract, compensation, platform and evidence.
- Responsive stacking on mobile; keyboard-visible focus for links.

## Page templates
- Project: overview, client/vendors, vacancy titles and aliases, markets/pay, workflow/platform, qualification, QA, vacancies, sources.
- Vendor: history, client/project relationship, recruitment, contracting, pay, quality, verified openings.
- Knowledge: question, verified findings, original evidence, interpretation, limitations, dated sources and cross-links.
- Jobs Matrix: filters and map complement (not replace) accessible data rows, status and source URLs.

## Media standards
- Prefer original readable screenshots with provenance, date, project and scope.
- Clearly label edited, redacted, reconstructed or illustrative visuals; never imply reconstructed UI is an untouched original.
- Provide meaningful alt text and captions; optimize for mobile and avoid unnecessary visual duplication.

## Responsive/accessibility QA
1. Check phone portrait and landscape, tablet and desktop.
2. Verify no clipped table text; touch scroll works and links are tappable.
3. Check keyboard navigation, focus visibility, color contrast and semantic table headers.
4. Confirm dark/light theme, WordPress block editor and front-end match.
5. Verify layout with long vendor names, citations and five-column comparisons.
6. Test after theme updates and before applying globally.

## Deployment workflow
- Source-controlled HTML/CSS and documentation live in this repository.
- Preview with `wordpress-editorial-sync.yml` using `dry_run=true`.
- Review generated preview and backup artifacts; only then publish with `dry_run=false`.
- Confirm the actual WordPress page content and front-end appearance; retain rollback.
- Never put WordPress credentials or application passwords into Git-tracked files.

## Changelog
- 1.0 — 2026-10-11: Consolidated design principles, tokens, table behavior, card/page patterns and QA checklist.
