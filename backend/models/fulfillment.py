from pydantic import BaseModel
from typing import List, Dict

class StockLevel(BaseModel):
    product_id: str
    quantity: int

class Warehouse(BaseModel):
    id: str
    name: str
    location: str
    shipping_cost_weighting: float
    stock: Dict[str, int] # product_id -> quantity

class FulfillmentSplitLine(BaseModel):
    product_id: str
    warehouse_id: str
    quantity: int

class FulfillmentSplit(BaseModel):
    id: str
    quotation_id: str
    splits: List[FulfillmentSplitLine]
    estimated_cost: float
    is_manual_override: bool = False

class BackorderRecord(BaseModel):
    id: str
    quotation_id: str
    product_id: str
    missing_quantity: int
    resolved: bool = False
