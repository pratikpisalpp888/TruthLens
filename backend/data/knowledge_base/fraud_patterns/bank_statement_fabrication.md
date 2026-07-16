# Bank Statement Fabrication

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
