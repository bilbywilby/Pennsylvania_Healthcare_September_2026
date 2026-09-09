# Pennsylvania Health Audit Wiki

This is the public-facing index for Pennsylvania health insurance research in
2026. Start here to understand the evidence, find Pennie information, or take
a practical patient-advocacy next step. The wiki distinguishes verified,
reported, proposed, modeled, and unresolved material.

## Start Here

- [Pipeline guide](pipeline.md): what each numbered stage does and how to run it.
- [Data and provenance](data-and-provenance.md): the current source-of-truth boundaries.
- [Public source of truth](public-source-of-truth.md): scope, status labels, and maintenance promise.
- [Pennie in 2026](pennie-2026.md): enrollment context and consumer checklist.
- [Patient advocacy guide](patient-advocacy.md): notices, appeals, billing, and privacy.
- [File structure](file-structure.md): where code, data, generated files, and documentation belong.
- [Research notes](research-notes.md): short, reviewable notes that can grow into fuller pages.

## Contributing A Page

Keep pages focused on one workflow or question. Link primary sources, record
the date checked, and label unresolved claims clearly. The TUI can browse these
pages or search them from the terminal:

```text
python3 pa_audit_tui.py
python3 pa_audit_tui.py --search crosswalk
```