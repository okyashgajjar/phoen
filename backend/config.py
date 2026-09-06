import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Phoen"
    PROJECT_TITLE: str = "Phoen — Enterprise CPQ & RevOps Platform"
    PROJECT_DESCRIPTION: str = (
        "Enterprise-grade Configure, Price, Quote (CPQ) and self-governing B2B revenue operations engine. "
        "Features multi-ceiling discount governance, automated approval escalation, 4-layer AI upsell engine, "
        "multi-warehouse logistics auto-splitting, milestone/hybrid recurring billing, restricted customer portal, "
        "and ReportLab legal proposal PDF streaming."
    )
    VERSION: str = "2.4.0-enterprise"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkey_for_wireframe_only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    class Config:
        case_sensitive = True

settings = Settings()
