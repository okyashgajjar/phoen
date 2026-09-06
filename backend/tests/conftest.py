import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from models.base import db

@pytest.fixture(autouse=True)
def reset_and_seed_db():
    """Reset DB and seed with demo data before each test."""
    # Clear all collections
    for attr in dir(db):
        val = getattr(db, attr)
        if isinstance(val, dict) and not attr.startswith('_'):
            val.clear()

    # Seed with demo data
    from seed import seed_database
    seed_database()
    yield
