from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    sales_rep = "sales_rep"
    manager = "manager"
    finance = "finance"
    customer = "customer"
    admin = "admin"

class UserBase(BaseModel):
    email: str
    role: RoleEnum
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[RoleEnum] = None
