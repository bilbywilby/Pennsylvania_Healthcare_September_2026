# Pennsylvania Health Insurance Audit 2026 — Repository Architecture & Directory Blueprint

**Repository Name:** `pennsylvania-health-insurance-audit-2026`  
**License:** Creative Commons Attribution 4.0 International (CC BY 4.0) / MIT (Code)  
**Status:** Active Audit Compilation & Release Pipeline  

---

## 1. Directory Tree Overview

```authority
pennsylvania-health-insurance-audit-2026/
├── .github/                                # GitHub Actions & Issue/PR Templates
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug-report.yml                  # Template for data/documentation bug reports
│   │   ├── data-correction.yml             # Template for data updates or source corrections
│   │   ├── feature-request.yml             # Proposed new visualizations or policy briefs
│   │   └── question.yml                    # General public and researcher inquiries
│   ├── workflows/
│   │   ├── ci.yml                          # Continuous integration (data linting & tests)
│   │   ├── data-pipeline.yml               # Automated fetching & processing of Pennie datasets
│   │   ├── deploy-api.yml                  # Fast-API service container deployment
│   │   └── report-generation.yml           # PDF & artifact generation pipeline
│   └── PULL_REQUEST_TEMPLATE.md            # Standard guidelines for contributor PRs
│
├── analysis/                               # Core Analytical Documents & Gap Analyses
│   ├── consumer-info-gaps.md               # Detailed evaluation of 12 critical information gaps
│   ├── federal-state-comparison.md         # ACA §1312/§1332 state vs federal divergence analysis
│   ├── gap-analysis.md                     # Policy gap evaluation & remediation priorities
│   └── methodology.md                      # Data extraction, validation, & verification protocols
│
├── assets/                                 # Static Assets, Visualizations, and Raw Datasets
│   ├── data/                               # Standardized JSON/CSV datasets for application consumption
│   │   ├── congressional-district-map.json # Congressional district boundary & impact mapping
│   │   ├── county-termination-data.csv     # County disenrollment & premium surge figures
│   │   ├── demographic-breakdowns.json     # Age band and FPL income bracket terminations
│   │   ├── enrollment-timeline.json        # Monthly timeline (Peak 2025 -> July 2026)
│   │   ├── peer-states-comparison.json     # CO, WA, NM, CA state subsidy investment benchmark
│   │   ├── phan-survey-results.csv         # 424-respondent affordability survey raw data
│   │   └── premium-increase-data.json      # PID carrier rate change filings (2026 approved / 2027 proposed)
│   └── visualizations/                     # Interactive charts & rendered graphic assets
│       ├── static/                         # High-res exports (PNG/SVG) for media & publications
│       │   ├── county-map.svg              # Statewide disenrollment intensity map
│       │   ├── enrollment-decline-chart.png# Timeline graph (497K -> 431K)
│       │   └── infographic.png            # 3-step action summary infographic
│       └── vega-lite/                      # Vega-Lite chart specs (JSON format)
│           ├── 12-gaps-severity-matrix.json
│           ├── affordability-perception-collapse.json
│           ├── county-termination-rates.json
│           ├── enrollment-timeline.json
│           ├── pa-vs-national-premiums.json
│           └── peer-states-subsidy-investment.json
│
├── data/                                   # Data Warehouse (Raw Extraction & Processed Buffers)
│   ├── metadata.json                       # Source catalog (22 documents, timestamps, hashes)
│   ├── processed/                          # Intermediate transformed datasets
│   │   ├── congressional-district-impact.csv
│   │   ├── demographic-breakdowns.csv
│   │   └── peer-states-comparison.csv
│   └── raw/                                # Immutable raw source files
│       ├── carrier-rate-changes.csv
│       ├── county-termination-rates.csv
│       ├── enrollment-timeline.csv
│       └── phan-survey-results.csv
│
├── deliverables/                           # Target Publication Packages & Toolkits
│   ├── audit-report/                       # Full Audit Master Files
│   │   ├── executive-summary.md            # Briefing for executive & legislative leadership
│   │   ├── full-audit-report.md            # Comprehensive 80+ page master audit document
│   │   ├── gap-analysis.md                 # Standalone consumer info gap report
│   │   └── unified-appendix.md             # Consolidated 22-source verification compilation
│   ├── outreach-materials/                 # Consumer-Facing Assets
│   │   ├── consumer-white-paper.md         # Public explanation of subsidy cliff
│   │   ├── outreach-strategy.md            # $300K multi-channel outreach plan
│   │   └── timeline-deadlines.md           # Critical consumer dates (OE 2027, Auto-Renewal)
│   ├── policy-briefs/                      # Legislative & Regulatory Briefs
│   │   ├── compliance-checklist.md         # 14-item state remediation tracker
│   │   ├── district-impact-analysis.md     # PA Congressional Districts 1–17 breakdown
│   │   ├── fiscal-note.md                  # $50M state subsidy ROI analysis ($159M–$230M avoided care)
│   │   └── legislative-brief.md            # Testimony & legislative action summary
│   └── press-kit/                          # Media Resources
│       ├── faq.md                          # Press FAQ (10 core questions answered)
│       ├── media-kit.pdf                   # Complete media packet
│       ├── op-ed-draft.md                  # Editorial board submission draft
│       ├── press-release.md                # Immediate release press announcement
│       ├── quote-bank.md                   # Approved spokesperson & stakeholder quotes
│       └── social-media-pack/              # Multi-platform content
│           ├── facebook-post.md
│           ├── instagram-caption.txt
│           ├── linkedin-post.md
│           └── twitter-thread.txt
│
├── docs/                                   # Supplemental Documentation & Reference
│   ├── data-sources/                       # Documentation by Source Sector
│   │   ├── academic-institutions.md        # Muhlenberg College & Penn State PORH methodology
│   │   ├── advocacy-organizations.md       # PHAN, PACHC, Families USA source notes
│   │   ├── government-agencies.md          # PHIEA, PID, CMS, IRS reference links
│   │   ├── industry-aggregators.md         # ACA Signups & HealthInsurance.org validation
│   │   └── journalism.md                   # Philadelphia Inquirer & Republican Herald citations
│   ├── glossary/
│   │   └── index.md                        # Healthcare marketplace & regulatory terms glossary
│   └── methodology/
│       ├── data-collection.md              # Scrape & extraction protocol
│       ├── roi-calculation.md              # Mathematical derivation of $50M ROI (3:1 to 4.6:1)
│       └── verification-process.md         # Cross-reference & verification matrix
│
├── scripts/                                # Utility Scripts & Maintenance Executables
│   ├── fetch_pennie_data.py                # Automated Pennie API/web portal data scraper
│   ├── generate_charts.py                  # Generates Vega-Lite JSON and static PNG exports
│   ├── generate_pdf_report.py              # Compiles Markdown files into branded PDF deliverables
│   ├── validate_sources.py                 # Validates URL integrity and source SHA-256 hashes
│   └── validate_vega_lite.py               # Schema validator for chart specifications
│
├── src/                                    # Python / API Source Code
│   ├── api/                                # FastAPI Endpoints for Public Consumption
│   │   └── main.py                         # REST API serving audit metrics, timelines, & counties
│   ├── analysis/                           # Python Notebooks & Analytical Routines
│   │   ├── demographic_segmentation.ipynb  # Cohort attrition modeling
│   │   ├── enrollment_trend_analysis.ipynb # Attrition regression models
│   │   └── roi_calculator.py               # Dynamic ROI calculation module
│   └── utils/
│       ├── citation_generator.py           # APA/BibTeX automatic formatter
│       └── data_helpers.py                 # CSV/JSON transformation helpers
│
├── tests/                                  # Comprehensive Test Suite
│   ├── __init__.py
│   ├── test_api.py                         # FastAPI endpoint integration tests
│   ├── test_charts.py                      # Vega-Lite spec compliance tests
│   └── test_data_validation.py             # Data sanity & integrity tests
│
├── .dockerignore                           # Docker build exclusions
├── .gitignore                              # Git exclusion rules
├── CHANGELOG.md                            # Release history and audit revisions
├── CITATION.md                             # Citation formats (APA, BibTeX, Chicago, MLA)
├── CODE_OF_CONDUCT.md                      # Community interaction standards
├── config.yaml                             # Central configuration for paths & settings
├── CONTRIBUTING.md                         # Contributor guidelines and data standards
├── Dockerfile                              # Audit pipeline container setup
├── Dockerfile.api                          # API server container setup
├── docker-compose.yml                      # Multi-container service orchestrator
├── GOVERNANCE.md                           # Project governance and maintainer guidelines
├── LICENSE                                 # Creative Commons / MIT license documentation
├── README.md                               # Primary repository documentation
├── requirements.txt                        # Python dependencies
└── SECURITY.md                             # Security vulnerability disclosure guidelines
```

