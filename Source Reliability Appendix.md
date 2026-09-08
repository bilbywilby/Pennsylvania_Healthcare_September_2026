# Source Reliability Appendix & Fabrication Exclusions

## 1. Excluded Documents & Fact-Checking Audit

During the initial ingestion phase, an unverified analysis titled *"Cross-Sectional Metadata Analysis of Pennsylvania Health Insurance Audit Protocols and Market Structures for September 2026"* was subjected to rigorous statutory and factual verification. The document was **strictly excluded** from this repository due to critical hallucinations, non-existent statutory citations, and inverted geographical mappings.

### Summary of Exclusions and Errors

| Flagged Citation / Claim | Initial Status | Verification Finding & Primary Source Evidence | Action Taken |
| :--- | :--- | :--- | :--- |
| **Rating Area Inversion** | Fabricated Mapping | The excluded document inverted Rating Areas 1 and 8 (listing Philadelphia as Area 1 and Northwest PA as Area 8). Official CMS crosswalk files confirm Rating Area 1 is Northwest PA (Erie, Crawford, Mercer) and Area 8 is Southeast PA (Philadelphia, Bucks, Chester, Delaware, Montgomery) (Centers for Medicare & Medicaid Services, 2024). | **Corrected:** Repository adopted official CMS 2026 geographic crosswalk files. |
| **Senate Bill 1071 (2024)** | Hallucinated Context | Cited as a health insurance coinsurance reform bill. In the 2023–2024 Pennsylvania General Assembly session, SB 1071 is an appropriations bill for the Trustees of the University of Pennsylvania (Title 24), totally unrelated to health insurance (Pennsylvania General Assembly, 2024). | **Excluded:** Removed from statutory references. |
| **Act 252 of 2023** | Non-Existent Law | Cited as a "Network Disclosure" act. Pennsylvania legislative records confirm no Act 252 was enacted in 2023. The primary 2023 health insurance enactment was Act 2 of 2023 (Insurance Data Security Act) (Pennsylvania General Assembly, 2023). | **Excluded:** Replaced with verified Act 2 of 2023 and Act 68 of 1998. |
| **§ 28-725 & § 29-8719** | Non-Existent Code | Cited as PA Insurance Code sections. Pennsylvania insurance laws are codified under Title 40 of Pennsylvania Statutes (40 P.S.) or Consolidated Statutes (40 Pa.C.S.); bare chapter-dash citations do not exist in state code (Pennsylvania Code, 2026). | **Excluded:** Replaced with Title 40 P.S. § 991.2164 et seq. |
| **Bulletin #23-04** | Mislabeled Scope | Cited as a general rate and audit bulletin. Official PID Department Notices confirm Bulletin 2023-04 specifically addresses *Medicare Supplement Guaranteed Issue Eligibility Following the COVID Public Health Emergency* (Pennsylvania Insurance Department, 2023). | **Reclassified:** Correctly annotated in source indices. |

---

## 2. Included Verified Statutory Baseline

All operational and legal logic in this project is anchored in verified Commonwealth statutes and federal regulations:

1. **Act 68 of 1998 (Quality Health Care Accountability and Protection Act):** Codified under 40 P.S. § 991.2101 et seq., establishing consumer protections, managed care organization requirements, and the 45-day prompt payment standard for clean claims (Pennsylvania General Assembly, 1998).
2. **Act 146 of 2022 (Independent External Review Act):** Establishes the state-administered Independent External Review process under PID oversight (40 P.S. § 991.2164), enabling enrollees to appeal adverse benefit determinations with certified independent review organizations (Pennsylvania Insurance Department, 2025; Pennsylvania General Assembly, 2022).
3. **Act 2 of 2023 (Insurance Data Security Act):** Codified under 40 P.S. § 4001 et seq., establishing data security, risk assessment, and breach notification requirements for licensed insurance entities (Pennsylvania General Assembly, 2023).
4. **No Surprises Act (H.R. 133 / Public Law 116-260):** Federal protections capping out-of-network emergency and non-emergency balance billing at the Qualifying Payment Amount (QPA) (Centers for Medicare & Medicaid Services, 2024).

---

## 3. References

* **Centers for Medicare & Medicaid Services.** (2024). *Pennsylvania geographic rating areas*. U.S. Department of Health and Human Services. https://www.cms.gov/cciio/resources/data-resources/downloads/pa-gra.pdf
* **Pennsylvania Code.** (2026). *Title 40: Insurance*. Commonwealth of Pennsylvania. https://www.pacodeandbulletin.gov
* **Pennsylvania General Assembly.** (1998). *Act 68 of 1998: Quality Health Care Accountability and Protection Act*. https://www.legis.state.pa.us
* **Pennsylvania General Assembly.** (2022). *Act 146 of 2022: Independent external review process*. https://www.legis.state.pa.us
* **Pennsylvania General Assembly.** (2023). *Act 2 of 2023: Insurance data security act*. https://www.legis.state.pa.us
* **Pennsylvania General Assembly.** (2024). *Senate Bill 1071 (2023-2024 Session)*. https://www.legis.state.pa.us/cfdocs/billinfo/billinfo.cfm?syear=2023&sind=0&body=S&type=B&bn=1071
* **Pennsylvania Insurance Department.** (2023). *Insurance Bulletin 2023-04: Medicare Supplement Guaranteed Issue Eligibility*. https://www.pa.gov/agencies/insurance/insurance-notices-and-bulletins
* **Pennsylvania Insurance Department.** (2025). *ACA 2026 health insurance rates and approved filings*. https://www.pa.gov/agencies/insurance/newsroom/aca-2026-health-insurance-rates
* **WITF.** (2025, October 17). *Health insurance rates for individual policies to see double-digit percent increase in 2026 in Pa.* https://www.witf.org/2025/10/17/health-insurance-rates-for-individual-policies-to-see-double-digit-percent-increase-in-2026-in-pa/