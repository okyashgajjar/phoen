"""
Request authentication and role gating.

Previously the bearer token was the user's own id or email, so anyone who knew
an email address could act as that user, and there was no expiry or revocation.
Tokens are now signed JWTs and the user is loaded from the database on every
request, so disabling an account takes effect immediately.
"""

import os
import sys

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database.config import SessionLocal
from database.models import AppUser
from models.users import RoleEnum
from services.security import decode_access_token, TokenError

security = HTTPBearer(auto_error=True)
optional_security = HTTPBearer(auto_error=False)

UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


def _serialise(user: AppUser) -> dict:
    """Shape an AppUser for the rest of the app. Never includes the hash."""
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
        "tier": user.tier or "Standard",
        "status": user.status or "ACTIVE",
        "customer_id": user.customer_id,
    }


def load_user(user_id: str) -> dict | None:
    session = SessionLocal()
    try:
        user = session.query(AppUser).filter(AppUser.id == user_id).first()
        return _serialise(user) if user is not None else None
    finally:
        session.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> dict:
    try:
        claims = decode_access_token(credentials.credentials)
    except TokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        )

    subject = claims.get("sub")
    if not subject:
        raise UNAUTHORIZED

    user = load_user(subject)
    if user is None:
        # The account was deleted after the token was issued.
        raise UNAUTHORIZED

    if (user.get("status") or "ACTIVE").upper() != "ACTIVE":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is disabled")

    # The role is read from the database, not from the token, so a role change
    # or a revocation takes effect on the next request rather than at expiry.
    return user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Security(optional_security),
) -> dict | None:
    """Non-blocking auth dependency: returns user dict if valid token supplied, else None."""
    if not credentials or not credentials.credentials:
        return None
    try:
        claims = decode_access_token(credentials.credentials)
    except TokenError:
        return None

    subject = claims.get("sub")
    if not subject:
        return None

    user = load_user(subject)
    if user is None:
        return None

    if (user.get("status") or "ACTIVE").upper() != "ACTIVE":
        return None

    return user


class RoleChecker:
    """Dependency that allows only the listed roles."""

    def __init__(self, allowed_roles: list[RoleEnum]):
        self.allowed_roles = [
            r.value if isinstance(r, RoleEnum) else str(r) for r in allowed_roles
        ]

    def __call__(self, user: dict = Depends(get_current_user)) -> dict:
        if user.get("role") not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this role",
            )
        return user


def get_portal_user(user: dict = Depends(get_current_user)) -> dict:
    """
    Customer portal gate.

    A portal account must be role 'customer' AND carry the customer_id it is
    scoped to. That id is what the portal endpoints filter every document by,
    which is what makes the portal a genuinely restricted view rather than an
    internal screen with a different label.
    """
    if user.get("role") != "customer":
        raise HTTPException(status_code=403, detail="Customer portal access only")
    if not user.get("customer_id"):
        raise HTTPException(
            status_code=403,
            detail="Portal account is not linked to a customer record",
        )
    return user
