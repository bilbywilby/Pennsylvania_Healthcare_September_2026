# Pennsylvania Right-to-Know Law (RTKL) Request Evaluation & Refined Templates

## 1. Review & Strategic Assessment

* **Context:** Professional / Functional (Administrative Law & Freedom of Information / Public Records).
* **Target Audience:** Agency Open-Records Officers (AORO) at the Pennsylvania Department of Human Services (DHS) and Pennie (Pennsylvania Health Insurance Exchange).
* **Proficiency Level:** Good.

### Primary Strengths
Programmatically generating RTK requests ensures consistent date handling and clear record categorization. The request shift toward 2026 Medicaid disenrollment data, Pennie coordination, and public update protocols addresses key administrative transparency issues.

---

## 2. Growth Areas & Critical Adjustments

### Area 1: Anonymity vs. Statutory Standing (65 P.S. §§ 67.702–67.703)
* **Observation:** The script included options for `[Your Name or "Anonymous Requester"]` and optional address fields.
* **Legal Context:** Under Sections 702 and 703 of the RTKL, a valid request **must** include the name and address of a legal resident of the United States. Under Office of Open Records (OOR) precedent (*e.g., Anonymous v. Downingtown Area School District*), agencies are not required to process anonymous requests. Furthermore, the OOR will dismiss any appeal filed anonymously due to a failure to establish statutory standing.
* **Actionable Step:** To maintain operational privacy while preserving legal standing, utilize a designated legal representative, journalist, or PA proxy resident as the named requester.

### Area 2: Analytical Causation vs. Objective Record Filters
* **Observation:** Item #1 requested records *"attributable to increased marketplace premiums"*.
* **Legal Context:** Under 65 P.S. § 67.703, an agency is not required to draw analytical conclusions, evaluate cause-and-effect relationships, or create new reports (*Pa. State Police v. Office of Open Records*). Requesting records "attributable to" a cause gives the agency grounds to deny the request as an improper interrogatory.
* **Actionable Step:** Request existing reports, dashboards, and correspondence containing specific overlapping search terms (e.g., `"Medicaid"` AND `"premium increase"`).

### Area 3: Standard Form Requirements (Section 504)
* **Observation:** Generating a plain `.txt` letter without standard statutory affirmations.
* **Legal Context:** Agencies are permitted under 65 P.S. § 67.504 to mandate the submission of the PA Office of Open Records Standard Form. Plain emails may be treated as "informal requests" and stripped of statutory appeal deadlines.
* **Actionable Step:** Ensure the generated request text explicitly replicates the required fields of the PA OOR Standard Form or attach the generated document to the official form.

---

## 3. Standardized RTKL Templates (2026 Disenrollment & Pennie Focus)

### Template A: Pennsylvania Department of Human Services (DHS)

```text
Subject: Right-to-Know Law Request – 2026 Medicaid Renewal, Disenrollment Data, and Pennie Coordination

Date: [Month Day, Year]

To: Agency Open-Records Officer
Pennsylvania Department of Human Services
Office of Legal Counsel – Right-to-Know Officer
P.O. Box 2675, Harrisburg, PA 17105
Email: RA-DHS-RTKL@pa.gov

Requester Information (Required under 65 P.S. § 67.703):
Name: [Full Name of Designated PA Resident / Proxy]
Mailing Address: [Street Address, City, State, ZIP]
Email: [Requester Email Address]
Telephone: [Phone Number]

Dear Open-Records Officer:

Pursuant to Pennsylvania’s Right-to-Know Law, 65 P.S. §§ 67.101–67.3104, I hereby request electronic copies of the following existing public records in the possession, custody, or control of the Pennsylvania Department of Human Services (DHS), covering the period from January 1, 2026 to the date of fulfillment:

1. Disenrollment & Renewal Reports:
   All existing final reports, executive dashboards, monthly data summaries, or statistical tables tracking Medicaid / Medical Assistance disenrollments, non-renewals, or coverage transitions referencing marketplace premiums, premium increases, or churn during calendar year 2026.

2. Inter-Agency Coordination Records:
   All written communications (including emails, attachments, memoranda, and meeting summaries) between DHS executive staff (including OMAP and OIM) and representatives of Pennie (Pennsylvania Health Insurance Exchange), the Pennsylvania Insurance Department (PID), or the Governor's Office concerning:
   a. Pennie enrollment fluctuations or premium changes affecting Medicaid transition pathways;
   b. Coordinated messaging, outreach strategies, or operational alignments for disenrolled individuals.

3. Data Publishing Schedules:
   Any standard operating procedure, schedule, directive, or protocol governing the publication timeline or update frequency for public-facing Medicaid enrollment, renewal, and termination datasets during 2026.

4. Exemption Log:
   If any responsive record is withheld or redacted, please provide an itemized privilege log citing the specific statutory exemption under 65 P.S. § 67.708 or applicable legal privilege.

SEARCH INSTRUCTIONS & KEYWORDS:
Please conduct electronic keyword searches across responsive electronic files and email systems using the following combined search strings:
- ("Medicaid" OR "Medical Assistance") AND ("Pennie" OR "marketplace") AND ("disenrollment" OR "premium")
- "renewal data" OR "churn report" OR "enrollment dashboard"

PREFERRED FORMAT & FEES:
Please provide all responsive records electronically in their native format (e.g., PDF, .xlsx, .eml). If processing fees are anticipated to exceed $25.00, please notify me prior to fulfilling the request.

Sincerely,

[Requester Name]
```

---

### Template B: Pennie (Pennsylvania Health Insurance Exchange)

