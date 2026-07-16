"""
TruthLens — ITR Rule Validation Engine.
Validates ITR (Income Tax Return) specific fields.
"""

import re
from typing import Dict, List, Any

def validate_itr_data(extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Validates ITR fields (ACK number, PAN format, etc).
    Returns a list of anomalies/findings.
    """
    findings = []
    
    # 1. Check Acknowledgement Number
    ack_num = extracted_data.get("ack_number", "")
    if ack_num:
        ack_str = str(ack_num).strip().replace(" ", "")
        if len(ack_str) != 15:
            findings.append({
                "field": "ack_number",
                "value": ack_num,
                "reason": f"Invalid Acknowledgement Number length ({len(ack_str)}). Must be exactly 15 digits.",
                "severity": "high",
                "label": "Invalid ACK length"
            })
        elif not ack_str.isdigit():
            findings.append({
                "field": "ack_number",
                "value": ack_num,
                "reason": "Acknowledgement Number contains non-numeric characters.",
                "severity": "high",
                "label": "Invalid ACK format"
            })

    # 2. Check PAN Format
    pan = extracted_data.get("pan_number", "")
    if pan:
        pan_str = str(pan).strip().upper()
        # Format: 5 letters, 4 digits, 1 letter
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_str):
            findings.append({
                "field": "pan_number",
                "value": pan,
                "reason": "Invalid PAN format. Must be 5 letters, 4 digits, 1 letter.",
                "severity": "high",
                "label": "Invalid PAN format"
            })
        else:
            # 4th character must be P, C, H, A, B, G, J, L, F, T (usually P for person)
            status_char = pan_str[3]
            if status_char not in ['P', 'C', 'H', 'A', 'B', 'G', 'J', 'L', 'F', 'T']:
                findings.append({
                    "field": "pan_number",
                    "value": pan,
                    "reason": f"Invalid PAN status character '{status_char}' at 4th position.",
                    "severity": "medium",
                    "label": "Suspicious PAN structure"
                })

            # 5th character must match the first letter of the surname (we just check if it's a letter)
            # A common mismatch check if we have the applicant name
            applicant_name = extracted_data.get("applicant_name", "")
            if applicant_name:
                surname = applicant_name.split()[-1].upper()
                if pan_str[4] != surname[0]:
                    findings.append({
                        "field": "pan_number",
                        "value": pan,
                        "reason": f"PAN 5th character '{pan_str[4]}' does not match applicant surname '{surname}'.",
                        "severity": "high",
                        "label": "PAN Name Mismatch"
                    })

    # 3. Assessment Year Check
    ay = extracted_data.get("assessment_year", "")
    if ay:
        if not re.match(r'^20[0-9]{2}-[0-9]{2}$', str(ay).strip()):
            findings.append({
                "field": "assessment_year",
                "value": ay,
                "reason": "Invalid Assessment Year format. Expected YYYY-YY (e.g., 2023-24).",
                "severity": "medium",
                "label": "Invalid AY Format"
            })

    # 4. Total Income Check (sanity check)
    income_str = str(extracted_data.get("total_income", "0")).replace(",", "").replace("₹", "").strip()
    try:
        income = float(income_str)
        if income == 0 and extracted_data.get("itr_type", "") in ["ITR-1", "ITR-2"]:
            findings.append({
                "field": "total_income",
                "value": income_str,
                "reason": "Total Income is 0 for a salaried/individual ITR.",
                "severity": "high",
                "label": "Zero Income Suspicion"
            })
    except ValueError:
        pass

    return findings
