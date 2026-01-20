"""Flask application factory for the GenAI Email & Report Drafting System.

This module provides the Flask application instance with database
initialization and JWT authentication.
"""

import logging
import os
from pathlib import Path

from config import get_config
from db import init_db
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint

logger = logging.getLogger(__name__)


def get_rate_limit_key():
    """Get the key for rate limiting.

    For authenticated endpoints, use the user ID from the JWT token.
    For unauthenticated endpoints, use the remote address.
    """
    try:
        # Try to get the JWT identity (only works for authenticated routes)
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()
        if identity:
            return f"user:{identity}"
    except Exception:
        pass

    # Fall back to remote address
    return get_remote_address()


def create_app(config_name: str = None) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_name: Name of configuration to use (development, production, test)

    Returns:
        Configured Flask application instance
    """
    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    config = get_config(config_name)
    app.config.from_object(config)

    # Initialize database
    init_db(app)

    _bootstrap_admin_user(app)

    # Initialize CORS
    cors_origins = [origin.strip() for origin in app.config.get("CORS_ALLOWED_ORIGINS", "").split(",") if origin]
    CORS(
        app,
        resources={r"/api/*": {"origins": cors_origins}, r"/health": {"origins": cors_origins}},
        supports_credentials=True,
    )

    # Initialize JWT
    jwt = JWTManager(app)

    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_rate_limit_key,
        default_limits=[app.config.get("RATELIMIT_DEFAULT")],
        storage_uri=app.config.get("RATELIMIT_STORAGE_URL"),
        strategy=app.config.get("RATELIMIT_STRATEGY"),
        enabled=app.config.get("RATELIMIT_ENABLED"),
    )

    # Make limiter available to blueprints
    app.limiter = limiter

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Handle expired token."""
        return jsonify({"error": "Token has expired", "message": "Please login again"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Handle invalid token."""
        return jsonify({"error": "Invalid token", "message": "Authentication failed"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Handle missing token."""
        return jsonify({"error": "Authorization token missing", "message": "Please provide a valid token"}), 401

    # Rate limit error handler
    @app.errorhandler(429)
    def ratelimit_handler(e):
        """Handle rate limit exceeded."""
        return jsonify({"error": "Rate limit exceeded", "message": "Too many requests. Please try again later."}), 429

    # Import models to ensure they're registered with SQLAlchemy
    with app.app_context():
        import models  # noqa: F401

    # Register blueprints
    from routes import admin_bp, auth_bp, documents_bp, history_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(history_bp)

    # Swagger UI
    swagger_url = "/api/docs"
    openapi_url = "/api/openapi.yaml"
    swagger_bp = get_swaggerui_blueprint(
        swagger_url,
        openapi_url,
        config={
            "app_name": "GenAI Email & Report Drafting System",
        },
    )
    app.register_blueprint(swagger_bp, url_prefix=swagger_url)

    # Apply rate limits to document generation endpoints
    # This is done after blueprint registration to ensure view functions exist
    if limiter.enabled:
        document_limit = app.config.get("RATELIMIT_DOCUMENT_GENERATION")
        # Decorate the view functions with rate limiting
        app.view_functions["documents.generate_email"] = limiter.limit(document_limit)(
            app.view_functions["documents.generate_email"]
        )
        app.view_functions["documents.generate_report"] = limiter.limit(document_limit)(
            app.view_functions["documents.generate_report"]
        )

    # Basic health check route
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "message": "GenAI Email & Report Drafting System - Phase 05"}, 200

    @app.route("/", methods=["GET"])
    def root():
        """Root endpoint with a friendly status message."""
        return {
            "status": "ok",
            "message": "GenAI Email & Report Drafting System API",
            "health": "/health",
            "openapi": "/api/openapi.yaml",
            "swagger": "/api/docs",
        }, 200

    @app.route("/api/openapi.yaml", methods=["GET"])
    def openapi_spec():
        """Serve the OpenAPI specification (YAML)."""
        spec_path = Path(__file__).resolve().parents[2] / "docs" / "api" / "openapi.yaml"
        return send_file(spec_path, mimetype="application/yaml")

    return app


def _bootstrap_admin_user(app: Flask) -> None:
    """Create a one-time admin user if configured and none exists."""
    if not app.config.get("ADMIN_BOOTSTRAP_ENABLED"):
        return

    username = app.config.get("ADMIN_BOOTSTRAP_USERNAME")
    email = app.config.get("ADMIN_BOOTSTRAP_EMAIL")
    password = app.config.get("ADMIN_BOOTSTRAP_PASSWORD")

    if not username or not email or not password:
        logger.warning("Admin bootstrap enabled but credentials are missing.")
        return

    with app.app_context():
        from db import db
        from models.audit_log import AuditLog
        from models.user import User
        from utils.validators import validate_email, validate_password

        if User.query.filter_by(role="ADMIN").first():
            return

        if not validate_email(email):
            logger.warning("Admin bootstrap email is invalid.")
            return

        is_valid_password, _ = validate_password(password)
        if not is_valid_password:
            logger.warning("Admin bootstrap password does not meet requirements.")
            return

        user = User(username=username.strip(), email=email.strip().lower(), role="ADMIN")
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        audit_log = AuditLog(
            user_id=user.id,
            action="admin_bootstrap_created",
            details=f"Bootstrap admin created: {user.username}",
        )
        db.session.add(audit_log)
        db.session.commit()

        logger.info("Bootstrap admin user created.")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
