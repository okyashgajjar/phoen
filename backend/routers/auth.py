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
    for u in users:
        if u.get("email") == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")
            
    user_id = str(uuid.uuid4())
    user_dict = user_in.dict()
    user_dict["id"] = user_id
    # We store the password as plaintext in the mock, don't do this in prod
    db.insert("users", user_id, user_dict)
    
    return user_dict

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
