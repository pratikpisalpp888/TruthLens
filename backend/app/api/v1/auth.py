"""
TruthLens — Auth API Endpoints.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.dependencies import get_db, get_current_user, require_role
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import AuthenticationException, ValidationException
from app.core.rate_limit import rate_limit_login, rate_limit_user
from app.core.config import settings
from app.db.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, TokenRefresh, UserResponse
from app.services.audit_service import AuditService

router = APIRouter()

@router.post("/register", response_model=UserResponse, dependencies=[Depends(rate_limit_user)])
async def register(
    data: UserRegister,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """Register a new user (Admin only)."""
    # Check if exists
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalars().first():
        raise ValidationException("Email already registered")
        
    new_user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        role=data.role
    )
    db.add(new_user)
    await db.flush()
    
    # Audit log
    audit_svc = AuditService(db)
    await audit_svc.log(
        user_id=current_user.id,
        action="user.created",
        resource_type="user",
        resource_id=new_user.id,
        details={"email": new_user.email, "role": new_user.role}
    )
    
    return UserResponse(
        user_id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        role=new_user.role
    )

@router.post("/login", response_model=TokenResponse)
async def login(
    request: Request,
    data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login and get tokens."""
    await rate_limit_login(data.username)
    
    result = await db.execute(select(User).where(User.email == data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(data.password, user.password_hash):
        raise AuthenticationException("Incorrect email or password")
    if not user.is_active:
        raise AuthenticationException("User is inactive")
        
    user.last_login = datetime.utcnow()
    
    # Audit log
    audit_svc = AuditService(db)
    await audit_svc.log(
        user_id=user.id,
        action="user.login",
        resource_type="user",
        resource_id=user.id,
        ip_address=request.client.host if request.client else None
    )
    
    return TokenResponse(
        access_token=create_access_token(user.id, user.role),
        refresh_token=create_refresh_token(user.id),
        expires_in=settings.JWT_EXPIRY_MINUTES * 60,
        user=UserResponse(
            user_id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            last_login=user.last_login
        )
    )

@router.post("/refresh", response_model=TokenResponse, dependencies=[Depends(rate_limit_user)])
async def refresh_token(
    data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token."""
    try:
        payload = decode_token(data.refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationException("Invalid token type")
        user_id = payload.get("sub")
    except Exception:
        raise AuthenticationException("Invalid refresh token")
        
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    
    if not user or not user.is_active:
        raise AuthenticationException("User not found or inactive")
        
    return TokenResponse(
        access_token=create_access_token(user.id, user.role),
        refresh_token=create_refresh_token(user.id),
        expires_in=settings.JWT_EXPIRY_MINUTES * 60
    )

@router.get("/me", response_model=UserResponse, dependencies=[Depends(rate_limit_user)])
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user details."""
    return UserResponse(
        user_id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        last_login=current_user.last_login
    )
