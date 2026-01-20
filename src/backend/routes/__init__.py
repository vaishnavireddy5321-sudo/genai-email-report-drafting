"""Routes package for the GenAI Email & Report Drafting System.

This package contains all API route blueprints.
"""

from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.documents import documents_bp
from routes.history import history_bp

__all__ = ["auth_bp", "admin_bp", "documents_bp", "history_bp"]
