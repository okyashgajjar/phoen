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
    tier: Optional[str] = "Standard"
    status: Optional[str] = "ACTIVE"

class UserCreate(UserBase):
    password: str
    # Required when role is 'customer': scopes the portal login to one customer.
    customer_id: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[RoleEnum] = None
    tier: Optional[str] = None
    status: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: str
    customer_id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[RoleEnum] = None

