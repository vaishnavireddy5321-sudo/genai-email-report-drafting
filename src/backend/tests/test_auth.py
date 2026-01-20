"""Unit tests for authentication endpoints and RBAC.

This module tests user registration, login, JWT validation, and
role-based access control.
"""

import pytest
from app import create_app
from db import db
from models.audit_log import AuditLog
from models.user import User


@pytest.fixture
def app():
    """Create test Flask application."""
    app = create_app("test")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def regular_user(app):
    """Create a regular user for testing."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com", role="USER")
        user.set_password("TestPass123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id  # Get the ID before session closes
    return user_id


@pytest.fixture
def admin_user(app):
    """Create an admin user for testing."""
    with app.app_context():
        user = User(username="adminuser", email="admin@example.com", role="ADMIN")
        user.set_password("AdminPass123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id  # Get the ID before session closes
    return user_id


class TestUserRegistration:
    """Tests for user registration endpoint."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/register", json={"username": "newuser", "email": "newuser@example.com", "password": "NewPass123"}
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["message"] == "User registered successfully"
        assert data["user"]["username"] == "newuser"
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["role"] == "USER"
        assert "access_token" in data
        assert "password_hash" not in data["user"]

    def test_register_missing_fields(self, client):
        """Test registration with missing fields."""
        response = client.post("/api/auth/register", json={"username": "newuser"})

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        response = client.post(
            "/api/auth/register", json={"username": "newuser", "email": "invalid-email", "password": "NewPass123"}
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "email" in data["error"].lower()

    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        response = client.post(
            "/api/auth/register", json={"username": "newuser", "email": "newuser@example.com", "password": "weak"}
        )

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "password" in data["error"].lower()

    def test_register_duplicate_username(self, client, regular_user):
        """Test registration with existing username."""
        response = client.post(
            "/api/auth/register",
            json={"username": "testuser", "email": "different@example.com", "password": "NewPass123"},
        )

        assert response.status_code == 409
        data = response.get_json()
        assert data["error"] == "User already exists"

    def test_register_duplicate_email(self, client, regular_user):
        """Test registration with existing email."""
        response = client.post(
            "/api/auth/register",
            json={"username": "differentuser", "email": "test@example.com", "password": "NewPass123"},
        )

        assert response.status_code == 409
        data = response.get_json()
        assert data["error"] == "User already exists"

    def test_register_creates_audit_log(self, client, app):
        """Test that registration creates an audit log entry."""
        response = client.post(
            "/api/auth/register",
            json={"username": "audituser", "email": "audit@example.com", "password": "AuditPass123"},
        )

        assert response.status_code == 201

        with app.app_context():
            user = User.query.filter_by(username="audituser").first()
            audit_logs = AuditLog.query.filter_by(user_id=user.id, action="user_registered").all()
            assert len(audit_logs) == 1


class TestUserLogin:
    """Tests for user login endpoint."""

    def test_login_success_with_username(self, client, regular_user):
        """Test successful login with username."""
        response = client.post("/api/auth/login", json={"username": "testuser", "password": "TestPass123"})

        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Login successful"
        assert data["user"]["username"] == "testuser"
        assert "access_token" in data

    def test_login_success_with_email(self, client, regular_user):
        """Test successful login with email."""
        response = client.post("/api/auth/login", json={"username": "test@example.com", "password": "TestPass123"})

        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Login successful"
        assert "access_token" in data

    def test_login_invalid_username(self, client):
        """Test login with non-existent username."""
        response = client.post("/api/auth/login", json={"username": "nonexistent", "password": "TestPass123"})

        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data

    def test_login_invalid_password(self, client, regular_user):
        """Test login with incorrect password."""
        response = client.post("/api/auth/login", json={"username": "testuser", "password": "WrongPass123"})

        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data

    def test_login_missing_fields(self, client):
        """Test login with missing fields."""
        response = client.post("/api/auth/login", json={"username": "testuser"})

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_login_creates_audit_log(self, client, regular_user, app):
        """Test that successful login creates an audit log entry."""
        response = client.post("/api/auth/login", json={"username": "testuser", "password": "TestPass123"})

        assert response.status_code == 200

        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            audit_logs = AuditLog.query.filter_by(user_id=user.id, action="login_success").all()
            assert len(audit_logs) >= 1


class TestProtectedEndpoints:
    """Tests for JWT-protected endpoints."""

    def test_get_current_user_success(self, client, regular_user):
        """Test accessing current user info with valid token."""
        # Login to get token
        login_response = client.post("/api/auth/login", json={"username": "testuser", "password": "TestPass123"})
        token = login_response.get_json()["access_token"]

        # Access protected endpoint
        response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        data = response.get_json()
        assert data["user"]["username"] == "testuser"

    def test_get_current_user_missing_token(self, client):
        """Test accessing protected endpoint without token."""
        response = client.get("/api/auth/me")

        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data

    def test_get_current_user_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token."""
        response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid_token_here"})

        assert response.status_code == 422 or response.status_code == 401
        data = response.get_json()
        assert "error" in data or "msg" in data


class TestAdminRBAC:
    """Tests for admin role-based access control."""

    def test_admin_ping_success(self, client, admin_user):
        """Test admin endpoint with admin user."""
        # Login as admin
        login_response = client.post("/api/auth/login", json={"username": "adminuser", "password": "AdminPass123"})
        token = login_response.get_json()["access_token"]

        # Access admin endpoint
        response = client.get("/api/admin/ping", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Admin access verified"
        assert data["user"]["role"] == "ADMIN"

    def test_admin_ping_regular_user_forbidden(self, client, regular_user):
        """Test admin endpoint rejects regular user."""
        # Login as regular user
        login_response = client.post("/api/auth/login", json={"username": "testuser", "password": "TestPass123"})
        token = login_response.get_json()["access_token"]

        # Try to access admin endpoint
        response = client.get("/api/admin/ping", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert "admin" in data["error"].lower()

    def test_admin_ping_missing_token(self, client):
        """Test admin endpoint requires authentication."""
        response = client.get("/api/admin/ping")

        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data


class TestPasswordHashing:
    """Tests for password hashing and verification."""

    def test_password_is_hashed(self, app):
        """Test that passwords are stored as hashes."""
        with app.app_context():
            user = User(username="hashtest", email="hash@example.com", role="USER")
            user.set_password("PlainPass123")
            db.session.add(user)
            db.session.commit()

            # Password hash should not be the plain password
            assert user.password_hash != "PlainPass123"
            # Hash should be long enough to be pbkdf2:sha256
            assert len(user.password_hash) > 50

    def test_password_verification_success(self, app):
        """Test correct password verification."""
        with app.app_context():
            user = User(username="verifytest", email="verify@example.com", role="USER")
            user.set_password("CorrectPass123")
            db.session.add(user)
            db.session.commit()

            assert user.check_password("CorrectPass123") is True

    def test_password_verification_failure(self, app):
        """Test incorrect password verification."""
        with app.app_context():
            user = User(username="failtest", email="fail@example.com", role="USER")
            user.set_password("CorrectPass123")
            db.session.add(user)
            db.session.commit()

            assert user.check_password("WrongPass123") is False
