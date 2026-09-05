# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from config import settings

# Import routers and seed
from routers import auth, products, quotations, approvals, fulfillment, billing, portal, reports
from seed import seed_database
from models.base import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Only seed if the DB is empty (i.e., first run)
    if not db.list("users"):
        seed_database()
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(products.router, prefix=settings.API_V1_STR + "/products", tags=["products"])
app.include_router(quotations.router, prefix=settings.API_V1_STR + "/quotations", tags=["quotations"])
app.include_router(approvals.router, prefix=settings.API_V1_STR + "/approvals", tags=["approvals"])
app.include_router(fulfillment.router, prefix=settings.API_V1_STR + "/fulfillment", tags=["fulfillment"])
app.include_router(billing.router, prefix=settings.API_V1_STR + "/billing", tags=["billing"])
app.include_router(portal.router, prefix=settings.API_V1_STR + "/portal", tags=["portal"])
app.include_router(reports.router, prefix=settings.API_V1_STR + "/reports", tags=["reports"])

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
