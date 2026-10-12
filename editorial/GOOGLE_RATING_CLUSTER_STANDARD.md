# Google Rating Project Cluster — Reference Architecture

Status: audit and editorial specification, 2026-10-12. No live WordPress pages changed.

## Canonical hierarchy
- **Parent:** Google Search Quality Rating Project (WordPress page 10): Google/client-vendor-platform model, historical evolution, overall workforce, general vs specialized groups, common quality framework. Avoid reproducing detailed task guides.
- **Child:** General Rater Pool (page 11): Needs Met, Page Quality, Side-by-Side, task UI, qualification, AET, NTA, quality feedback.
- **Child:** AI Helpfulness Response Evaluation (page 12): prompt, individual response rating, response-vs-response comparison, problem flags, explanation, evaluation UI, quality.
- **Child:** Factuality & Research (page 13): claim extraction, research/evidence verification, sourcing, sentence-level assessments, evaluation UI, quality.

## Mandatory template for child pages
1. Project snapshot: client, known vendors, workflow, platform, geography, contract, pay and exact title aliases; mark unknowns.
2. Scope and differentiation: what it evaluates, and what it does NOT evaluate.
3. Qualification/onboarding: documented vs historical; vendor-specific routes.
4. Task interface: annotated, appropriately sourced real task or illustrative mockup clearly labeled.
5. Rating workflow: stepwise evaluation with examples.
6. Production conditions: AET, NTA, allocation; distinguish observations from universal policy.
7. Quality controls: feedback, calibration, audits; link to dedicated quality article.
8. Evidence and limitations: primary sources, dated experience, inference.
9. Related projects, canonical cross-links and vacancy mapping.

## Audit findings from WordPress content
- Parent page 10: ~60k characters, 3 images, only 4 hyperlinks in current raw HTML; includes extensive quality discussion and general-pool detail that should be summarized and linked to specialist pages.
- General Pool page 11: ~37k characters, 4 images, 21 hyperlinks; strongest structured template (numbered sections) and potential model for the other children.
- Factuality page 13: ~17k characters, 3 images, 11 hyperlinks; requires parity of project snapshot, workflow examples and evidence section.
- Helpfulness page 12: ~23k characters, 2 images, 11 hyperlinks; requires parity of project snapshot, qualification and evidence section.
- All four have headings on workflows, AET/quality and adjacent project comparisons; consolidate shared concepts in the parent or dedicated thematic pages, with short contextual references in each child.

## Next editorial actions
1. Build a heading-level content ownership matrix: each topic has one canonical page, with links elsewhere.
2. Verify every existing task image renders, is relevant and has accurate captions; no generic replacement images.
3. Normalize project snapshot fields and terminology; exact historical vacancy titles must have dated evidence.
4. Add reciprocal navigation: parent → each child, child → parent, Helpfulness ↔ Factuality, General Pool → specialized groups.
5. Strengthen source attribution and update dates; label first-hand and inferred claims.
6. Test Gutenberg rendering, mobile layouts, anchor links, and cross-links before publishing edits.

## Acceptance criteria
- Every page has a unique editorial purpose.
- All claims about project exclusivity, job aliases, rates and vendor policies have evidence or uncertainty labels.
- All real-task visuals load and captions accurately describe them.
- Project metadata uses the same card design as Vendors and Projects.
- Shared topics are linked rather than duplicated.
- WordPress content is backed up and verified after each change.
