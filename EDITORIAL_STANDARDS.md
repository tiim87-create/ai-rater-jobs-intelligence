# AI Rater Insider — Editorial & Design Standards

**Version:** 1.3  
**Adopted:** 2026-10-11  
**Scope:** AI Rater Insider (airaterinsider.com), WordPress editorial content, project directories, and Jobs Intelligence.

## 1. Editorial mission
Every substantive article must offer readers **information that is difficult to find elsewhere**: original reporting, historical context, primary documents, first-hand experience, interface examples, meaningful synthesis, or verifiable analysis. Avoid generic SEO filler and repetitive introductory prose.

## 2. Evidence and accuracy
- Prioritize official vendor/client documentation, job listings, company disclosures, original guidelines, and dated primary sources.
- Distinguish explicitly between **publicly verified facts**, **first-hand/project intelligence**, **inference or interpretation**, and **unresolved questions**.
- Cite sources close to material claims; preserve dates, geographic scope, historical context and changes over time.
- Do not invent rates, job availability, project-client relationships, internal procedures, screenshots, statistics or source links.
- Historical and current facts must be labeled accordingly; revisit fast-changing hiring and compensation claims.
- Avoid overstating what is knowable about private client systems, behavioral monitoring or task allocation.

## 3. Editorial voice
- Publish in clear, professional, natural English with a human editorial voice.
- Be precise, evidence-led and readable; avoid generic AI marketing phrases, inflated claims and excessive repetition.
- Use original observations responsibly and mark them as first-hand rather than official vendor policy.
- Separate explanation from practical advice and opinion.

### Narrative journalism standard (all editorial content)
- Write for a curious reader or working rater, not an academic committee. Use investigative technology journalism informed by first-hand industry experience.
- Open with a concrete scene, surprising documented detail, or compelling reader question; deliver the key insight early.
- Use short, varied paragraphs, conversational transitions and plain English. Explain necessary technical terms on first use.
- Let the story progress from a human situation to how a system works, evidence, implications and what remains unknown.
- Integrate original screenshots, cases and historical anecdotes where they advance the narrative. Never invent scenes, dialogue or vendor-specific controls.
- Prefer natural headings that promise an answer, not a rigid numbered report or repeated 'Layer' labels.
- Avoid repeated blockquotes, repetitive caveats, corporate jargon, generic AI phrasing and abstract terms such as 'provenance' without a concrete explanation.
- Keep evidence discipline: place compact source notes close to claims, distinguish firsthand reports and hypotheses, and maintain a concise evidence/limitations section.
- Tables support the narrative; they do not replace it. Preserve SEO structure and scannability without turning the article into a listicle.
- Editing target: engaging and accessible to non-experts while preserving specialist insight and nuance.

### Site-wide application by content type
- **Knowledge / research:** story-driven investigative reporting with human examples, primary evidence and accessible explanations.
- **Vendors:** tell the company's role and evolution through concrete industry consequences, not corporate-profile boilerplate.
- **Projects:** open with what a contributor actually does, then explain workflow, qualification, platforms and verified employment details.
- **Jobs Matrix / vacancy intelligence:** keep structured data concise and exact; apply the voice to introductions, descriptions and explanatory notes, never at the expense of data precision.
- **Guides / onboarding:** clear, friendly, actionable explanations without promotional promises or speculative shortcuts.
- **About / landing pages:** concise, distinctive, confident human voice; avoid generic marketing copy.
- **UI labels, tables and technical references:** prioritize clarity and scannability; narrative style is not a reason to make interfaces wordy.
- Apply to existing pages during editorial revision; do not overwrite all published pages blindly. Preserve unique sources, established URLs, visuals and citations, and review changes before broad rollout.

## 4. Site architecture
- **Projects:** specific project families, workflows, task interfaces, qualification, platforms, project-to-job mappings.
- **Vendors:** companies, historical identity, business model, recruitment, contract and payment practices.
- **Knowledge:** cross-industry history, economics, employment, quality and anti-fraud, workforce operations.
- **Research:** methodology, evidence tracking, research queue and datasets, nested conceptually under Knowledge.
- **Jobs Matrix:** current and historical vacancies, official links, location, status and mapping evidence.
- Keep project pages distinct from qualification-lab training pages. Avoid competing or duplicate landing pages.

