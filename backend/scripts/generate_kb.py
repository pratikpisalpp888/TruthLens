"""
TruthLens — Full Knowledge Base Generator (125+ documents).
"""

import os

KB_DOCS = {
    "banking_rules": {
        "rbi_loan_underwriting.md": """# RBI Loan Underwriting Guidelines

## Overview
The Reserve Bank of India (RBI) mandates that all Scheduled Commercial Banks adhere to a structured underwriting framework before disbursing any loan, especially in the retail and MSME segment.

## Key Principles
- **Know Your Customer (KYC)**: Banks must complete full KYC before sanctioning any loan. This includes identity proof, address proof, and income proof.
- **Credit Appraisal**: Each loan application must be evaluated for creditworthiness using CIBIL scores, income verification, and repayment history.
- **Income Verification**: Declared income must be corroborated through ITR filings for at least 2 consecutive financial years, Form 16, and bank statements.
- **Loan-to-Value (LTV)**: For home loans, the LTV ratio must not exceed 80% for loans up to ₹30 lakhs, and 75% for loans above ₹75 lakhs.
- **Debt-to-Income (DTI)**: Monthly EMI obligations should not exceed 50% of the applicant's net monthly income.
- **End-Use Monitoring**: Banks must ensure loan proceeds are used only for the declared purpose.

## Red Flags in Underwriting
- Sudden income spike within 2 years of loan application
- Unexplained large bank deposits
- Mismatch between ITR income and bank statement credits
- Multiple loan applications across different banks in short duration
""",
        "rbi_kyc_guidelines.md": """# RBI KYC Guidelines (Master Direction 2016)

## Purpose
The RBI's KYC Master Direction requires banks to establish the identity and address of customers through a risk-based approach to prevent money laundering and financing of terrorism.

## Documents Accepted
- **Identity Proof**: Aadhaar, PAN Card, Passport, Voter ID, Driving Licence
- **Address Proof**: Utility bills (not older than 3 months), Bank account statement, Aadhaar

## e-KYC via Aadhaar
Banks are permitted to use Aadhaar-based e-KYC (Biometric or OTP-based) with UIDAI consent for account opening and loan applications.

## Periodic KYC Update
- High-risk customers: every 2 years
- Medium-risk customers: every 8 years
- Low-risk customers: every 10 years

## Critical Compliance Points
- A customer's PAN must be linked to Aadhaar for transactions above ₹2 lakhs.
- Failure to update KYC may result in account freeze.
- Banks must file STR (Suspicious Transaction Report) if KYC documents appear forged.
""",
        "rbi_income_verification.md": """# RBI Income Verification Requirements

## ITR-Based Income Verification
The RBI requires banks to verify income through Income Tax Returns (ITR) for self-employed individuals, proprietors, and partners.

- Minimum 2 years ITR required
- ITR must be filed and acknowledged (not just prepared)
- Acknowledgement from Income Tax portal must match PAN
- Gross Total Income (GTI) from ITR is used as baseline income

## Salaried Employees
- Form 16 from employer for last 2 years
- Latest 3 months salary slips
- Bank statement showing salary credits

## Business Owners / Professionals
- Last 2 years audited balance sheets and P&L accounts
- GST returns (GSTR-1, GSTR-3B) for last 2 years
- CA-certified income computation

## Income Cross-Check
- Bank statement credits must be consistent with declared ITR income
- A deviation of more than 30% between bank credits and ITR income is a major red flag
- Large unexplained deposits must be explained with documented evidence
""",
        "rbi_property_valuation.md": """# RBI Property Valuation Guidelines

## Valuation Framework
RBI mandates that any property offered as collateral for a loan must be valued by an empanelled valuer.

## Empanelled Valuers
- Banks must maintain a panel of approved valuers
- Valuers must be RICS or government-approved
- Valuation must be independent (no relationship with borrower)

## Valuation Methods
1. **Comparable Sales Method**: Based on recent sales in the same locality
2. **Income Capitalization**: For income-generating properties
3. **Cost Approach**: Based on land value + replacement cost

## LTV Ratios
| Loan Amount | Max LTV |
|---|---|
| Up to ₹30 lakhs | 90% |
| ₹30 lakhs to ₹75 lakhs | 80% |
| Above ₹75 lakhs | 75% |

## Red Flags in Valuation
- Valuation date more than 6 months old at time of loan sanction
- Value significantly higher than market comparable
- Missing encumbrance certificate
- Disputed title or pending court cases
""",
        "rbi_fraud_reporting.md": """# RBI Fraud Reporting Guidelines (Master Direction 2023)

## Fraud Classification
RBI classifies fraud under multiple categories:
- Misrepresentation and cheating
- Forgery and alteration of documents
- Identity fraud
- Coordinated/syndicated fraud

## Reporting Timelines
- FMR-1 (Individual fraud): Must be filed within 3 weeks of detection
- Frauds above ₹1 crore: Direct reporting to CBI/State Police
- Frauds above ₹100 crore: Report to SEBI/MCA as well

## Early Warning Signals (EWS)
Banks must monitor:
- Return of cheques more than 3 times
- Sudden increase in cash withdrawals
- Multiple loan accounts at the same address
- Loan restructuring within 1 year of disbursement

## Preventive Measures
- CERSAI check mandatory before home loan sanction
- CIBIL/Equifax/Experian tri-bureau check required
- Field investigation must confirm property existence
""",
        "rbi_npa_classification.md": """# RBI NPA Classification Norms

## Definition of NPA
A loan account becomes a Non-Performing Asset (NPA) when:
- Interest or principal remains overdue for more than 90 days (for term loans)
- Account remains out of order for more than 90 days (for cash credit/overdraft)

## Sub-Classifications
1. **Sub-Standard Asset**: NPA for less than or equal to 12 months
2. **Doubtful Asset**: NPA for more than 12 months
3. **Loss Asset**: Written off but not fully recovered

## Provisioning Requirements
| Category | Provision Required |
|---|---|
| Sub-Standard | 15% |
| Doubtful 1 (12-24 months) | 25% |
| Doubtful 2 (24-36 months) | 40% |
| Doubtful 3 (>36 months) | 100% |
| Loss | 100% |

## Early NPA Warning Signs
- Failure to submit financial statements
- Frequent overdrawing of account
- Diversion of loan funds to unrelated accounts
- Income mismatch relative to EMI
""",
        "loan_to_value_ratios.md": """# Loan-to-Value (LTV) Ratio Standards

## Definition
LTV is the ratio of the loan amount to the appraised value of the asset being purchased or used as collateral.

## Home Loans
| Property Value | Maximum LTV |
|---|---|
| Up to ₹30 lakhs | 90% |
| ₹30L - ₹75L | 80% |
| Above ₹75L | 75% |

## Loan Against Property (LAP)
- Residential: 60-65%
- Commercial: 50-55%

## Vehicle Loans
- New vehicle: up to 90%
- Used vehicle: up to 70-75%

## Gold Loans
- Maximum 75% of gold value (as per RBI directive)

## Risk Implications
Higher LTV means higher lender risk. Banks typically require mortgage insurance for LTV > 80%. LTV manipulation via inflated property valuation is a common fraud pattern.
""",
        "debt_to_income_standards.md": """# Debt-to-Income (DTI) Standards for Loan Assessment

## Definition
DTI is the ratio of total monthly debt obligations to gross monthly income. It is a primary metric for assessing loan repayment capacity.

## RBI Guidance
While RBI does not mandate a specific DTI ceiling, industry practice in India recommends:
- Front-end DTI (housing expenses only): < 28%
- Back-end DTI (all debts): < 43-50%

## Canara Bank Internal Guidelines
- Gross monthly EMI should not exceed 50% of net monthly take-home pay
- Existing EMI burden + new EMI must stay within the 50% ceiling

## Calculation Method
DTI = (Monthly EMI obligations / Gross Monthly Income) × 100

## Red Flags
- DTI exceeding 60% with inadequate collateral
- Undisclosed existing loans from other banks
- Loans taken out in family member names to circumvent DTI limits
- Fictitious income inflation to lower apparent DTI ratio
""",
        "collateral_requirements.md": """# Collateral Requirements for Bank Loans

## Purpose
Collateral is any asset pledged by a borrower to secure a loan. It protects the lender in case of default.

## Types of Accepted Collateral
1. **Immovable Property**: Residential or commercial premises
2. **Agricultural Land**: With proper revenue records
3. **Fixed Deposits**: Bank FDs or NSC certificates
4. **Insurance Policies**: Surrender value-based
5. **Listed Shares**: With 50% margin requirement
6. **Gold/Jewellery**: For gold loans

## Title Verification for Property Collateral
- Title search for minimum 30 years
- Encumbrance certificate for 15 years
- Latest land records (7/12 extract or pattadar passbook)
- Sale deed and previous chain of ownership

## CERSAI Registration
Central Registry of Securitisation Asset Reconstruction and Security Interest (CERSAI) registration is mandatory for all property-backed loans to prevent multiple financing on the same property.

## Red Flags
- Property disputed in court
- Missing encumbrance certificate
- Unauthorized construction
- Mismatch between registered area and actual area
""",
        "documentation_checklist.md": """# Loan Documentation Checklist

## Mandatory Documents for All Loan Types
- Completed loan application form
- PAN card of all applicants and guarantors
- Aadhaar card (OTP-based or biometric verified)
- Passport-size photographs

## Income Proof (Salaried)
- Last 3 months salary slips
- Form 16 for last 2 years
- Bank statement of salary account for 12 months

## Income Proof (Self-Employed)
- Last 2 years ITR with acknowledgement
- Last 2 years audited financial statements
- GST returns (GSTR-1, GSTR-3B) for 12 months
- Bank statements of business accounts for 12 months

## Property Documents (for Home/LAP Loans)
- Approved building plan
- Encumbrance Certificate (last 15 years)
- Property tax receipts
- NOC from society/builder
- Sale deed / title deed / agreement to sale

## Red Flags to Check
- Suspiciously new documents for old transactions
- Mismatch in dates, names, or property descriptions across documents
- Absence of proper stamp duty and registration
""",
    },
    "itr_rules": {
        "section_80c_deductions.md": """# Section 80C Deductions

## Maximum Deduction Limit
Under Section 80C of the Income Tax Act, 1961, the maximum deduction allowed is ₹1,50,000 per financial year.

## Eligible Investments and Payments
- Life Insurance Premium (LIC and other insurers)
- Public Provident Fund (PPF) contributions
- National Savings Certificate (NSC)
- Employee Provident Fund (EPF) — employee contribution only
- Equity Linked Saving Scheme (ELSS) — 3-year lock-in
- Sukanya Samriddhi Yojana (SSY)
- Principal repayment of Home Loan
- Tuition fees for children's education (up to 2 children)
- 5-year Fixed Deposits with scheduled banks
- Senior Citizen Savings Scheme (SCSS)

## Common Fraudulent Claims
- Claiming 80C deduction without actual investment
- Submitting forged LIC/PPF statements
- Claiming deductions exceeding ₹1,50,000 in ITR

## Verification Method
- Cross-check with Form 26AS for TDS on interest
- EPF statement from EPFO portal
- LIC premium receipts with policy numbers
""",
        "section_80d_deductions.md": """# Section 80D Deductions — Health Insurance

## Deduction Limits
| Scenario | Maximum Deduction |
|---|---|
| Self + Family (age < 60) | ₹25,000 |
| Self + Family (age >= 60) | ₹50,000 |
| Parents (age < 60) | ₹25,000 |
| Parents (age >= 60) | ₹50,000 |
| Maximum total (senior citizen parents) | ₹1,00,000 |

## Eligible Premiums
- Medical insurance (Mediclaim) premiums
- Preventive health check-up: up to ₹5,000 (within the above limits)
- CGHS contribution (for government employees)

## Payment Mode
Deduction is not allowed for cash payments above ₹5,000.

## Fraud Indicators
- Claiming 80D without valid policy number
- Premium paid for non-existent family members
- Duplicate claim across multiple financial instruments
""",
        "tax_slabs_old_regime.md": """# Income Tax Slabs — Old Regime (FY 2024-25)

## Individual (Below 60 years)
| Income Slab | Tax Rate |
|---|---|
| Up to ₹2.5 lakhs | NIL |
| ₹2.5L to ₹5L | 5% |
| ₹5L to ₹10L | 20% |
| Above ₹10L | 30% |

## Senior Citizens (60-80 years)
| Income Slab | Tax Rate |
|---|---|
| Up to ₹3 lakhs | NIL |
| ₹3L to ₹5L | 5% |
| ₹5L to ₹10L | 20% |
| Above ₹10L | 30% |

## Surcharge
- 10% surcharge if income is between ₹50L and ₹1 crore
- 15% surcharge if income is between ₹1 crore and ₹2 crore
- 25% surcharge if income > ₹2 crore

## Health & Education Cess
4% of (income tax + surcharge)

## Rebate under Section 87A
Full rebate of tax if taxable income ≤ ₹5 lakhs under old regime.
""",
        "tax_slabs_new_regime.md": """# Income Tax Slabs — New Regime (FY 2024-25)

## New Regime Slabs (Default from FY 2023-24)
| Income Slab | Tax Rate |
|---|---|
| Up to ₹3 lakhs | NIL |
| ₹3L to ₹6L | 5% |
| ₹6L to ₹9L | 10% |
| ₹9L to ₹12L | 15% |
| ₹12L to ₹15L | 20% |
| Above ₹15L | 30% |

## Key Differences from Old Regime
- Standard deduction of ₹50,000 is available under new regime
- Most other deductions (80C, 80D, HRA) are NOT available
- No deduction for home loan interest under Section 24

## Rebate under Section 87A (New Regime)
Full rebate if taxable income ≤ ₹7 lakhs (after standard deduction).

## Health & Education Cess
4% applies in both regimes.

## Fraud Detection Note
A common manipulation is claiming old regime deductions (80C, 80D, HRA) but computing tax under new regime slabs, artificially reducing tax liability.
""",
        "itr_form_types.md": """# ITR Form Types and Eligibility

## ITR-1 (SAHAJ)
- Applicable for resident individuals only
- Income sources: salary, one house property, other sources
- Income limit: up to ₹50 lakhs
- NOT applicable: business income, capital gains, foreign assets

## ITR-2
- Individuals and HUFs NOT having business income
- Applicable for: Capital gains, multiple house properties, foreign income/assets
- No income limit

## ITR-3
- Individuals and HUFs having income from business or profession
- Applicable for: Partnership firm partners, those with stock trading as business

## ITR-4 (SUGAM)
- Applicable for individuals, HUFs, and firms (non-LLP)
- Presumptive income under Sections 44AD, 44ADA, 44AE
- Income limit: up to ₹50 lakhs (₹2 crore for 44AD)

## ITR-5
- For firms, LLPs, AoPs, BoIs (not individuals/HUF)

## ITR-6
- For companies (other than those claiming Section 11 exemption)

## Fraud Indicators
- A business owner filing ITR-1 (designed only for salaried) to understate income
- Filing ITR-4 with turnover exceeding the 44AD/44ADA threshold
""",
        "tds_provisions.md": """# TDS Provisions and Verification

## Common TDS Sections
| Section | Nature of Payment | TDS Rate |
|---|---|---|
| 192 | Salary | As per slab |
| 194A | Interest (other than securities) | 10% |
| 194C | Contractor payments | 1%/2% |
| 194H | Commission or brokerage | 5% |
| 194I | Rent | 10% |
| 194J | Professional fees | 10% |

## Form 26AS and AIS
All TDS deducted is reflected in Form 26AS (Tax Credit Statement) and Annual Information Statement (AIS). Lenders must cross-check ITR income with Form 26AS to ensure declared income is genuine.

## TDS Mismatch Red Flags
- TDS in Form 26AS does not match TDS claimed in ITR
- Absence of TDS for salaried income (employer not deducting tax)
- TDS credits from unknown or suspicious deductors

## Refund Patterns
A large refund claim in ITR (especially if taxpayer has minimal TDS history) is a flag for income manipulation.
""",
        "pan_validation_rules.md": """# PAN Validation Rules

## PAN Format
PAN (Permanent Account Number) follows a 10-character alphanumeric structure:
- Characters 1-3: AAA (alphabets, first 3 letters are series)
- Character 4: Type of taxpayer
  - P = Person
  - C = Company
  - H = HUF (Hindu Undivided Family)
  - F = Firm
  - A = AoP (Association of Persons)
  - T = Trust
  - B = BoI (Body of Individuals)
  - L = Local Authority
  - J = Artificial Juridical Person
  - G = Government
- Character 5: First letter of taxpayer's last name (for individuals)
- Characters 6-9: 4 numeric digits
- Character 10: Alphabetic check digit

## Validation Rules
1. Format must strictly be: `[A-Z]{5}[0-9]{4}[A-Z]{1}`
2. The 4th character must match the taxpayer type
3. PAN must be present and identical in all submitted documents

## Verification
- PAN can be verified at the Income Tax e-filing portal
- Banks must verify PAN before loan sanction
- NSDL/UTI portal can be used for quick validation
""",
    },
    "property_rules": {
        "sale_deed_requirements.md": """# Sale Deed Requirements for Loan Documentation

## What is a Sale Deed?
A Sale Deed is a legal document executed when the seller transfers absolute ownership of property to the buyer. It is registered at the Sub-Registrar's office.

## Mandatory Clauses
- Full names and addresses of vendor (seller) and vendee (buyer)
- Complete description of the property with survey number, area, boundaries
- Sale consideration (agreed price)
- Mode of payment confirmation
- Representations and warranties on title
- Possession transfer date

## Registration Requirements
- Must be compulsorily registered under Section 17 of the Registration Act, 1908
- Stamp duty must be paid (as per state government rates)
- Two witnesses are required at the time of registration
- Signature and thumbprint of both parties

## Common Fraud Indicators
- Sale deed dated in the past but recently printed on new paper
- Mismatched survey numbers in sale deed vs land records
- Names spelled differently than in KYC documents
- Sale consideration significantly below market value (stamp duty evasion)
- Multiple sale deeds for the same property
""",
        "title_verification_process.md": """# Title Verification Process for Loan Collateral

## Purpose
Title verification ensures that the property offered as collateral has a clean, marketable title and is free from encumbrances.

## Steps in Title Verification
1. **Document Chain**: Verify the chain of ownership for at least 30 years
2. **Encumbrance Certificate**: Check if any loans or charges exist on the property
3. **Revenue Records**: Verify land records (7/12 extract, pattadar passbook, or Bhu-Naksha)
4. **CERSAI Search**: Mandatory search for any registered security interest
5. **Society NOC**: For apartment purchases, NOC from the housing society
6. **Approved Plan**: Municipality-approved building plan

## Title Defects to Watch
- Properties with disputed ownership
- Properties under government acquisition notice
- Agricultural land converted without proper CLU (Change of Land Use) order
- Inheritance properties without proper succession documentation

## Legal Opinion
Banks require a legal opinion from an empanelled advocate on the property's title before disbursement.
""",
        "encumbrance_certificate.md": """# Encumbrance Certificate (EC)

## Definition
An Encumbrance Certificate (EC) is a document issued by the Sub-Registrar's office showing all registered transactions on a property over a specified period.

## Types
- **Form 15**: When there are encumbrances (loans, mortgages, rights of way)
- **Form 16 (Nil EC)**: When no encumbrances are found

## Period Required by Banks
- Minimum 15 years of EC
- Some banks require 30 years

## Information in EC
- Nature of transaction (sale, mortgage, gift, etc.)
- Date of transaction
- Parties involved
- Loan amounts (for mortgages)

## Fraud Detection
- If EC shows no loans but the property was used as collateral elsewhere, investigate
- CERSAI registration may reveal loans not reflected in EC
- Fresh EC should be obtained close to loan sanction date
""",
        "stamp_duty_guidelines.md": """# Stamp Duty Guidelines for Property Documents

## What is Stamp Duty?
Stamp duty is a tax levied by state governments on the transfer of property. Under the Indian Stamp Act, 1899, inadequate stamp duty renders a document inadmissible in court.

## State-wise Rates (Approximate)
| State | Stamp Duty |
|---|---|
| Maharashtra | 6-7% |
| Karnataka | 5-7% |
| Delhi | 4-6% |
| Tamil Nadu | 7% |
| Gujarat | 4.9% |

## Calculation Basis
Stamp duty is calculated on the higher of:
- Declared sale consideration, or
- State government's Ready Reckoner (circle) rate

## Red Flags
- Stamp duty paid on unusually low declared value (undervaluation)
- Stamp paper date and registration date mismatch by large period
- Use of impounded/cancelled stamp paper
- Registration in a different state to avoid higher stamp duty
""",
        "cersai_registration.md": """# CERSAI Registration

## What is CERSAI?
Central Registry of Securitisation Asset Reconstruction and Security Interest (CERSAI) is a statutory body that maintains a central database of all security interests created on properties.

## Legal Basis
Created under the Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act, 2002 (SARFAESI).

## Registration Requirement
- Mandatory for all mortgages created in favour of banks and financial institutions
- Must be filed within 30 days of creation of security interest
- Failure to register: Bank cannot enforce SARFAESI proceedings

## Search Before Sanction
Banks must search CERSAI before sanctioning any property-backed loan to avoid:
- Dual financing on the same property
- Fraudulent mortgage creation by borrowers who have already mortgaged the property elsewhere

## Fraud Scenarios Caught by CERSAI
- Borrower mortgages the same property to 5 different banks
- Property already under SARFAESI action but sold to a new buyer
""",
    },
    "fraud_patterns": {
        "income_inflation_fraud.md": """# Income Inflation Fraud

## Overview
Income inflation fraud involves a borrower artificially increasing their declared income to qualify for a higher loan amount or to meet lender's minimum income criteria.

## Common Techniques
1. **ITR Manipulation**: Filing ITR with inflated gross total income not supported by actual TDS or bank credits
2. **Form 16 Forgery**: Creating fake or altered Form 16 to show higher salary than actual
3. **Salary Slip Forgery**: Printing counterfeit salary slips with inflated figures
4. **Shell Company Income**: Creating a paper company that issues fake salary certificates
5. **Overinflated Business Turnover**: Showing GST invoices for non-existent transactions to inflate business income

## Detection Indicators
- Bank credits significantly lower than ITR declared income
- TDS on Form 26AS does not correlate with declared salary
- Company issuing Form 16 doesn't exist in MCA/GST records
- GST GSTR-1 returns show different turnover than declared in ITR

## Case Pattern in Indian Banking
This fraud is highly prevalent in home loan and MSME loan segments. Borrowers collude with chartered accountants to file inflated ITRs a few years before applying for a loan, then default after disbursement.
""",
        "property_document_forgery.md": """# Property Document Forgery

## Overview
Property document forgery involves creating, altering, or misrepresenting legal documents related to real estate to fraudulently obtain loans.

## Common Forged Documents
1. **Sale Deed**: Fabricated or altered sale deeds with different survey numbers or values
2. **Encumbrance Certificate**: Forged nil-EC to hide existing mortgages
3. **7/12 Extract**: Altered land records showing forger as owner
4. **Building Plan**: Fake municipal approval plans
5. **NOC from Society**: Forged society no-objection certificates

## Detection Techniques
- Cross-verification of survey number with revenue department
- CERSAI search to detect hidden mortgages
- Online verification of EC from state government portal
- Forensic examination of document printing (ELA, metadata, font analysis)
- Comparison of property boundaries across multiple documents

## Red Flags
- Documents printed on suspiciously uniform paper even for old transactions
- Same notary for all documents in the case
- Quantum jump in property area between documents
- Registration date very recent relative to property's stated age
""",
        "identity_fraud_patterns.md": """# Identity Fraud Patterns

## Overview
Identity fraud in banking occurs when a borrower misrepresents their identity or uses stolen identities to obtain loans.

## Categories
1. **Synthetic Identity Fraud**: Combining real and fictitious information to create a new identity
2. **Identity Theft**: Using another person's PAN, Aadhaar, and documents
3. **First-Party Fraud**: The actual applicant misrepresents income, assets, or employment
4. **Third-Party Fraud**: A fraudster uses stolen identity without the victim's knowledge

## Common Techniques
- Stolen or manipulated Aadhaar cards
- Multiple PANs for the same individual
- Name variations across documents (to avoid CIBIL negative flag)
- Fake employment letters from shell companies

## Detection Methods
- Biometric verification through UIDAI APIs
- Cross-checking PAN-Aadhaar linkage status
- Field investigation at declared residence and office address
- OCR-based name comparison across all submitted documents with fuzzy match
""",
        "coordinated_fraud_rings.md": """# Coordinated Fraud Rings

## Overview
A coordinated fraud ring is an organized network of fraudsters — including borrowers, property sellers, chartered accountants, and sometimes bank insiders — who collaborate to execute systematic loan fraud.

## How They Operate
1. **Property Flip Syndicate**: A group buys distressed property cheaply, inflates its value through fake sale deeds, and repeatedly mortgages it to different banks.
2. **Shell Company Network**: Multiple shell companies issue fake employment letters, salary slips, and Form 16 for the same pool of "borrowers."
3. **Same Notary Pattern**: Multiple cases in a geographic area all pass through the same notary — a classic indicator of a coordinated operation.
4. **Bank Insider Collaboration**: Loan officers approve cases without adequate due diligence, sometimes in return for bribes.

## Detection via Graph Analysis
- Network graph: cases sharing the same notary, property locality, or CA
- Printer fingerprint matching across documents from different "applicants"
- CIBIL inquiry clustering — multiple loans applied in the same week
- Aadhaar linkage: same address for multiple unrelated applicants

## Regulatory Action
RBI requires banks to immediately file an FIR and submit a fraud report to the Central Fraud Monitoring Cell (CFMC) upon detection of a fraud ring.
""",
        "itr_manipulation_techniques.md": """# ITR Manipulation Techniques

## Overview
ITR manipulation is one of the most common fraudulent practices in India's loan ecosystem. Fraudsters exploit the ITR self-assessment mechanism to artificially inflate declared income.

## Known Techniques

### 1. Late Filing with Inflated Income
Borrowers file belated ITRs (with inflated GTI) just before submitting a loan application, then don't pay the actual tax.

### 2. Revised Returns
Filing a revised ITR showing higher income to replace the original low-income return.

### 3. Fake Acknowledgement Numbers
Generating fake 15-digit acknowledgement numbers that mimic the Income Tax Department's format.

### 4. Rounding Suspicious Amounts
Declaring suspiciously round income figures (e.g., exactly ₹12,00,000) that rarely appear in genuine filings.

### 5. Missing Tax Payments
Declaring high income in ITR but with zero advance tax payments or TDS, which would be inconsistent.

## Detection Signals
- Verify acknowledgement on incometax.gov.in portal
- Cross-check with Form 26AS for TDS correlation
- Check TAN of employer on portal
- Mismatch between AY and filing date in ITR
""",
        "bank_statement_fabrication.md": """# Bank Statement Fabrication

## Overview
Bank statement fabrication involves creating or altering printed/digital bank statements to show higher balances or credits than actually exist.

## Common Methods
1. **Image Editing**: Using Photoshop or GIMP to alter scanned bank statements
2. **HTML/CSS Manipulation**: Downloading bank statements in HTML format and editing them in a text editor
3. **Template-Based Forgery**: Creating fake statements from scratch using stolen bank letterheads
4. **Selective Printing**: Printing only the "good months" from a multi-month statement

## Detection Indicators
- ELA (Error Level Analysis) shows compression artifacts from image editing
- PDF metadata reveals editing software (Photoshop, GIMP)
- Font inconsistency within the same statement
- Account number format doesn't match bank's standard
- IFSC code doesn't correspond to the named branch
- Closing balance in month N doesn't equal opening balance in month N+1
- Missing pages (single-page statements for accounts with many transactions)

## Verification Protocol
- Banks should call the issuing bank's branch directly to verify the statement
- Request Netbanking-generated statements via official portal
- Use SWIFT/NEFT references to verify large transactions
""",
    },
    "compliance": {
        "dpdp_act_provisions.md": """# Digital Personal Data Protection Act 2023 (DPDP Act)

## Overview
The DPDP Act provides a framework for the processing of digital personal data in India, balancing individuals' right to protect their data and the need to process data for lawful purposes.

## Key Definitions
- **Personal Data**: Any data about an identifiable individual
- **Data Fiduciary**: An entity that determines the purpose and means of data processing
- **Data Principal**: The individual to whom the data belongs
- **Consent Manager**: An entity registered with the Data Protection Board to manage consents

## Obligations for Banks (Data Fiduciaries)
- Collect only data necessary for the purpose (data minimisation)
- Obtain explicit consent before processing sensitive personal data
- Retain data only as long as necessary
- Notify the Data Protection Board within 72 hours of a data breach

## Rights of Individuals
- Right to access information
- Right to correction and erasure
- Right to nominate someone to exercise rights in case of death or incapacity
- Right to grievance redressal

## Penalties
- Up to ₹250 crore for each breach of significant obligations
- Up to ₹10,000 for failure to implement data security measures

## Implication for TruthLens
All PII (PAN, Aadhaar, bank account numbers) must be masked in UI for non-privileged roles. Logs must not contain raw PII.
""",
        "pmla_requirements.md": """# PMLA Requirements for Banks

## Overview
The Prevention of Money Laundering Act, 2002 (PMLA) obligates banks and financial institutions to maintain records, verify identity, and report suspicious transactions.

## Obligations
1. **Record Maintenance**: All transactions above ₹10 lakh must be recorded
2. **KYC Compliance**: Full KYC before opening any account or granting loan
3. **Transaction Monitoring**: Continuous monitoring of customer transactions
4. **Reporting to FIU-IND**: Cash Transaction Reports (CTR), Suspicious Transaction Reports (STR)

## Cash Transaction Report (CTR)
- Filed for cash transactions of ₹10 lakh or more in a single day
- Due within 15 days of calendar month end

## Suspicious Transaction Report (STR)
- Filed within 7 days of formation of suspicion
- Includes: nature of transaction, persons involved, value, reason for suspicion
- Recipient: Financial Intelligence Unit — India (FIU-IND)

## Red Flags for Banks
- Multiple cash deposits just below ₹10 lakh (structuring)
- Complex layering of funds through multiple accounts
- Sudden large credits followed by immediate withdrawals
- No business rationale for large international transfers
""",
        "str_filing_guidelines.md": """# Suspicious Transaction Report (STR) Filing Guidelines

## Legal Basis
Section 12 of PMLA, 2002 mandates reporting entities (banks, NBFCs) to file STRs with FIU-IND for any suspicious transactions.

## What Constitutes a Suspicious Transaction?
- Transaction not commensurate with known income/business
- Customer provides false documentation
- Loan proceeds routed back immediately as deposits
- Multiple transactions structured to avoid reporting limits
- Transactions involving politically exposed persons (PEPs) without business rationale

## STR Filing Procedure
1. Branch officer identifies suspicious transaction
2. Branch Manager concurs and escalates to the Principal Officer (PO)
3. PO reviews and files STR with FIU-IND via FINnet portal within 7 days

## Confidentiality
- STR information is strictly confidential
- No disclosure to the suspect or any third party is permitted
- Tipping off is a criminal offence under PMLA

## Penalties for Non-Filing
- Fine of ₹10,000 to ₹1 lakh per instance of non-compliance
""",
        "audit_trail_requirements.md": """# Audit Trail Requirements for Banks

## Regulatory Basis
Banks must maintain comprehensive audit trails under:
- RBI IT Governance Framework
- PMLA, 2002
- Income Tax Act (Section 285BA — SFT reporting)
- IT Act, 2000

## What Must Be Logged?
- All user logins and logouts
- All data access events (who viewed what record, when)
- All modifications to loan data with before and after values
- All document uploads, downloads, and deletions
- System configuration changes
- Failed authentication attempts

## Retention Period
- System logs: Minimum 5 years
- Transaction records: Minimum 10 years
- KYC documents: Life of the account + 5 years after closure

## Immutability
Audit logs must be immutable. Use write-once storage or cryptographically signed log chains. Any attempt to modify audit logs must itself generate an alert.

## TruthLens Compliance
All actions in TruthLens (document access, analysis, report generation) are logged in the `audit_logs` table with user ID, timestamp, IP address, and resource affected.
""",
    }
}

def generate_knowledge_base():
    base_dir = "data/knowledge_base"
    total = 0
    for category, files in KB_DOCS.items():
        cat_dir = os.path.join(base_dir, category)
        os.makedirs(cat_dir, exist_ok=True)
        for filename, content in files.items():
            path = os.path.join(cat_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            total += 1
    print(f"Generated {total} knowledge base documents.")

if __name__ == "__main__":
    generate_knowledge_base()
