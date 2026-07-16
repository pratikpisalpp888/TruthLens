"""
TruthLens — In-Memory Rate Limiter.
"""

import time
from fastapi import Request, HTTPException, status
from collections import defaultdict

# Simple in-memory storage: { "key": [timestamps] }
_rate_limits = defaultdict(list)

def check_rate_limit(key: str, limit: int, window: int):
    """
    Checks if a key has exceeded the limit within the window (in seconds).
    """
    current_time = time.time()
    # Clean up old timestamps
    _rate_limits[key] = [t for t in _rate_limits[key] if current_time - t < window]
    
    if len(_rate_limits[key]) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    _rate_limits[key].append(current_time)

async def rate_limit_user(request: Request):
    # 100 requests / minute per user (based on IP for pre-auth, or user ID if auth'd)
    client_ip = request.client.host if request.client else "unknown"
    check_rate_limit(f"user_req:{client_ip}", 100, 60)

async def rate_limit_login(email: str):
    # 10 login attempts / hour per email
    check_rate_limit(f"login:{email}", 10, 3600)
