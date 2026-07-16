"""
TruthLens — FastAPI Dependencies.
"""

from typing import List
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import AuthenticationException, AuthorizationException
from app.db.session import get_db
from app.core.security import decode_token
from app.db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthenticationException("Invalid token payload")
    except Exception:
        raise AuthenticationException("Invalid authentication credentials")
        
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    
    if not user:
        raise AuthenticationException("User not found")
        
    if not user.is_active:
        raise AuthenticationException("User is inactive")
        
    return user

def require_role(allowed_roles: List[str]):
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise AuthorizationException("You do not have permission to perform this action.")
        return current_user
    return role_checker
