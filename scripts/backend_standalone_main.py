from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
import os
import sys

# Ensure parent directory is in path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.config import SessionLocal, engine
from database import models

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DealFlow360 API",
    description="Enterprise API for the Intelligent, Self-Governing Sales Operations Platform",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/health")
def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "DealFlow360 API"}

@app.get("/api/products")
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all master products with their associated brand."""
    products = db.query(models.Product).offset(skip).limit(limit).all()
    
    result = []
    for p in products:
        brand_name = db.query(models.Brand).filter(models.Brand.id == p.brand_id).first()
        brand_name = brand_name.name if brand_name else None
        
        result.append({
            "id": p.id,
            "code": p.code,
            "name": p.name,
            "product_type": p.product_type,
            "brand": brand_name,
            "base_price": p.base_price
        })
    return {"total": db.query(models.Product).count(), "data": result}

@app.get("/api/inventory/{sku}")
def get_inventory(sku: str, db: Session = Depends(get_db)):
    """Retrieve multi-warehouse inventory allocation for a specific SKU."""
    variant = db.query(models.ProductVariant).filter(models.ProductVariant.sku == sku).first()
    if not variant:
        raise HTTPException(status_code=404, detail="SKU not found")
        
    inventory_records = db.query(models.Inventory).filter(models.Inventory.variant_id == variant.id).all()
    
    allocations = []
    total_stock = 0
    total_allocated = 0
    
    for inv in inventory_records:
        warehouse = db.query(models.Warehouse).filter(models.Warehouse.id == inv.warehouse_id).first()
        allocations.append({
            "warehouse": warehouse.name if warehouse else inv.warehouse_id,
            "quantity_on_hand": inv.quantity_on_hand,
            "quantity_allocated": inv.quantity_allocated,
            "quantity_available": inv.quantity_available,
            "reorder_level": inv.reorder_level
        })
        total_stock += inv.quantity_on_hand
        total_allocated += inv.quantity_allocated
        
    return {
        "sku": variant.sku,
        "name": variant.name,
        "total_stock": total_stock,
        "total_allocated": total_allocated,
        "total_available": total_stock - total_allocated,
        "allocations": allocations
    }

@app.get("/api/deal_health")
def get_deal_health(limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve the top most at-risk or healthy deals based on anomaly detection logic."""
    health_records = db.query(models.DealHealth).order_by(models.DealHealth.risk_score.desc()).limit(limit).all()
    
    return [
        {
            "quotation_id": dh.quotation_id,
            "health_status": dh.health_status,
            "risk_score": dh.risk_score,
            "flags": dh.flags,
            "recommended_actions": dh.recommended_actions,
            "last_evaluated": dh.last_evaluated_at
        } for dh in health_records
    ]

@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Retrieve high-level business intelligence statistics across all cities."""
    total_customers = db.query(models.Customer).count()
    total_inventory_value = db.query(func.sum(models.Inventory.quantity_on_hand * models.ProductVariant.cost_price))\
                              .join(models.ProductVariant, models.Inventory.variant_id == models.ProductVariant.id)\
                              .scalar()
                              
    total_quotations = db.query(models.Quotation).count()
    total_orders = db.query(models.Order).count()
    
    return {
        "total_customers": total_customers,
        "total_inventory_value_inr": total_inventory_value or 0,
        "total_quotations": total_quotations,
        "total_orders": total_orders
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
