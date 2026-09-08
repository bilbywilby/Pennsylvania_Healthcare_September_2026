# Pennsylvania Right-to-Know (RTK) Request: Operational Strategy & Automation Guide

---

## 1. Dual-Agency Submission Strategy

Because Pennsylvania decouples public health benefit administration from its commercial exchange, determine whether your request requires dual submission:

* **PA Department of Human Services (DHS)**
  * **Scope:** Medical Assistance (Medicaid), CHIP enrollment, fee-for-service data, and Managed Care Organization (MCO) capitation contracts.
  * **Submission Channel:** [Official PA DHS RTK Portal](https://www.dhs.pa.gov) or direct email to the designated DHS Agency Open-Records Officer (AORO).

* **Pennie (PA Health Insurance Exchange Authority)**
  * **Scope:** Commercial marketplace operations, ACA plan enrollment, individual market outreach, and exchange-level communications.
  * **Submission Channel:** Direct email/mail to Pennie’s designated Open-Records Officer.

> **Recommendation:** If your query bridges Medicaid unwinding, transitions to exchange plans, or joint communications, submit parallel RTK requests to both entities simultaneously.

---

## 2. Search Parameter Optimization & Denials Prevention

Under **65 P.S. § 67.503**, agencies frequently issue 30-day extensions or initial denials citing an *insufficiently specific request* (**Section 703**). Apply the following refinements:

### Key Custodians (Scope Restriction)
* **Office of Income Maintenance (OIM)**
* **Office of Medical Assistance Programs (OMAP)**
* **Office of Communications**

### Recommended Search Term Variations (Boolean & Exact Match)
To capture internal agency dialogue and draft guidance, include variations such as:
* `"10% loss stop"` | `"10 percent loss stop"` | `"loss-stop"`
* `"communication pause"` | `"communications freeze"` | `"outreach moratorium"`
* `"MLR threshold"` | `"capitation adjustment"`

---

## 3. Submission Protocol & Statutory Timeline

Under **Section 901**, the agency must respond within **5 business days** of receiving the request.

| Timeline Milestone | Event / Action Required | Statutory Reference |
| :--- | :--- | :--- |
| **Day 0** | Request submitted. Retain automated portal receipt or sent-email headers. | — |
| **Day 5** | Mandatory Agency Response Due: Fulfillment, Denial, or Section 902 Notice. | 65 P.S. § 67.901 |
| **Day 5 + 30 Days** | Maximum extension period if Section 902 extension invoked. | 65 P.S. § 67.902 |

---

## 4. Terminal Automation Workflows

### File Path Verification
The template is located at:
```text
/home/droid/whysoquit/rtk_request.txt
```

To verify file existence and preview content:
```bash
# Verify file listing
ls -l ~/whysoquit/rtk_request.txt

# Search entire home directory if path moves
find ~ -type f -name 'rtk_request.txt' 2>/dev/null

# Preview header and footer of document
sed -n '1,35p' ~/whysoquit/rtk_request.txt
tail -35 ~/whysoquit/rtk_request.txt

# Locate remaining unpopulated placeholder brackets
grep -nE '\[[^]]+\]' ~/whysoquit/rtk_request.txt
```

### Direct String Replacement & Final Compilation
Run the following script block to populate applicant metadata and output `rtk_request_final.txt`:

```bash
# Set environment variables
NAME="Anthony Dee"
ADDR="Your Street Address"
CITY_ZIP="Allentown, PA 18101"
EMAIL="your.email@domain.com"
PHONE="555-555-5555"

# Run batch replacements using sed
sed -e "s/\[Your full name\]/$NAME/g" \
    -e "s/\[Your mailing address\]/$ADDR/g" \
    -e "s/\[City, State ZIP\]/$CITY_ZIP/g" \
    -e "s/\[Your email address\]/$EMAIL/g" \
    -e "s/\[Your telephone number, optional\]/$PHONE/g" \
    -e "s/\[START DATE\] through \[END DATE\]/January 01, 2024 through September 07, 2026/g" \
    ~/whysoquit/rtk_request.txt > ~/whysoquit/rtk_request_final.txt
```

### Post-Processing Verification
After running the script, confirm that no unpopulated brackets remain:

```bash
grep -nE '\[[^]]+\]' ~/whysoquit/rtk_request_final.txt
```

If the command returns no output, the request file is ready for submission.