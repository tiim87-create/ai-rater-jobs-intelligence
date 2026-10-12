# AI Rater Insider — Card Design Standard

Status: Approved baseline — 2026-10-12
Scope: WordPress.com pages in Vendors, Projects, Knowledge Base, Industry, and article diagrams. This standard prevents page-specific card variants. Validate against the site's existing Vendors/Projects components before modifying those components.

## Single reusable visual language
- Minimal, editorial, Apple-inspired aesthetic; white or neutral surfaces, subtle #E2E8F0 border, restrained #2563EB accent, dark #0F172A heading, muted #64748B supporting text.
- Cards are informational surfaces, **not colorful status badges**. Avoid different colored top borders per card, arbitrary gradients, saturated fills, and heavy shadows.
- Consistent spacing: 20–24px internal padding, 12–16px between cards, border radius 12px. Use the same typography hierarchy across all page families; compact eyebrow, clear heading, concise explanatory text.
- Grid responsive: 3 columns only when cards fit comfortably, otherwise 2 or 1; mobile stacks vertically. Equal card padding and aligned headings. Never force a five-card horizontal strip on narrow screens.
- Content anatomy: optional eyebrow/number → short title → one- or two-sentence description → optional grounded metadata/link. Do not invent ratings, figures or states.
- Cards for Vendors, Projects, and conceptual article frameworks must share tokens, but retain appropriate semantic fields. A conceptual framework is not a vendor listing.

## Implementation requirements
1. Prefer reusing existing WordPress block patterns/classes for cards from the approved Vendors and Projects pages. Do not introduce standalone inline styles if a shared component exists.
2. For article-only HTML fallback, use: border 1px solid #E2E8F0, radius 12px, padding 24px, white background, heading #0F172A, description #64748B, accent #2563EB **only for eyebrow/number/link**. No colored top border.
3. Responsive layout should use a wrapping grid with a sensible min-width (~220px); five cards display as 3+2 or 2+2+1 depending on width, not as five narrow columns.
4. Distinguish verified facts, first-hand evidence, and hypotheses in adjacent captions; do not decorate uncertain claims as verified statuses.
5. Use valid serialized Gutenberg markup; inspect editor for invalid blocks and verify the saved page after every change.
6. Avoid duplicates: one summary/Key findings section, one instance of each card component, and consistent cross-links.
7. Before release, visually compare against Vendors and Projects on desktop and mobile, verify all links and the editor, and preserve existing editorial content.

## Five-layer article example
Cards: 01 Technical Screening; 02 Behavioral Screening; 03 Identity Verification; 04 Background Checks; 05 Continuous Account Integrity Monitoring. All five use the **same** neutral card component; numbers are small blue eyebrows, not colored status bars. These are overlapping analytical categories, not a universal chronological sequence.

## Editorial alignment
Follow [Editorial Attribution Standard](EDITORIAL_ATTRIBUTION_STANDARD.md) for evidence labeling and confidentiality.