## 5. Terminology and taxonomy
- Do not conflate **client**, **vendor**, **platform**, **project**, **project family**, **pool**, **workflow**, **task**, **job posting**, or **job title**.
- Record current and historical vacancy titles as aliases with source, vendor, country and validity where known.
- Example first-hand mapping: TELUS **Content Reviewer** relates to Google Search rating; TELUS **Content Evaluator** relates to YouTube / Internet Safety. Treat mappings as project intelligence unless independently corroborated by official public listings.
- Project-to-vacancy relationships need explicit confidence and supporting evidence.

## 6. Standard page structure
For deep project pages, use as applicable: Project Overview; Client & Vendors; Job Titles & Historical Aliases; Geography & Compensation; Platform & Task Types; Qualification & Onboarding; Quality Control; Current Openings; Original Materials & Further Research.
For Knowledge articles: reader question and key finding; verified background; original evidence and analysis; practical implications; limitations; dated sources; relevant next reading.
Do not force sections with no useful evidence; placeholders are for drafts, not published articles.

## 7. Visual design system
- Minimal, high-tech, Apple-like aesthetic with consistent hierarchy, whitespace and restraint.
- Use a consistent introductory eyebrow, page title, summary, optional jump navigation and unified article/card layout.
- Cards: consistent padding, border, radius, metadata label, title and clear text link; no unrelated styles across Projects, Vendors and Knowledge.
- Prefer theme tokens and registered Gutenberg blocks; ensure mobile responsiveness and editable WordPress content.
- Screenshots and task illustrations must be accurate, correctly ordered, legible and labeled by provenance. Do not substitute invented UI for original interfaces.

The implementation reference for reusable design components, tokens, table styling and QA is [editorial/design/DESIGN_SYSTEM.md](editorial/design/DESIGN_SYSTEM.md). Store source code in GitHub and verify front-end behavior before applying changes site-wide.

## 8. Jobs Intelligence standards
- Prefer automated ingestion of official TELUS Digital, WeloData/WeloGlobal and RWS postings; avoid manual fixes as the primary solution.
- Preserve job ID, title, official URL, vendor, geography, language, status, timestamps, evidence and mapping confidence.
- Explicit **Global** must remain Global, not Unmapped. Use Unmapped only when geography cannot be reliably resolved.
- Geocode geographic locations where source evidence supports them; do not invent coordinates, countries, client assignments or compensation.
- Distinguish discovered/checked/changed/removed records and current versus historical postings.
- Changes to data processing should be tested against representative records from all vendors.

## 9. SEO and internal linking
- Maintain descriptive headings, useful metadata, canonical topic ownership and contextually relevant internal links.
- Avoid duplicate articles and overlapping hubs. Prefer updating established URLs over creating competing pages.
- Before changing slugs, prepare redirects and review internal links.
- Link related economics, employment, vendor integrity, project history and job-intelligence articles where the transition helps the reader.

## 10. Publishing and review workflow
1. Inventory the existing page and related material before rewriting.
2. Verify sources and identify unsupported or stale claims.
3. Preserve unique first-hand evidence and existing useful links.
4. Edit for accuracy, clarity, structure, taxonomy and design consistency.
5. Check mobile layout, WordPress block validity, visuals, SEO and links.
6. Publish only when content is sufficiently complete and reviewed; otherwise use drafts.
7. Record significant editorial changes and open research questions.

## 11. Governance
This document is the project's **working editorial standard**, not a claim that every legacy page already complies. Proposed deviations should be discussed and recorded by Git commit. Revise the version and change history when standards materially change.

### Change history
- **1.3 — 2026-10-11:** Extended the narrative journalism voice site-wide, adapted to content type, with staged editorial rollout.
- **1.2 — 2026-10-11:** Adopted investigative, human-centered narrative journalism as the default voice for Knowledge features.
- **1.0 — 2026-10-11:** Consolidated agreed editorial principles, site architecture, taxonomy, design, SEO, evidence and Jobs Intelligence rules.
- **1.1 — 2026-10-11:** Linked the version-controlled design system and reusable UI source code as the implementation reference.
