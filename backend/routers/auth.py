from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from models.base import db
from models.users import User, UserCreate, Token, RoleEnum
import uuid

router = APIRouter()

class LoginData(BaseModel):
    email: str
    password: str

@router.post("/signup", response_model=User)
def signup(user_in: UserCreate):
    users = db.list("users")
    
    # Check if email is already registered
    for u in users:
        if u.get("email") == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")
            
    # Check if an admin already exists (we only allow 1 unique admin for signup)
    if user_in.role == RoleEnum.admin:
        admin_exists = any(u.get("role") == "admin" for u in users)
        if admin_exists:
            raise HTTPException(status_code=400, detail="An admin account already exists. Please log in.")
    else:
        # For this mockup, direct signup is only for admins. Other roles are created by admin.
        raise HTTPException(status_code=400, detail="Only the initial Admin can be created via signup.")
            
    user_id = str(uuid.uuid4())
    user_dict = user_in.dict()
    user_dict["id"] = user_id
    user_dict["tier"] = "Gold" # default tier
    # We store the password as plaintext in the mock, don't do this in prod
    db.insert("users", user_id, user_dict)
    
    return user_dict

@router.post("/users", response_model=User)
def create_user(user_in: UserCreate, current_user: dict = Depends(get_current_user)):
    # Only Admin can create users (in this simple mockup)
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to create users")
        
    users = db.list("users")
    for u in users:
        if u.get("email") == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")
            
    user_id = str(uuid.uuid4())
    user_dict = user_in.dict()
    user_dict["id"] = user_id
    user_dict["tier"] = "Gold" # default tier for internal or mock
    db.insert("users", user_id, user_dict)
    
    return user_dict

@router.get("/users/all")
def get_all_users(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.list("users")

@router.post("/login", response_model=Token)
def login(login_data: LoginData):
    users = db.list("users")
    user = None
    for u in users:
        if u.get("email") == login_data.email and u.get("password") == login_data.password:
            user = u
            break
            
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
        
    # For mock, we return the user_id as the token
    return {"access_token": user["id"], "token_type": "bearer"}

from dependencies import get_current_user

@router.get("/me", response_model=User)
def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user
