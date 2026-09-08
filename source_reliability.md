# Source Reliability Appendix & Fabrication Exclusions

## 1. Excluded Documents & Fact-Checking Audit

During the initial ingestion phase, an unverified analysis titled *"Cross-Sectional Metadata Analysis of Pennsylvania Health Insurance Audit Protocols and Market Structures for September 2026"* was subjected to rigorous statutory and factual verification. The document was **strictly excluded** from this repository due to critical hallucinations, non-existent statutory citations, and scrambled geographical mappings.

### Summary of Exclusions and Errors

| Flagged Citation / Claim | Initial Status | Verification Finding & Primary Source Evidence | Action Taken |
| :--- | :--- | :--- | :--- |
| **Rating Area Scrambling** | Scrambled Mapping | The excluded document inverted Rating Areas 1 and 8 and misattributed counties across Areas 3, 4, 5, 6, and 9. Official CMS crosswalk files confirm Area 4 is Pittsburgh Metro, Area 5 is Central/Laurel Highlands, Area 6 is Central/Lehigh Valley, and Area 9 is the Capital Region (Centers for Medicare & Medicaid Services, 2024). | **Corrected:** Repository adopted the official live CMS 2026 geographic crosswalk files, verified county-by-county against all 67 PA counties with no duplicates or omissions. |
| **Senate Bill 1071 (2024)** | Hallucinated Context | Cited as a health insurance coinsurance reform bill. SB 1071 is an appropriations bill for the Trustees of the University of Pennsylvania (Title 24), totally unrelated to health insurance (Pennsylvania General Assembly, 2024). | **Excluded:** Removed from statutory references. |
| **Act 252 of 2023** | Non-Existent Law | Cited as a "Network Disclosure" act. Pennsylvania legislative records confirm no Act 252 was enacted in 2023. The primary 2023 health insurance enactment was Act 2 of 2023 (Insurance Data Security Act) (Pennsylvania General Assembly, 2023). | **Excluded:** Replaced with verified Act 2 of 2023 and Act 68 of 1998. |
| **Incorrect Statutory Series & Section** | Mis-codified Section | Cited as 40 P.S. § 4001 et seq. Act 2 of 2023 is codified under Pennsylvania Consolidated Statutes as 40 Pa.C.S. § 4501 et seq., not unconsolidated P.S. statutes or section 4001 (Pennsylvania General Assembly, 2023). | **Corrected:** Citation updated to 40 Pa.C.S. § 4501 et seq. |
| **§ 28-725 & § 29-8719** | Non-Existent Code | Cited as PA Insurance Code sections. Pennsylvania insurance laws are codified under Title 40 of Pennsylvania Statutes (40 P.S.) or Consolidated Statutes (40 Pa.C.S.); bare chapter-dash citations do not exist in state code (Pennsylvania Code, 2026). | **Excluded:** Replaced with Title 40 P.S. § 991.2164 et seq. |
| **Bulletin #23-04** | Mislabeled Scope | Cited as a general rate and audit bulletin. Official PID Department Notices confirm Bulletin 2023-04 specifically addresses *Medicare Supplement Guaranteed Issue Eligibility Following the COVID Public Health Emergency* — an unrelated topic (Pennsylvania Insurance Department, 2023). | **Reclassified:** Correctly annotated in source indices; not cited elsewhere in this repository as authority for rate or audit claims. |

---

## 2. Included Verified Statutory Baseline

All operational and legal logic in this project is anchored in verified Commonwealth statutes and federal regulations:

1. **Act 68 of 1998 (Quality Health Care Accountability and Protection Act):** Codified under 40 P.S. § 991.2101 et seq., establishing consumer protections, managed care organization requirements, and the 45-day prompt payment standard for clean claims (Pennsylvania General Assembly, 1998).
2. **Act 146 of 2022 (Independent External Review Act):** Establishes the state-administered Independent External Review process under PID oversight (40 P.S. § 991.2164 et seq.), enabling enrollees to appeal adverse benefit determinations with certified independent review organizations (Pennsylvania Insurance Department, 2025; Pennsylvania General Assembly, 2022).
3. **Act 2 of 2023 (Insurance Data Security Act):** Codified under 40 Pa.C.S. § 4501 et seq., establishing data security, risk assessment, and breach notification requirements for licensed insurance entities (Pennsylvania General Assembly, 2023).
4. **No Surprises Act (H.R. 133 / Public Law 116-260):** Federal protections capping out-of-network emergency and non-emergency balance billing at the Qualifying Payment Amount (QPA) (Centers for Medicare & Medicaid Services, 2024).

---

## 3. Open Verification Items

Flagged for follow-up so this repository never implies a higher confidence level than the evidence supports:

* **Per-carrier rating-area assignments** in `README.md` §1 and `data/approved_rates_2026.csv` are currently cited in aggregate to WITF's October 2025 reporting, which confirms statewide and headline (Ambetter/Partners) figures but does not itemize every carrier's rating-area footprint at that level of granularity. Each row should be checked against that carrier's individual PID rate-filing decision letter (as filed with the Department) before this table is used as a standalone citation source. Status: **unresolved**.
* **Outpatient coinsurance caps and pharmacy deductible statutes** referenced in earlier project planning (tied to Lehigh County-specific implementation questions) have not yet been matched to a verified, currently-enacted PA statute. No citation should be added for this until a specific, checkable statutory section is identified. Status: **unresolved — do not cite**.

---

## 4. References

* **Centers for Medicare & Medicaid Services.** (2024). *Pennsylvania geographic rating areas: Including state specific geographic divisions*. U.S. Department of Health and Human Services. https://www.cms.gov/cciio/programs-and-initiatives/health-insurance-market-reforms/pa-gra
* **Pennie.** (2026, February 9). *One in five Pennie enrollees drop health coverage due to expired federal tax credits* [Press release]. https://agency.pennie.com/one-in-five-pennie-enrollees-drop-health-coverage-due-to-expired-federal-tax-credits/
* **Pennsylvania Code.** (2026). *Title 40: Insurance*. Commonwealth of Pennsylvania. https://www.pacodeandbulletin.gov
* **Pennsylvania General Assembly.** (1998). *Act 68 of 1998: Quality Health Care Accountability and Protection Act*. https://www.legis.state.pa.us
* **Pennsylvania General Assembly.** (2022). *Act 146 of 2022: Independent external review process*. https://www.legis.state.pa.us
* **Pennsylvania General Assembly.** (2023). *Act 2 of 2023: Insurance data security act*. https://www.legis.state.pa.us
* **Pennsylvania General Assembly.** (2024). *Senate Bill 1071 (2023-2024 session)*. https://www.legis.state.pa.us/cfdocs/billinfo/billinfo.cfm?syear=2023&sind=0&body=S&type=B&bn=1071
* **Pennsylvania Insurance Department.** (2023). *Insurance Bulletin 2023-04: Medicare Supplement Guaranteed Issue Eligibility*. https://www.pa.gov/agencies/insurance/insurance-notices-and-bulletins
* **Pennsylvania Insurance Department.** (2025). *ACA 2026 health insurance rates and approved filings*. https://www.pa.gov/agencies/insurance/newsroom/aca-2026-health-insurance-rates
* **WITF.** (2025, October 17). *Health insurance rates for individual policies to see double-digit percent increase in 2026 in Pa.* https://www.witf.org/2025/10/17/health-insurance-rates-for-individual-policies-to-see-double-digit-percent-increase-in-2026-in-pa/
