# Real-Data Arrival Checklist: PID Covered-Lives Extract

This checklist defines the operational verification, execution, and rollback procedure required when the external Pennsylvania Insurance Department (PID) extract drops into `data/carrier-rate-changes.csv`.

---

## 1. Pre-Ingestion Schema Validation
Before running the pipeline orchestrator, verify the raw extract against the locked contract in `HANDOVER.json`.

* [ ] **Drop Location Verification:** Confirm file exists at `data/carrier-rate-changes.csv`.
* [ ] **Header Inspection:** Ensure headers contain required columns:
  * Required: `carrier` (or legacy `carrier_name`), `rate_change` (or legacy `approved_rate_change`), `rating_area`.
  * Optional: `covered_lives`, `serff_id`, `verified`.
* [ ] **Encoding & Newlines:** Verify file is valid UTF-8 without trailing null bytes or unescaped quote characters.
* [ ] **Numeric Value Range:** Confirm `rate_change` entries are expressed in percentage points (e.g., `10.0` for 10%, not `0.10`).

---

## 2. Ingestion & Pipeline Execution

* [ ] **Execute Pipeline:** Run the master orchestrator script:
  ```bash
  bash bootstrap/00_run_all.sh
  ```
* [ ] **Log Inspection (`step_05` Ingestion):**
  * Check for column alias normalization logs (`carrier_name -> carrier`, `approved_rate_change -> rate_change`).
  * Ensure no `FilingValidationError` is raised due to duplicate `(carrier, serff_id)` collisions or malformed numerics.
* [ ] **Log Inspection (`step_06` Exposure Output):**
  * Confirm log output reads: **`basis: covered_lives`**.
  * Verify watermarking: `verified` key is correctly propagated (`True` if all contributing filings are verified, `False` if any are unverified).

---

## 3. Acceptance Criteria

| Check Item | Target State | Pass / Fail |
| :--- | :--- | :--- |
| **Exposure Basis** | Step 06 log explicitly reports `basis: covered_lives` | [ ] |
| **Weighted Rate Change** | Non-null, positive float for all populated rating areas | [ ] |
| **Unweighted Fallback** | Logged ONLY if `covered_lives` is entirely absent across all rows | [ ] |
| **Audit Verification** | Downstream `04_audit` consumer ingests exposure payload without schema errors | [ ] |

---

## 4. Rollback & Emergency Fallback Procedures

In the event of an unhandled extract schema anomaly or pipeline failure:

1. **Schema Mismatch / Malformed Extract:**
   * If `FilingValidationError` is raised on unknown headers, confirm if new column aliases need to be added to `COLUMN_ALIASES` in `scripts/filing_loader.py`.
   * Do **not** modify column names manually in `data/carrier-rate-changes.csv` without logging an emergency patch in git.

2. **Reversion to Previous Baseline:**
   * If the drop corrupts county exposure calculations downstream, clear staging artifacts and restore the last known good data drop:
     ```bash
     git checkout HEAD -- data/
     python3 -m pytest tests/ -q
     ```

3. **Fallback Logging Audit:**
   * If logs report `basis: unweighted_fallback`, verify whether the extract was missing the `covered_lives` column entirely or contained non-numeric/null values across all rows.