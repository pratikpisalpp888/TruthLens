"""
TruthLens — Auth Schemas.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str

class UserResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    role: str
    last_login: Optional[datetime] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Optional[UserResponse] = None

class TokenRefresh(BaseModel):
    refresh_token: str
