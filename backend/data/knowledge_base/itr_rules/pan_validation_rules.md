# PAN Validation Rules

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
