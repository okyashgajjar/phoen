from models.base import db
from models.sales import Quotation
from models.fulfillment import FulfillmentSplitLine
import uuid

def calculate_warehouse_split(quotation_id: str):
    quotation = db.get("quotations", quotation_id)
    if not quotation:
        return None
        
    all_warehouses = db.list("warehouses")
    
    splits = []
    backorders = []
    
    # Very basic auto-split: try to fulfill from the first warehouse that has stock
    # If not enough, split across multiple
    # A real implementation would weight shipping cost (traveling salesman/knapsack)
    
    for line in quotation.get("lines", []):
        if line.get("is_recurring"):
            continue # Don't physically ship recurring subscription lines (usually)
            
        remaining_qty = line.get("qty", line.get("quantity", 0))
        product_id = line.get("product_id")
        if remaining_qty is None:
            remaining_qty = 0
        
        for wh in all_warehouses:
            stock = wh.get("stock", {}).get(product_id, 0)
            if stock > 0:
                qty_to_take = min(stock, remaining_qty)
                splits.append(FulfillmentSplitLine(
                    product_id=product_id,
                    warehouse_id=wh.get("id"),
                    quantity=qty_to_take
                ))
                remaining_qty -= qty_to_take
                
                # Mock update stock temporarily for calculation (real system would reserve)
                # We won't mutate db here to keep calculation idempotent
                
            if remaining_qty == 0:
                break
                
        if remaining_qty > 0:
            # Generate backorder
            backorder = {
                "id": str(uuid.uuid4()),
                "quotation_id": quotation_id,
                "product_id": product_id,
                "missing_quantity": remaining_qty,
                "resolved": False
            }
            db.insert("backorder_records", backorder["id"], backorder)
            
    # Calculate estimated cost (mock)
    estimated_cost = len(splits) * 15.0 # $15 per shipment line mock
    
    split_record = {
        "id": str(uuid.uuid4()),
        "quotation_id": quotation_id,
        "splits": [s.dict() for s in splits],
        "estimated_cost": estimated_cost,
        "is_manual_override": False
    }
    
    db.insert("fulfillment_splits", split_record["id"], split_record)
    return split_record
