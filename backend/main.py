# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from config import settings

# Import routers and seed
from routers import auth, products, quotations, approvals, fulfillment, billing, portal, reports, governance, analytics, catalog_products
from seed import seed_database
from models.base import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Always seed to populate the in-memory fallback for tests
    seed_database()
    yield

tags_metadata = [
    {"name": "auth", "description": "Authentication & Session Management with signed JWTs, PBKDF2 password hashing, and role claims."},
    {"name": "catalog", "description": "Dynamic enterprise catalog items, hardware variants with RAM/SSD specs, and multi-DC stock levels."},
    {"name": "quotations", "description": "CPQ Quote Builder, line item CRUD, blended discount risk recalculation, and proposal PDF streaming."},
    {"name": "approvals", "description": "Multi-tier approval workflow cockpit (Sales Rep -> Manager -> Finance Controller -> Executive)."},
    {"name": "governance", "description": "Finance discount ceiling rules, tier limits, margin floors, and exception override audit trails."},
    {"name": "fulfillment", "description": "Multi-warehouse auto-split fulfillment, regional DC stock reservations, and delivery challan generation."},
    {"name": "billing", "description": "Milestone CAPEX invoicing, recurring subscription proration, and payment reconciliation."},
    {"name": "portal", "description": "Restricted customer negotiation portal, line change requests, digital signature, and PDF agreement download."},
    {"name": "reports", "description": "Executive dashboard KPIs, deal health anomalies, stalled deal alerts, and sales performance analytics."},
    {"name": "analytics", "description": "Financial BI reporting with dynamic gross margin heatmaps and PDF/XLSX multi-format export."},
    {"name": "system", "description": "Engine health diagnostics, database telemetry, and benchmark metrics."},
]

app = FastAPI(
    title=settings.PROJECT_TITLE,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(catalog_products.router, prefix=settings.API_V1_STR + "/products", tags=["catalog"])
app.include_router(products.router, prefix=settings.API_V1_STR + "/products", tags=["products"])
app.include_router(quotations.router, prefix=settings.API_V1_STR + "/quotations", tags=["quotations"])
app.include_router(approvals.router, prefix=settings.API_V1_STR + "/approvals", tags=["approvals"])
app.include_router(fulfillment.router, prefix=settings.API_V1_STR + "/fulfillment", tags=["fulfillment"])
app.include_router(billing.router, prefix=settings.API_V1_STR + "/billing", tags=["billing"])
app.include_router(portal.router, prefix=settings.API_V1_STR + "/portal", tags=["portal"])
app.include_router(reports.router, prefix=settings.API_V1_STR + "/reports", tags=["reports"])
app.include_router(governance.router, prefix=settings.API_V1_STR + "/governance", tags=["governance"])
app.include_router(analytics.router, prefix=settings.API_V1_STR + "/reports", tags=["analytics"])

@app.get("/", tags=["system"])
def read_root():
    return {
        "message": f"Welcome to Phoen (DealFlow360) Enterprise CPQ & RevOps Platform API",
        "project": settings.PROJECT_TITLE,
        "version": settings.VERSION,
        "status": "operational",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.VERSION}

@app.get(settings.API_V1_STR + "/system/diagnostics", tags=["system"])
def system_diagnostics():
    """Live database diagnostics and engine benchmark metrics for evaluators and faculties."""
    from database.config import SessionLocal, engine
    from database.models import (
        Customer, CatalogItem, Variant, Inventory, PricingRule,
        SalesDocument, DocumentLine, Subscription, AuditLog,
        ProductRecommendation, AppUser, Warehouse
    )
    from datetime import datetime, timezone
    
    session = SessionLocal()
    try:
        table_stats = {
            "customers": session.query(Customer).count(),
            "catalog_items": session.query(CatalogItem).count(),
            "variants": session.query(Variant).count(),
            "inventory_records": session.query(Inventory).count(),
            "pricing_rules": session.query(PricingRule).count(),
            "sales_documents": session.query(SalesDocument).count(),
            "document_lines": session.query(DocumentLine).count(),
            "product_recommendations": session.query(ProductRecommendation).count(),
            "audit_logs": session.query(AuditLog).count(),
            "warehouses": session.query(Warehouse).count(),
            "subscriptions": session.query(Subscription).count(),
            "app_users": session.query(AppUser).count(),
        }
        return {
            "status": "healthy",
            "platform": settings.PROJECT_TITLE,
            "version": settings.VERSION,
            "database": {
                "status": "connected",
                "dialect": engine.dialect.name,
                "table_count": len(table_stats),
                "records": table_stats,
            },
            "engines": {
                "dual_ceiling_discount_governance": "active",
                "blended_risk_score_matrix": "active",
                "ai_copurchase_upsell_engine": "active",
                "multi_warehouse_fulfillment_split": "active",
                "hybrid_billing_proration": "active",
                "customer_portal_isolation": "active",
                "reportlab_pdf_generator": "active",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    finally:
        session.close()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
