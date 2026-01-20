"""Admin routes with role-based access control.

This module provides admin-only endpoints that require ADMIN role.
"""

from datetime import datetime, timedelta, timezone
from functools import wraps

from db import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from models.audit_log import AuditLog
from models.document import Document
from models.user import User
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from utils.validators import validate_email, validate_password

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def admin_required():
    """Decorator to require admin role for route access.

    This decorator must be used after @jwt_required() decorator.
    It checks the JWT token's role claim to ensure the user is an admin.

    Returns:
        Decorator function that enforces admin role
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            jwt_data = get_jwt()
            user_role = jwt_data.get("role", "USER")

            if user_role != "ADMIN":
                return jsonify({"error": "Admin access required"}), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator


@admin_bp.route("/ping", methods=["GET"])
@jwt_required()
@admin_required()
def admin_ping():
    """Admin-only ping endpoint for verification.

    Requires:
        Valid JWT token with ADMIN role

    Returns:
        JSON response confirming admin access
    """
    try:
        user_id = int(get_jwt_identity())  # Convert from string to int
        user = db.session.get(User, user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "Admin access verified", "user": user.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": f"Admin ping failed: {str(e)}"}), 500


@admin_bp.route("/audit-logs", methods=["GET"])
@jwt_required()
@admin_required()
def get_audit_logs():
    """Get recent audit log entries.

    Query parameters:
        limit (int): Maximum number of entries to return (default: 50, max: 100)
        offset (int): Number of entries to skip for pagination (default: 0)

    Requires:
        Valid JWT token with ADMIN role

    Returns:
        JSON response with audit log entries and total count
    """
    try:
        # Get pagination parameters
        limit = request.args.get("limit", 50, type=int)
        offset = request.args.get("offset", 0, type=int)

        # Enforce safe limits
        limit = min(limit, 100)
        offset = max(offset, 0)

        # Query audit logs ordered by most recent first
        query = AuditLog.query.order_by(AuditLog.created_at.desc())

        # Get total count
        total = query.count()

        # Apply pagination
        audit_logs = query.limit(limit).offset(offset).all()

        # Convert to dict, excluding sensitive data
        logs_data = []
        for log in audit_logs:
            log_dict = log.to_dict()
            # Include only non-sensitive user identifier (username, not email)
            if log.user_id:
                user = db.session.get(User, log.user_id)
                if user:
                    log_dict["username"] = user.username
                else:
                    log_dict["username"] = None
            else:
                log_dict["username"] = None

            logs_data.append(log_dict)

        return jsonify({"audit_logs": logs_data, "total": total, "limit": limit, "offset": offset}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to retrieve audit logs: {str(e)}"}), 500


@admin_bp.route("/summary", methods=["GET"])
@jwt_required()
@admin_required()
def get_summary():
    """Get system activity summary metrics.

    Requires:
        Valid JWT token with ADMIN role

    Returns:
        JSON response with summary metrics:
        - total_users: Total number of registered users
        - total_documents: Total number of generated documents
        - documents_last_24h: Documents generated in the last 24 hours
        - recent_events_count: Number of audit log entries in the last 24 hours
    """
    try:
        # Calculate 24 hours ago timestamp
        twenty_four_hours_ago = datetime.now(timezone.utc) - timedelta(hours=24)

        # Count total users
        total_users = db.session.query(func.count(User.id)).scalar()

        # Count total documents
        total_documents = db.session.query(func.count(Document.id)).scalar()

        # Count documents created in last 24 hours
        documents_last_24h = (
            db.session.query(func.count(Document.id)).filter(Document.created_at >= twenty_four_hours_ago).scalar()
        )

        # Count recent audit events (last 24 hours)
        recent_events_count = (
            db.session.query(func.count(AuditLog.id)).filter(AuditLog.created_at >= twenty_four_hours_ago).scalar()
        )

        return (
            jsonify(
                {
                    "total_users": total_users or 0,
                    "total_documents": total_documents or 0,
                    "documents_last_24h": documents_last_24h or 0,
                    "recent_events_count": recent_events_count or 0,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": f"Failed to retrieve summary: {str(e)}"}), 500


@admin_bp.route("/users", methods=["POST"])
@jwt_required()
@admin_required()
def create_admin_user():
    """Create a new admin user.

    Request JSON:
        username (str): Unique username
        email (str): Valid email address
        password (str): Password (min 8 chars, at least 1 letter and 1 digit)

    Requires:
        Valid JWT token with ADMIN role

    Returns:
        JSON response with user info or error message
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        username = data.get("username", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not username or not email or not password:
            return jsonify({"error": "Username, email, and password are required"}), 400

        if len(username) < 3 or len(username) > 100:
            return jsonify({"error": "Username must be between 3 and 100 characters"}), 400

        if not validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400

        is_valid_password, password_error = validate_password(password)
        if not is_valid_password:
            return jsonify({"error": password_error}), 400

        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({"error": "User already exists"}), 409

        # Create new admin user
        user = User(username=username, email=email, role="ADMIN")
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Audit log
        audit_log = AuditLog(
            user_id=user.id,
            action="admin_user_created",
            details=f"Admin user created: {username}",
        )
        db.session.add(audit_log)
        db.session.commit()

        return jsonify({"message": "Admin user created successfully", "user": user.to_dict()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create admin user: {str(e)}"}), 500
