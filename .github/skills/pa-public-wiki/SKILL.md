---
name: pa-public-wiki
description: Maintain a public-facing Pennsylvania health insurance 2026 wiki as a cited, patient-centered source of truth.
argument-hint: What Pennsylvania health insurance topic should the wiki research or update?
---

# Pennsylvania Public Wiki

Use this skill to turn repository evidence into plain-language, public-facing
wiki pages about Pennsylvania health insurance in 2026. The output must help a
resident understand what is known, what may change, and what practical next
step is available.

## Workflow

1. Identify the reader's question and the smallest relevant repository anchor:
   a source appendix, dataset, report, pipeline stage, or existing wiki page.
2. Separate plan year, market, and status. Always distinguish 2026 approved
   or observed information from 2027 proposed filings and future schedules.
3. Check primary sources first: Pennie, the Pennsylvania Insurance Department,
   CMS, Pennsylvania statutes, and the Office of Consumer Advocate. Use news
   sources as secondary context, never as the sole authority for a legal or
   enrollment claim.
4. Draft for a general reader. Define acronyms, explain why the information
   matters, and place the practical action near the relevant fact.
5. Label each material claim as verified, reported, modeled, proposed, or
   unresolved. Do not silently promote a modeled value to a fact.
6. Add a source link and a checked or publication date. For time-sensitive
   enrollment information, include an explicit instruction to confirm dates on
   Pennie's current site.
7. Link the page from `docs/wiki/index.md` and update the file-structure page
   when adding a new durable artifact.

## Decision Rules

- If sources disagree, preserve the disagreement and explain which source is
  primary; do not average or choose the more convenient number.
- If a claim cannot be checked from a primary source, put it in an open-
  questions section or omit it.
- Treat carrier-level rates as filing or market evidence, not as a personal
  quote. Never promise eligibility, savings, coverage, or an appeal outcome.
- Keep personal health information, household income, and identifiers out of
  examples and repository files.
- Advocacy guidance should point readers toward official assistance, records,
  deadlines, and appeal rights without presenting legal advice as a guarantee.

## Completion Checks

- The page has a clear audience, scope, plan year, and last-checked date.
- Facts, projections, requests, and recommendations are visibly distinct.
- Pennie and agency links are present for time-sensitive claims.
- The page links to the relevant data or provenance note in this repository.
- The TUI search and a focused syntax or documentation check pass.