---

## 2. Comprehensive File Placeholders & Content Schemas

### 2.1 Configuration Files

#### `config.yaml`
```yaml
# Pennsylvania Health Insurance Audit 2026 - Master Config
project:
  name: "Pennsylvania Health Insurance Audit 2026"
  version: "1.0.0"
  audit_period: "January 2026 - August 2026"
  release_date: "2026-08-04"
  organization: "Pennsylvania Health Insurance Audit Team"

paths:
  raw_data: "data/raw"
  processed_data: "data/processed"
  assets_data: "assets/data"
  visualizations: "assets/visualizations"
  deliverables: "deliverables"
  output_reports: "output/reports"

audit_targets:
  investment_ask: 50000000 # $50 Million State Investment
  coverage_restoration_target: 44000 # Enrollees restored
  uncompensated_care_min: 159000000 # $159 Million min avoided
  uncompensated_care_max: 230000000 # $230 Million max avoided
  peak_enrollment_2025: 497000
  latest_enrollment_july_2026: 431270
  cumulative_terminations: 177000

api:
  host: "0.0.0.0"
  port: 8000
  cors_origins: ["*"]
```

---

### 2.2 GitHub Workflows & Templates

#### `.github/workflows/ci.yml`
```yaml
name: Continuous Integration & Data Validation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint Data and Validate Schemas
        run: |
          python -m unittest discover tests/

      - name: Validate Vega-Lite Specs
        run: |
          python scripts/validate_vega_lite.py
```

