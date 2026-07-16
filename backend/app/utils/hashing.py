"""
TruthLens — Hashing Utilities.

Fast hashing using BLAKE3 or xxHash for files and data.
"""

from __future__ import annotations

import hashlib


class Hasher:
    """Hashing utility for files and strings."""

    @staticmethod
    def sha256(data: bytes) -> str:
        """Generate SHA-256 hash."""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def chunked_file_hash(file_path: str) -> str:
        """Generate hash for large files."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
