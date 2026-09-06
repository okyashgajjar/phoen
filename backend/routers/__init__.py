"""
Phoen API Routers.

Encapsulates all RESTful route controllers for CPQ operations, catalog search,
governance, multi-warehouse fulfillment, billing, and reporting.
"""

from .auth import router as auth_router
from .products import router as products_router
from .catalog_products import router as catalog_products_router
from .quotations import router as quotations_router
from .approvals import router as approvals_router
from .governance import router as governance_router
from .fulfillment import router as fulfillment_router
from .billing import router as billing_router
from .portal import router as portal_router
from .reports import router as reports_router
from .analytics import router as analytics_router

all_routers = [
    (auth_router, "/api/v1/auth", ["auth"]),
    (catalog_products_router, "/api/v1/catalog", ["catalog"]),
    (products_router, "/api/v1/products", ["catalog"]),
    (quotations_router, "/api/v1/quotations", ["quotations"]),
    (approvals_router, "/api/v1/approvals", ["approvals"]),
    (governance_router, "/api/v1/governance", ["governance"]),
    (fulfillment_router, "/api/v1/fulfillment", ["fulfillment"]),
    (billing_router, "/api/v1/billing", ["billing"]),
    (portal_router, "/api/v1/portal", ["portal"]),
    (reports_router, "/api/v1/reports", ["reports"]),
    (analytics_router, "/api/v1/analytics", ["analytics"]),
]

__all__ = [
    "auth_router",
    "products_router",
    "catalog_products_router",
    "quotations_router",
    "approvals_router",
    "governance_router",
    "fulfillment_router",
    "billing_router",
    "portal_router",
    "reports_router",
    "analytics_router",
    "all_routers",
]
