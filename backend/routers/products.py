from fastapi import APIRouter, Depends, HTTPException
from models.base import db
from models.products import Product, ProductBase
from dependencies import get_current_user, RoleChecker
from models.users import RoleEnum
from typing import List
import uuid

router = APIRouter()

@router.get("/", response_model=List[Product])
def list_products(current_user: dict = Depends(get_current_user)):
    return db.list("products")

@router.post("/", response_model=Product, dependencies=[Depends(RoleChecker([RoleEnum.admin]))])
def create_product(product_in: ProductBase):
    prod_id = str(uuid.uuid4())
    prod_dict = product_in.dict()
    prod_dict["id"] = prod_id
    db.insert("products", prod_id, prod_dict)
    return prod_dict

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str, current_user: dict = Depends(get_current_user)):
    prod = db.get("products", product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod
