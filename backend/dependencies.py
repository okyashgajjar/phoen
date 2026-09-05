from fastapi import Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from models.users import RoleEnum
from models.base import db

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    # Mock JWT decoding: we will just pass the user ID or email as the token for the wireframe
    user = db.get("users", token)
    if not user:
        # Fallback to check if token is email
        users = db.list("users")
        for u in users:
            if u.get("email") == token:
                user = u
                break
                
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
        
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list[RoleEnum]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Security(get_current_user)):
        if user.get("role") not in [r.value for r in self.allowed_roles]:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return user
