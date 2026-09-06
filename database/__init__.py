"""
Phoen Database Package.

Provides connection factories, session lifecycle management, and
SQLAlchemy 2.0 relational models for the 16 core ACID tables.
"""

from .config import SessionLocal, engine, get_db
from .models import (
    Base,
    Customer,
    CatalogItem,
    Variant,
    Inventory,
    Warehouse,
    SalesDocument,
    DocumentLine,
    PricingRule,
    ProductRecommendation,
    AuditLog,
    Subscription,
    AppUser,
    WarehouseAllocation,
)

__all__ = [
    # Session management
    "SessionLocal",
    "engine",
    "get_db",
    # Base
    "Base",
    # Core Relational Models
    "Customer",
    "CatalogItem",
    "Variant",
    "Inventory",
    "Warehouse",
    "SalesDocument",
    "DocumentLine",
    "PricingRule",
    "ProductRecommendation",
    "AuditLog",
    "Subscription",
    "AppUser",
    "WarehouseAllocation",
]
