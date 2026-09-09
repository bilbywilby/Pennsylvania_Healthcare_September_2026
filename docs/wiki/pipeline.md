# Pipeline Guide

The numbered Python scripts are the operational path. Run them from the
repository root or use the TUI's **Run audit pipeline** action.

| Stage | Purpose |
| --- | --- |
| `01_directories.py` | Create the expected directory skeleton and privacy rules. |
| `02_crosswalk.py` | Validate and write the Pennsylvania county crosswalk. |
| `03_validate_csvs.py` | Confirm required public data files exist. |
| `04_audit.py` | Validate carrier filing structure and rating areas. |
| `05_ingest_carrier_extensions.py` | Ingest and aggregate carrier extensions. |
| `06_provenance_gate.py` | Apply the final provenance gate. |

The pipeline stops on the first non-zero exit code. Generated files belong in
`data/public`; private material belongs in `data/private` and is ignored by
Git.