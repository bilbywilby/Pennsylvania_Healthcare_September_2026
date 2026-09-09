---
name: pr-template-maintainer
description: Create or improve a GitHub pull request template that gives contributors a clear, repository-appropriate checklist and review context.
argument-hint: What repository workflow or review requirements should the pull request template capture?
---

# Pull Request Template Maintainer

Use this skill to create or revise `.github/pull_request_template.md` for this
repository. The template should make the purpose, scope, validation, provenance,
and reviewer follow-up of a change easy to understand without duplicating the
full implementation details.

## Workflow

1. Inspect the existing repository conventions, contribution documentation,
   CI configuration, and current pull request template before editing.
2. Preserve useful existing sections and repository-specific terminology.
3. Add only checklist items that contributors can reasonably verify. Keep
   security, privacy, data provenance, documentation, and testing requirements
   explicit when they apply to the repository.
4. Separate the change summary, validation evidence, risk or migration notes,
   and reviewer checklist so authors do not bury required information.
5. Use Markdown that renders correctly on GitHub. Keep prompts concise and
   remove sample prose that could be submitted accidentally.
6. If the repository handles healthcare, insurance, personal, or regulated
   data, require authors to state whether sensitive data is present and how
   provenance or sanitization was preserved.
7. Validate the final file as readable Markdown and confirm that it is located
   at `.github/pull_request_template.md`.

## Required Template Coverage

- Summary and motivation
- Scope or affected areas
- Tests, checks, or other validation performed
- Documentation or data/provenance impact
- Risk, compatibility, and follow-up notes
- A concise reviewer checklist

## Decision Rules

- Do not invent CI jobs, policies, labels, owners, or approval requirements.
- Do not require tests when the repository has no applicable test or validation
  mechanism; request an explanation instead.
- Do not expose credentials, personal health information, household information,
  or other sensitive values in examples.
- Keep the template generic enough for routine changes while preserving
  healthcare-audit traceability where relevant.
- Avoid checklists that merely restate GitHub's default pull request behavior.

## Completion Checks

- The template has a clear purpose and useful prompts for authors.
- Every required checkbox is actionable and repository-relevant.
- Validation and documentation expectations are visible.
- Sensitive-data and provenance considerations are addressed where applicable.
- Markdown structure is valid and the template does not contain placeholder
  text that could be mistaken for completed project policy.
