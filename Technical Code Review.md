# Architecture Validation & Code Review: `archive-by-keyword.sh`

## Executive Summary
The separation of execution logic (`archive-by-keyword.sh`) from domain definitions (`*.profile`) succeeds in making the archiving system completely domain-agnostic. Both edge-case bugs identified during testing—self-referential report matches and destination namespace collisions—have been cleanly resolved.

---

## Technical Audit of Fixes

### 1. In-Progress Report Contamination (Self-Match Fix)
* **Problem**: Scanning `$HOME_DIR` while appending output to `$REPORT` inside `$HOME_DIR` created a race condition where `grep` matched keywords present in the report header (such as `[duckbot]`).
* **Fix**: Moving report generation into `$ARCHIVE_DIR/reports/` relies on the pre-existing exclusion of `ARCHIVE` in both `DEFAULT_EXCLUDE_DIRS` (`--exclude-dir=ARCHIVE`) and `PRUNE_EXPR` (`-name ARCHIVE`).
* **Verification**: Because `grep` skips `ARCHIVE` at the directory tree level, the report file can never self-trigger Phase 2 content matches regardless of the profile's keyword pattern.

### 2. Path Mirroring & Collision Prevention
* **Problem**: Extracting `basename "$d"` or `basename "$f"` resulted in target collisions when two identically named folders or files existed in different source paths.
* **Fix**: Implementing the `relparent` helper with Bash parameter expansion:
  ```bash
  relparent() {
    local p; p="$(dirname "$1")"
    [[ "$p" == "." ]] && p=""
    echo "$p"
  }
  destdir="$ARCHIVE_DIR/dirs${parent:+/$parent}"
  ```
* **Verification**:
  * **Top-level directory** (`~/pa-audit-work`): `rel` = `pa-audit-work`, `parent` = `""`, `destdir` = `$ARCHIVE_DIR/dirs/`. Target path: `$ARCHIVE_DIR/dirs/pa-audit-work/`.
  * **Nested directory** (`~/projects/clientA/pa-audit-work`): `rel` = `projects/clientA/pa-audit-work`, `parent` = `projects/clientA`, `destdir` = `$ARCHIVE_DIR/dirs/projects/clientA`. Target path: `$ARCHIVE_DIR/dirs/projects/clientA/pa-audit-work/`.
  * Both structures coexist without overwriting or accidental nesting.

---

## Engine Robustness Highlights

1. **Process Isolation & Array Persistence**: `mapfile -t ... < <(...)` process substitution prevents subshell state loss, preserving array lengths for execution during the `--apply` phase.
2. **Defensive Parameter Checks**: `set -uo pipefail` combined with required parameter assertions (`: "${DOMAIN:?profile must set DOMAIN}"`) ensures early execution failure if a profile is malformed.
3. **Exclusion Parity**: `DEFAULT_EXCLUDE_DIRS` is consistently translated across `find` prune expressions (`PRUNE_EXPR` and `PRUNE_EXPR_GIT`) and `grep` flags (`GREP_EXCLUDES`).

---

## Domain Profile Template

For future profiles, create a file in `~/.archive-profiles/<domain>.profile` using the template below:

```bash
DOMAIN="your-domain-name"

# Regex for Phase 2 content search (grep -E)
KEYWORDS='keyword1|keyword2|phrase with spaces'

# Regex for Phase 1 directory name search (posix-extended iregex)
DIR_NAME_PATTERN='.*/(pattern1[^/]*|pattern2[^/]*)'

# Pattern for Phase 4 GitHub repository filtering (optional, defaults to DOMAIN)
GH_FILTER='keyword1|keyword2'

# Optional: Add domain-specific exclusions on top of DEFAULT_EXCLUDE_DIRS
# EXTRA_EXCLUDE_DIRS=(custom_build_dir temp_dumps)
```