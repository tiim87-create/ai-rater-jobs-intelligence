# AI Rater Insider — Knowledge Architecture v1.0

Status: editorial working standard · 2026-10-12

## Purpose
Make the website a connected, evidence-based industry knowledge system rather than a collection of unrelated posts. WordPress remains the publication layer; GitHub holds structured data, schemas and editorial governance. Do not confuse observations with confirmed vendor policy.

## Canonical entity types
| Entity | Canonical ID example | Required fields |
|---|---|---|
| Client | client:google | name, evidence, relationships |
| Vendor | vendor:telus-digital | legal/brand names, regions, projects, official source |
| Project | project:google-general-rating | client, known vendors, workflow, platform, confidence |
| Vacancy | vacancy:telus:129038 | vendor, exact public title, reference ID, URL, observed date, geography, status |
| Market | market:us-en | country, language, eligibility caveats |
| Workflow | workflow:needs-met | tasks, qualification, platform, project links |
| Control | control:identity-verification | stage, vendor, applicability, evidence |
| Evidence | evidence:YYYY-NNN | source, date, claim, access level, confidence |
| Research article | article:slug | topic, primary entities, evidence links, last review |

Never use job title as project identity: public titles change and can map to different project families. Keep observed titles and historical aliases, each dated and sourced. Never silently convert unknown geography to a country; distinguish Global from unmapped.

## Relationships
Client → commissions → Project; Vendor → recruits-for → Project; Project → uses → Workflow; Vacancy → recruits-for → Project (confidence required); Vacancy → offered-in → Market; Vendor/Project → uses → Control (evidence required); Evidence → supports/disputes → Claim; Article → explains → Entities.

## Editorial placement
- Vendor page: corporate background, hiring, compensation, policies, verified controls.
- Project page: workflow, platform, qualification, client-vendor mapping, title aliases.
- Jobs Matrix: individual official postings, markets, current/historical status.
- Industry research: cross-vendor mechanisms, pay trends, account integrity, audits, replacement cycles.
- Case study: dated primary evidence, scope, limitations, interpretation; link to broader research.
- Quality/performance suspensions belong under quality monitoring unless evidence directly ties them to fraud or identity checks.

## Evidence standard
Levels: A = primary official documentation; B = dated direct records or first-hand material (redacted); C = independent corroboration; D = community/self-report; E = analytical inference. Each claim has source URL or private evidence pointer, date, applicability (vendor, market, worker type, period), and status (confirmed / reported / inferred / unresolved). A signed authorization is not proof every permitted check occurred. US employee I-9 is not automatically applicable to freelancers. Public silence is not proof of absence. Never publish personal data or secret detection thresholds.

## Review cadence
Vacancies: automated daily or weekly, record last_checked and changes. Vendor policies and rates: monthly or upon material update. Evergreen industry research: quarterly. Historical claims: revisit only when evidence changes. Broken-link and cross-reference audits: weekly.

## First implementation backlog
1. Inventory published WordPress pages with canonical article IDs, primary entity and evidence links.
2. Build controlled vocabulary for clients, vendors, projects, workflows, markets and job-title aliases.
3. Add evidence register with source date, confidence, applicability and privacy status.
4. Map each project to its vendor/client and known historical vacancy titles; preserve uncertainty.
5. Generate cross-link recommendations from the entity graph, then review editorially.
6. Validate Jobs Matrix geography, especially Global vs unmapped, without manual per-vacancy patching.
7. Add automated stale-content and broken-link reporting.

## Publishing rules
No automated publication of inferred mappings. Changes to live articles require review and preservation of Gutenberg blocks, figures, links, attribution, and neutral card design per CARD_DESIGN_STANDARD.md. This document is the architecture specification, not a claim that all underlying databases already exist.
