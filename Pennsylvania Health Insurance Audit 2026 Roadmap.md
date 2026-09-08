# Pennsylvania Health Insurance Audit Engine (2026)
## Strategic Product Roadmap, OPSEC Framework & Execution Plan

**Prepared for:** General Carter (OPSEC Lead) & Audit Engineering Team  
**Repository:** `pennsylvania-health-insurance-audit-2026`  
**Document Version:** 1.0.0  
**Effective Date:** September 2026  

---

## 1. Product Context & Strategic Alignment

| Strategic Dimension | Specification / Definition |
| :--- | :--- |
| **Product Stage** | **MVP Transition to Enterprise V1 Audit Engine.** Moving from an ad-hoc single-state prototype (PA Locality 24 / PA-East) to a standardized, multi-state regulatory audit engine capable of ingestion, PII/PHI scrubbing, and actuarial validation. |
| **Target User** | **Senior Regulatory Compliance Officer & Actuarial Auditor** (e.g., Pennsylvania Insurance Department / State Regulatory Enforcers). |
| **User Pain Point** | Disparate, unsanitized data formats (PDFs, unformatted markdown, raw CSV logs) containing rate hike requests ($50.1\text{M}$ blocked), GLP-1 utilization spikes, and Out-of-Network (OON) Fair Market Value (FMV) disputes. Manual verification takes weeks and risks accidental PII/PHI leaks to public git remotes. |
| **Primary Business Goal** | Build an air-gapped, automated pipeline that ingests rate filings, GLP-1 pharmacy metrics, and dispute dossiers, sanitizes them, and enforces 100% data provenance with zero privacy breaches. |
| **Key Performance Indicators (KPIs)** | 1. **Zero PII/PHI Leaks:** $0$ raw SSNs, NPIs, or Member IDs pushed to remote repos.<br>2. **Audit Latency:** Reduce audit report generation from 14 days to $<4$ hours.<br>3. **Git Lineage:** $100\%$ preservation of file history using `git mv` and structured commits.<br>4. **Actuarial Accuracy:** $100\%$ validation against `validation_log.csv` benchmarks. |
| **Tech Stack & Constraints** | **Stack:** Python 3.11+, Bash CLI, Git/GitHub Actions, `w3m` / terminal inspection tools.<br>**Constraints:** Strict HIPAA/HITECH compliance, local air-gapped Enclave compatibility, strict execution speed for pre-commit hooks ($<2\text{s}$). |

---

## 2. OPSEC & Data Integrity Architecture

### 2.1 Git History Preservation Protocol
Standard shell commands like `mv` sever file tracking history in Git. To maintain chain-of-custody and blame logs for audit evidence:

1. **Structured Migration:** All moves **must** utilize `git mv` to preserve commit lineage across directory restructuring.
2. **Directory Isolation:** Target directory `target_subfolder/` must be categorized into logical domains:
   * `./target_subfolder/reports/` (PDF / DOCX)
   * `./target_subfolder/dossiers/` (Markdown / Forensic logs)
   * `./target_subfolder/datasets/` (CSV filings & utilization)

```bash
#!/usr/bin/env bash
# git_preserve_move.sh - OPSEC compliant git file migration

TARGET="target_subfolder"
mkdir -p "$TARGET/reports" "$TARGET/dossiers" "$TARGET/datasets"

# Migrate datasets with git history intact
git mv rate_filings_by_carrier.csv "$TARGET/datasets/" 2>/dev/null || true
git mv enrollment_by_month.csv "$TARGET/datasets/" 2>/dev/null || true
git mv glp1_spend_breakdown.csv "$TARGET/datasets/" 2>/dev/null || true
git mv validation_log.csv "$TARGET/datasets/" 2>/dev/null || true

# Migrate reports & dossiers
git mv PA_Health_Insurance_Report_April2026.pdf "$TARGET/reports/" 2>/dev/null || true
git mv PA_Health_Insurance_Market_March2026_FINAL.docx "$TARGET/reports/" 2>/dev/null || true
```

### 2.2 Advanced PII/PHI & HIPAA Scanning Pipeline
Expanding Carter's atomic PII scanner into a full local pre-commit hook (`.git/hooks/pre-commit`) covering SSNs, Emails, National Provider Identifiers (NPI), and Health Insurance Claim Numbers (HICN/Member IDs).

```python
#!/usr/bin/env python3
"""
pii_phi_scanner.py - Pre-Commit Security Engine
Scans repository text files for potential PII/PHI before git commit staging.
"""
import sys
import os
import re

PATTERNS = {
    "SSN": r'\b(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b',
    "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "NPI (Provider ID)": r'\b[1-2]\d{9}\b',
    "MEMBER_ID": r'\b[A-Z]{3}\d{8,11}\b',
    "FEIN (Tax ID)": r'\b\d{2}-\d{7}\b'
}

EXCLUDED_DIRS = {".git", ".opsec_logs", "node_modules", "__pycache__"}
ALLOWED_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".yaml", ".yml", ".py", ".sh"}

def scan_repository():
    violations = 0
    print("[*] Launching OPSEC PII/PHI Scan...")
    
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            for label, pattern in PATTERNS.items():
                                matches = re.findall(pattern, line)
                                if matches:
                                    print(f"[!] ALERT [{label}] in {path}:{line_num} -> Match: {matches[0][:4]}***")
                                    violations += 1
                except Exception as e:
                    print(f"[x] Error reading {path}: {e}")

    if violations > 0:
        print(f"\n[CRITICAL] OPSEC Scan failed with {violations} violation(s). Commit aborted.")
        sys.exit(1)
    else:
        print("[+] OPSEC Scan Passed: Zero PII/PHI detected.")
        sys.exit(0)

if __name__ == "__main__":
    scan_repository()
```

