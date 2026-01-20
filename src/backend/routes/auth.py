"""Authentication routes for user registration and login.

This module provides endpoints for user authentication including
registration, login, and user profile retrieval.
"""

from db import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.audit_log import AuditLog
from models.user import User
from sqlalchemy.exc import IntegrityError
from utils.validators import validate_email, validate_password

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user.

    Request JSON:
        username (str): Unique username
        email (str): Valid email address
        password (str): Password (min 8 chars, at least 1 letter and 1 digit)

    Returns:
        JSON response with user info and access token or error message
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        username = data.get("username", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        # Validate inputs
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
            # Use generic message to prevent user enumeration (OWASP best practice)
            return jsonify({"error": "User already exists"}), 409

        # Create new user
        user = User(username=username, email=email, role="USER")
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Create audit log
        audit_log = AuditLog(user_id=user.id, action="user_registered", details=f"New user registered: {username}")
        db.session.add(audit_log)
        db.session.commit()

        # Generate JWT token
        access_token = create_access_token(
            identity=str(user.id), additional_claims={"role": user.role}  # Convert to string for JWT
        )

        return (
            jsonify({"message": "User registered successfully", "user": user.to_dict(), "access_token": access_token}),
            201,
        )

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT token.

    Request JSON:
        username (str): Username or email
        password (str): User password

    Returns:
        JSON response with user info and access token or error message
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        username_or_email = data.get("username", "").strip()
        password = data.get("password", "")

        if not username_or_email or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email.lower())
        ).first()

        if not user or not user.check_password(password):
            # Create audit log for failed login attempt
            if user:
                audit_log = AuditLog(
                    user_id=user.id, action="login_failed", details=f"Failed login attempt for user: {user.username}"
                )
                db.session.add(audit_log)
                db.session.commit()

            return jsonify({"error": "Invalid username or password"}), 401

        # Create audit log for successful login
        audit_log = AuditLog(user_id=user.id, action="login_success", details=f"User logged in: {user.username}")
        db.session.add(audit_log)
        db.session.commit()

        # Generate JWT token
        access_token = create_access_token(
            identity=str(user.id), additional_claims={"role": user.role}  # Convert to string for JWT
        )

        return jsonify({"message": "Login successful", "user": user.to_dict(), "access_token": access_token}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Login failed: {str(e)}"}), 500


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Get current authenticated user information.

    Requires:
        Valid JWT token in Authorization header

    Returns:
        JSON response with current user information
    """
    try:
        user_id = int(get_jwt_identity())  # Convert from string to int
        user = db.session.get(User, user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"user": user.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to retrieve user: {str(e)}"}), 500
