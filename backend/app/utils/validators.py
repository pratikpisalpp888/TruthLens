"""
TruthLens — Validation Utilities.

Format validators for specific Indian identifiers.
"""

from __future__ import annotations

import re


class Validators:
    """Validation utility for common identifiers."""

    @staticmethod
    def is_valid_pan(pan: str) -> bool:
        """Validate Indian PAN format."""
        return bool(re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", pan.upper()))

    @staticmethod
    def is_valid_aadhaar(aadhaar: str) -> bool:
        """Validate Indian Aadhaar format (12 digits)."""
        clean = aadhaar.replace(" ", "")
        return bool(re.match(r"^\d{12}$", clean))

    @staticmethod
    def is_valid_ifsc(ifsc: str) -> bool:
        """Validate Indian IFSC format."""
        return bool(re.match(r"^[A-Z]{4}0[A-Z0-9]{6}$", ifsc.upper()))