---

### 2.3 Key Dataset Schemas

#### `data/raw/enrollment-timeline.csv`
```csv
date,enrollment,cumulative_terminations,note
2021-01-01,333000,0,"EPTC enacted under ARPA; surge begins"
2025-01-01,497000,0,"Record high peak enrollment under EPTC"
2026-02-01,486000,85000,"OE 2026 closes; 85K terminated during OE window"
2026-03-24,471442,120000,"Post-OE attrition documented by PSU PORH"
2026-04-09,462000,130000,"Pennie Advisory Council deck statistics"
2026-05-01,452525,145000,"Post-OE attrition continues"
2026-06-01,443024,160000,"Pennie affordability portal update"
2026-07-01,431270,177000,"Latest verified audit enrollment figure"
```

#### `assets/data/demographic-breakdowns.json`
```json
{
  "metadata": {
    "source": "Pennie Advisory Council Meeting Deck (April 2026)",
    "data_cutoff": "2026-04-09",
    "total_sample_attrition": 130000
  },
  "age_brackets": [
    {
      "bracket": "26-34",
      "risk_level": "High",
      "trend": "Accelerating post-OE exits",
      "impact": "Young/healthy cohort exit driving risk pool deterioration"
    },
    {
      "bracket": "55-64",
      "risk_level": "Critical",
      "trend": "Highest absolute termination volume",
      "impact": "Pre-Medicare population hit by 3:1 age rating & subsidy cliff"
    }
  ],
  "income_brackets_fpl": [
    {
      "fpl_band": "150%-200%",
      "risk_level": "Critical",
      "rate": "Highest proportional disenrollment",
      "impact": "Working-poor gap; ineligible for Medicaid, unable to afford full premium"
    },
    {
      "fpl_band": ">400%",
      "risk_level": "High",
      "rate": "Complete loss of subsidy",
      "impact": "Subject to full unsubsidized premium spikes (up to 485%)"
    }
  ]
}
```

---

### 2.4 Visualization Specifications

