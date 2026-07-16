# Audit Trail Requirements for Banks

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
