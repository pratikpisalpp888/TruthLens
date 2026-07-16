# Identity Fraud Patterns

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
