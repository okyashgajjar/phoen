"""
Phoen Domain Models & Pydantic Validation Schemas.

Consolidates RBAC user models, quotation schemas, catalog definitions,
and state enums into an accessible package boundary.
"""

from .users import (
    RoleEnum,
    User,
    UserBase,
    UserCreate,
    UserUpdate,
    Token,
    TokenData,
)
from .sales import (
    QuotationStatus,
    STATUS_LABELS,
    QuotationLineIn,
)
from .products import (
    Product,
    ProductBase,
    Variant,
    PriceList,
    DiscountTier,
    CategoryDiscountCeiling,
)
from .base import db, DealFlowDatabase

__all__ = [
    # User & RBAC
    "RoleEnum",
    "User",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "Token",
    "TokenData",
    # Sales & Quotations
    "QuotationStatus",
    "STATUS_LABELS",
    "QuotationLineIn",
    # Products & Pricing
    "Product",
    "ProductBase",
    "Variant",
    "PriceList",
    "DiscountTier",
    "CategoryDiscountCeiling",
    # In-memory database interface
    "db",
    "DealFlowDatabase",
]