---

## 3. Product Roadmap (Phases 1–4)

```
[Phase 1: Foundation & OPSEC] ──► [Phase 2: Data Standardization] ──► [Phase 3: Actuarial Engine] ──► [Phase 4: Multi-State Scale]
   (Weeks 1-2)                        (Weeks 3-4)                           (Weeks 5-6)                     (Weeks 7-8)
```

### Phase 1: Repo Consolidation & Hardening (Weeks 1–2)
* **Objective:** Establish clean directory layout, zero PII leaks, and git history continuity.
* **Deliverables:**
  * Automated `git mv` migration script.
  * Local `.git/hooks/pre-commit` PII/PHI scanner.
  * Environment variable management (`.env.example`) and strict `.gitignore`.

### Phase 2: Data Standardization & Provenance (Weeks 3–4)
* **Objective:** Parse heterogeneous audit inputs (PDF, CSV, MD) into unified JSON schema.
* **Deliverables:**
  * Pydantic schemas for `RateFiling`, `GLP1Utilization`, and `OONDispute`.
  * Automated correlation check against `validation_log.csv`.
  * Markdown-to-PDF compiler for official state regulatory filings.

### Phase 3: Actuarial Audit Engine & IDR Calculator (Weeks 5–6)
* **Objective:** Automate rate increase threshold checks and OON dispute Fair Market Value (FMV) benchmarks.
* **Deliverables:**
  * Rate-hike trigger module flagging requested changes exceeding $+10\%$ baseline.
  * IDR multiplier calculator ($1.15\times$ to $2.50\times$ Medicare) for CPT codes `99214`, `72148`, `45378`.
  * Compliance check for 28 Pa. Code § 9.725 hold-harmless provisions.

### Phase 4: Multi-State Scaling & Reporting Enclave (Weeks 7–8)
* **Objective:** Extend core audit rules beyond PA Locality 24 to full multi-state compliance.
* **Deliverables:**
  * Multi-state config loader (PA, NJ, NY, MD).
  * Air-gapped CLI dashboard (`w3m` / `rich` interface) for rapid auditor review.
  * Automated executive report generator outputting audit-ready PDFs.

---

## 4. Prioritized User Stories

### User Story 101: Pre-Push PII Prevention (OPSEC)
* **As a** Compliance Auditor  
* **I want to** automatically scan all text files and datasets before committing  
* **So that** no member SSNs, NPI numbers, or private emails are published to external remotes.
* **Acceptance Criteria:**
  1. `pii_phi_scanner.py` runs automatically via pre-commit hook in $<2\text{s}$.
  2. Blocks commit execution and logs alert file location if matches are detected.
  3. Ignores false positives within binary files or `.git` internals.

### User Story 102: Git-Preserving Directory Cleanout
* **As a** Lead Repository Maintainer  
* **I want to** move PA health insurance files into structured target subfolders using `git mv`  
* **So that** file revision history, author blame logs, and audit trails remain 100% intact.
* **Acceptance Criteria:**
  1. No file loss during transfer.
  2. Running `git log --follow <new_path>` retains pre-migration commit history.
  3. Separate subdirectories created for `/reports`, `/datasets`, and `/dossiers`.

### User Story 103: Actuarial Rate & GLP-1 Variance Flagging
* **As an** Actuarial Risk Specialist  
* **I want to** cross-analyze `rate_filings_by_carrier.csv` against `glp1_spend_breakdown.csv`  
* **So that** I can flag carriers attributing unreasonable rate hikes ($>15\%$) to GLP-1 weight-loss drugs following Medicaid policy changes.
* **Acceptance Criteria:**
  1. Script calculates net percentage contribution of pharmacy spend to overall rate hikes.
  2. Highlights carriers exceeding average individual market benchmark ($21.5\%$).
  3. Outputs clean validation summary matching `validation_log.csv`.

---

## 5. Metrics & Compliance Matrix

```markdown
  +-----------------------------------------------------------------------------------+
  |                              AUDIT ENGINE VERIFICATION                            |
  +-----------------------------------------------------------------------------------+
  | Metric                       | Baseline (Manual) | Target (Phase 3) | Status     |
  +------------------------------+-------------------+------------------+------------+
  | PII / PHI Leak Frequency     | High Risk         | 0 Incidents      | ENFORCED   |
  | File Organization Latency    | 45 mins           | < 5 seconds      | AUTOMATED  |
  | IDR FMV Calculation Time     | 30 mins / case    | < 1 sec / case   | AUTOMATED  |
  | Audit Report Generation      | 14 Days           | < 4 Hours        | PLANNED    |
  | Data Provenance Coverage     | 65%               | 100% Tracked     | IN-PROGRESS|
  +-----------------------------------------------------------------------------------+
```

### Immediate Next Steps for General Carter:
1. Initialize `.git/hooks/pre-commit` using the `pii_phi_scanner.py` script above.
2. Execute the `git_preserve_move.sh` script to re-organize files without losing git blame history.
3. Commit directory structure update with message: `refactor(opsec): consolidate PA audit files with git history preservation`.