from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    category: str
    base_price: float
    unit: str
    tax_percent: float
    description: Optional[str] = None
    is_recurring: bool = False # Useful to link to subscription plans

class Product(ProductBase):
    id: str

class Variant(BaseModel):
    id: str
    product_id: str
    attribute: str # e.g., Size, Pack
    value: str
    price_delta: float

class PriceList(BaseModel):
    id: str
    customer_tier: str
    currency: str
    product_overrides: dict # product_id -> price

class DiscountTier(BaseModel):
    id: str
    customer_tier: str
    max_discount_percent: float

class CategoryDiscountCeiling(BaseModel):
    id: str
    category: str
    max_discount_percent: float
