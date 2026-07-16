"""
TruthLens — Security Utilities.
"""

from datetime import datetime, timedelta
import hashlib
import uuid
from typing import Any, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings
from app.utils.encryption import AESCipher

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_cipher = AESCipher(settings.ENCRYPTION_KEY)

# ---------------------------------------------------------------------------
# Password Handling
# ---------------------------------------------------------------------------
def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# ---------------------------------------------------------------------------
# JWT Token Management
# ---------------------------------------------------------------------------
def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
    to_encode = {
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "sub": user_id,
        "role": role
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "sub": user_id,
        "type": "refresh"
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        from app.core.exceptions import TokenInvalidError
        raise TokenInvalidError()

# ---------------------------------------------------------------------------
# Encryption wrappers
# ---------------------------------------------------------------------------
def encrypt_file(data: bytes, key: str = None) -> bytes:
    # Use global cipher unless a specific key is passed (not implemented)
    return _cipher.encrypt(data)

def decrypt_file(data: bytes, key: str = None) -> bytes:
    return _cipher.decrypt(data)

def generate_file_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