```text
Subject: Right-to-Know Law Request – 2026 Marketplace Premium Impacts and DHS Coordination Records

Date: [Month Day, Year]

To: Agency Open-Records Officer
Pennie (Pennsylvania Health Insurance Exchange)
312 Market Street, Suite 300
Harrisburg, PA 17101
Email: RTKL@pennie.com

Requester Information (Required under 65 P.S. § 67.703):
Name: [Full Name of Designated PA Resident / Proxy]
Mailing Address: [Street Address, City, State, ZIP]
Email: [Requester Email Address]
Telephone: [Phone Number]

Dear Open-Records Officer:

Pursuant to Pennsylvania’s Right-to-Know Law, 65 P.S. §§ 67.101–67.3104, I hereby request electronic copies of the following existing public records in the possession, custody, or control of Pennie covering the period from January 1, 2026 to the date of fulfillment:

1. Exchange Enrollment & Churn Data:
   All existing statistical reports, monthly executive briefings, or dashboards reflecting exchange enrollment changes, plan switches, or coverage losses associated with 2026 premium modifications.

2. DHS & Inter-Agency Communications:
   Emails, memoranda, and briefing materials exchanged between Pennie executive leadership or policy directors and the PA Department of Human Services (DHS) regarding:
   a. Transition of disenrolled Medicaid beneficiaries to Pennie coverage during 2026;
   b. Joint agency outreach efforts, enrollment projections, or financial assistance modifications.

3. Log of Withheld Records:
   If any record is withheld or redacted, please provide an itemized log identifying the document date, author, recipient, and statutory basis under 65 P.S. § 67.708.

SEARCH KEYWORDS:
- ("Pennie" OR "Exchange") AND ("Medicaid" OR "DHS") AND ("premium" OR "enrollment decline")
- "transition report" OR "disenrollment data"

PREFERRED FORMAT & FEES:
Please deliver responsive records electronically in native format. Please notify me if total fees will exceed $25.00.

Sincerely,

[Requester Name]
```

---

## 4. Legally Compliant Python Generator Script

Below is the updated `rtk_request.py` script. It enforces required statutory fields (preventing procedural rejections) while keeping output generation automated.

```python
#!/usr/bin/env python3
"""
Generates statutory-compliant PA Right-to-Know Law (RTKL) requests for DHS & Pennie.
Enforces 65 P.S. § 67.703 compliance (requester name & address requirements).
"""
import datetime
import os

DHS_TEMPLATE = """Subject: Right-to-Know Law Request – 2026 Medicaid Renewal and Pennie Coordination Records

Date: {today}

To: Agency Open-Records Officer
Pennsylvania Department of Human Services
Office of Legal Counsel – Right-to-Know Officer
P.O. Box 2675, Harrisburg, PA 17105
Email: RA-DHS-RTKL@pa.gov

Requester Information:
Name: {name}
Mailing Address: {address}
Email: {email}
Telephone: {phone}

Dear Open-Records Officer:

Pursuant to Pennsylvania’s Right-to-Know Law, 65 P.S. §§ 67.101–67.3104, I hereby request electronic copies of the following existing public records in the possession, custody, or control of DHS, covering the period from January 1, 2026 through the date of this response:

1. All existing reports, dashboards, or statistical tables tracking Medicaid/Medical Assistance disenrollments, non-renewals, or transitions referencing marketplace premiums or enrollment changes during calendar year 2026.
2. Written communications (including emails, attachments, and memoranda) between DHS executive staff and representatives of Pennie or the PA Insurance Department concerning Pennie enrollment fluctuations or joint outreach strategies between January 1, 2026 and the present.
3. Schedules, standard operating procedures, or protocols governing the public release or update frequency of DHS Medicaid enrollment and termination datasets during 2026.

Please deliver all records electronically in native format. If any portion is denied, please provide an itemized exemption log pursuant to 65 P.S. § 67.708.

Sincerely,

{name}
"""

def main():
    today = datetime.date.today().strftime("%B %d, %Y")
    
    print("=== PA RTKL Request Generator ===")
    print("Note: 65 P.S. § 67.703 requires a valid name & address to maintain legal standing.\n")
    
    name = input("Requester Full Name: ").strip()
    address = input("Mailing Address (Street, City, ST, ZIP): ").strip()
    email = input("Email Address: ").strip()
    phone = input("Telephone (Optional): ").strip() or "N/A"
    
    if not name or not address or not email:
        print("\n[ERROR] Name, Address, and Email are legally required under RTKL Section 703.")
        return

    content = DHS_TEMPLATE.format(
        today=today,
        name=name,
        address=address,
        email=email,
        phone=phone
    )
    
    filename = "rtk_request_dhs_2026.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"\n[SUCCESS] Request saved to '{filename}'.")
    print("Submit via email to RA-DHS-RTKL@pa.gov and attach the PA Standard OOR Request Form if required.")

if __name__ == "__main__":
    main()
```

---

## 5. Summary of Procedural Best Practices

| Requirement | Statutory Citation | Operational Recommendation |
| :--- | :--- | :--- |
| **Requester Identity** | 65 P.S. §§ 67.702 / 703 | Provide full legal name & address; use a designated PA proxy if personal privacy is required. |
| **Specificity Standard** | 65 P.S. § 67.703 | Combine broad terms (e.g., `"Medicaid"` AND `"premium"`). Avoid asking *why* or requesting *causal proof*. |
| **Response Window** | 65 P.S. § 67.901 | 5 business days from receipt. 30-day extensions require written notice under § 67.902. |
| **Appeal Window** | 65 P.S. § 67.1101 | 15 business days from a written denial or deemed denial date to appeal to the Office of Open Records. |