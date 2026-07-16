"""
TruthLens — Data Masking Utilities.
"""

import re

def mask_pan(pan: str) -> str:
    """Masks PAN: ABCDE1234F -> ABCXX****F"""
    if not pan or len(pan) < 10:
        return pan
    return f"{pan[:3]}XX****{pan[-1]}"

def mask_aadhaar(aadhaar: str) -> str:
    """Masks Aadhaar: 123456789012 -> XXXX-XXXX-9012"""
    # Remove spaces/hyphens first
    clean = re.sub(r'[\s\-]', '', aadhaar)
    if len(clean) != 12:
        return aadhaar
    return f"XXXX-XXXX-{clean[-4:]}"

def mask_account(account: str) -> str:
    """Masks Account Number: 1234567890 -> XXXXXX7890"""
    if not account or len(account) < 6:
        return account
    return "X" * (len(account) - 4) + account[-4:]

def mask_email(email: str) -> str:
    """Masks Email: user@email.com -> u***@email.com"""
    if not email or "@" not in email:
        return email
    parts = email.split("@")
    name = parts[0]
    domain = parts[1]
    if len(name) <= 1:
        masked_name = name
    else:
        masked_name = name[0] + "***"
    return f"{masked_name}@{domain}"

def apply_masking(data: dict, role: str) -> dict:
    """
    Applies masking to a dictionary recursively.
    Admin sees raw data, Officer sees masked data.
    """
    if role == "admin":
        return data

    if not isinstance(data, dict):
        return data

    result = {}
    for k, v in data.items():
        if isinstance(v, dict):
            result[k] = apply_masking(v, role)
        elif isinstance(v, list):
            result[k] = [apply_masking(item, role) if isinstance(item, dict) else item for item in v]
        elif isinstance(v, str):
            key_lower = k.lower()
            if "pan" in key_lower:
                result[k] = mask_pan(v)
            elif "aadhaar" in key_lower:
                result[k] = mask_aadhaar(v)
            elif "account" in key_lower or "acc_no" in key_lower:
                result[k] = mask_account(v)
            elif "email" in key_lower:
                result[k] = mask_email(v)
            else:
                result[k] = v
        else:
            result[k] = v
    return result