#### `assets/visualizations/vega-lite/county-termination-rates.json`
```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": {
    "text": "Top 10 Pennsylvania Counties by Pennie Termination Rate",
    "subtitle": "Schuylkill leads at 24%; 15 of top 20 counties are census-designated rural"
  },
  "width": "container",
  "height": 300,
  "data": {
    "url": "../../data/county-termination-data.csv"
  },
  "mark": "bar",
  "encoding": {
    "x": {
      "field": "termination_pct",
      "type": "quantitative",
      "title": "Termination Rate (%)"
    },
    "y": {
      "field": "county",
      "type": "nominal",
      "sort": "-x",
      "title": "County"
    },
    "color": {
      "field": "census_designation",
      "type": "nominal",
      "scale": {
        "domain": ["Rural", "Urban"],
        "range": ["#d95f02", "#7570b3"]
      },
      "legend": {"title": "Designation"}
    },
    "tooltip": [
      {"field": "county", "type": "nominal", "title": "County"},
      {"field": "termination_pct", "type": "quantitative", "title": "Disenrollment Rate (%)"},
      {"field": "census_designation", "type": "nominal", "title": "Type"},
      {"field": "rating_area_notes", "type": "nominal", "title": "Marketplace Notes"}
    ]
  }
}
```

---

### 2.5 API Implementation

#### `src/api/main.py`
```python
"""
FastAPI Public Microservice for Pennsylvania Health Insurance Audit 2026 Data Access
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import pandas as pd
from pathlib import Path

app = FastAPI(
    title="PA Health Insurance Audit API",
    description="Programmatic access to 2026 Pennsylvania health insurance audit metrics, county disenrollments, and rate filings.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("./assets/data")

@app.get("/health")
def health_check():
    return {"status": "healthy", "audit_release": "2026-08-04"}

@app.get("/metrics/summary")
def get_summary_metrics():
    return {
        "peak_enrollment_2025": 497000,
        "latest_enrollment_july_2026": 431270,
        "total_coverage_lost": 177000,
        "avg_premium_increase_pa_pct": 102,
        "avg_premium_increase_national_pct": 58,
        "federal_subsidy_lost_annual": "$600M",
        "state_affordability_appropriation": "$0",
        "proposed_investment": "$50M",
        "projected_roi": "3:1 to 4.6:1"
    }

@app.get("/counties/top20")
def get_top_counties():
    try:
        df = pd.read_csv(DATA_DIR / "county-termination-data.csv")
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### 2.6 Deliverable Templates & Documentation

#### `deliverables/policy-briefs/fiscal-note.md`
```markdown
# Fiscal Note & Return on Investment Analysis
**Target Legislation:** Appropriation to the State Health Insurance Affordability Program  
**Requested Funding:** $50,000,000  
**Audit Period:** August 2026  

---

### Fiscal Impact Summary

| Metric | Figure | Notes / Source |
| :--- | :--- | :--- |
| **Proposed State Investment** | **$50,000,000** | ~8.3% of lost $600M federal subsidy |
| **Direct Enrollee Restoration** | **~44,000 residents** | Re-enrollment projected via price reduction |
| **Broad Premium Reduction** | **9% – 12%** | Benefiting 280,000+ continuing enrollees |
| **Avoided Uncompensated Care** | **$159M – $230M** | Cost-shift protection for PA hospitals |
| **Estimated Return on Investment** | **3.0:1 to 4.6:1** | Net savings per state dollar invested |

---

### Derivation & Formula

$$\text{ROI Ratio} = \frac{\text{Avoided Uncompensated Care Costs}}{\text{State Appropriation}}$$

$$\text{Minimum ROI} = \frac{\$159,000,000}{\$50,000,000} = 3.18 : 1$$

$$\text{Maximum ROI} = \frac{\$230,000,000}{\$50,000,000} = 4.60 : 1$$
```

---

## 3. Maintenance & Automated Data Flow

1. **Raw Ingestion (`/data/raw/`):** Scraped or manually parsed government filings, meeting decks, and news archives are preserved as raw CSVs and JSONs.
2. **Validation (`/scripts/validate_sources.py`):** Ensures source document hash checks match and URLs in the Unified Appendix remain accessible.
3. **Processing (`/data/processed/` & `/assets/data/`):** Cleans raw inputs and standardizes formats for charts, web apps, and API consumption.
4. **API & Static Rendering (`/src/api/` & `/scripts/generate_charts.py`):** Serves API endpoints and updates Vega-Lite specs alongside exported PNG/SVG static visual assets.
5. **PDF & Media Build (`/scripts/generate_pdf_report.py`):** Compiles markdown briefs into release-ready PDF media kits and legislative packets.