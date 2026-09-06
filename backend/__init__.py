"""
Phoen Enterprise CPQ & RevOps Platform.

A high-performance B2B Configure, Price, Quote (CPQ) and Revenue Operations
engine featuring 16 relational ACID tables, dual-ceiling discount governance,
4-layer AI co-purchase intelligence, and multi-warehouse split logistics.
"""

import sys
import os

# Ensure backend directory is in sys.path when imported as a package
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

try:
    from backend.config import settings
except ImportError:
    from config import settings

__title__ = getattr(settings, "PROJECT_TITLE", "Phoen Enterprise CPQ")
__version__ = getattr(settings, "VERSION", "2.4.0-enterprise")
__author__ = "Phoen Engineering Team"

__all__ = [
    "settings",
    "__title__",
    "__version__",
    "__author__",
]
