# Technical Root-Cause Analysis & Resolution Guide

## Problem Overview

The test suite exhibits split behavior during execution:
- **`tests/test_schema_reconciliation.py::TestFilingLoader::test_validated_filings_flow_through_exposure`**: **PASSED** (asserts `exposure[1]["weighted_rate_change"] == 17.50`).
- **`tests/test_synthetic_pa.py`**: **FAILED** (`TypeError: NoneType - float` and `KeyError: 'weighted_rate_change'`).

Because both tests logically invoke `schema_reconciliation`, this behavior confirms that `test_synthetic_pa.py` is loading a pre-fix or shadowed version of `schema_reconciliation.py` located elsewhere on disk or resolved through a different `sys.path` order.

---

## 1. Diagnostic Verification Checklist

Execute the following commands to confirm module paths and eliminate any stale bytecode or shadowing files.

### Step 1.1: Inspect Active Module File Paths via Pytest
Run a quick inline execution to inspect the exact resolved file path for `schema_reconciliation` in both test suites:

```bash
python3 -c "import sys; sys.path.insert(0, 'scripts'); import schema_reconciliation; print(schema_reconciliation.__file__)"
```

To see what `test_synthetic_pa.py` actually resolves at runtime, run:

```bash
python3 -m pytest tests/test_synthetic_pa.py --pdbcls=IPython.terminal.debugger:TerminalPdb -s -k "test_failing_name" --trace
```
*(Or insert `import schema_reconciliation as sr; print("LOADED FROM:", sr.__file__)` directly into `test_synthetic_pa.py`).*

### Step 1.2: Locate All Shadowing Duplicates
Search the workspace for all files matching `schema_reconciliation*.py`:

```bash
find . -type f -name "schema_reconciliation*.py" 2>/dev/null
```

### Step 1.3: Purge Stale Bytecode & Caches
Ensure compiled Python files (`.pyc`) or `__pycache__` directories do not point to stale file modified times (mtime):

```bash
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete
```

---

## 2. Immediate Targeted Fix

Align the import bootstrap at the top of `tests/test_synthetic_pa.py` to point explicitly to the canonical `scripts/` directory before importing any project modules.

```python
# Place at the very top of tests/test_synthetic_pa.py
import sys
from pathlib import Path

# Resolve absolute path to project root / scripts
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import pytest
import synthetic_pa as sp
import schema_reconciliation as sr
```

Then re-verify the single test suite:

```bash
python3 -m pytest tests/test_synthetic_pa.py -v
```

---

## 3. Long-Term Architectural Recommendation

Relying on manual `sys.path.insert(0, ...)` snippets inside individual test files can introduce fragile import orders across test files. To permanently prevent path drift across test runners, apply one of the following standard patterns:

### Option A: Centralized Root `conftest.py` (Recommended for Script Layouts)
Create a `conftest.py` file in the root `tests/` directory. Pytest executes `conftest.py` prior to running test files, guaranteeing uniform path resolution across all suites without repeating boilerplate.

```python
# tests/conftest.py
import sys
from pathlib import Path

# Automatically inject `scripts/` into sys.path for all pytest invocations
ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
```

### Option B: Editable Install (Recommended for Package Layouts)
If the project includes a `pyproject.toml` or `setup.py`, install the source package in editable mode within your virtual environment:

```bash
pip install -e .
```

This registers the project modules cleanly in the Python environment, rendering manual `sys.path` modifications unnecessary.