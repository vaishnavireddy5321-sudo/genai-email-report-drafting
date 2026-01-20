"""Unit tests for admin endpoints and RBAC enforcement.

This module tests admin-only endpoints to ensure proper role-based
access control and functionality.
"""

from datetime import datetime, timedelta, timezone

import pytest
from app import create_app
from db import db
from models.audit_log import AuditLog
from models.document import Document
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
        user_id = user.id
    return user_id


@pytest.fixture
def admin_user(app):
    """Create an admin user for testing."""
    with app.app_context():
        user = User(username="adminuser", email="admin@example.com", role="ADMIN")
        user.set_password("AdminPass123")
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    return user_id


@pytest.fixture
def regular_user_token(client, regular_user):
    """Get JWT token for regular user."""
    response = client.post("/api/auth/login", json={"username": "testuser", "password": "TestPass123"})
    data = response.get_json()
    return data["access_token"]


@pytest.fixture
def admin_user_token(client, admin_user):
    """Get JWT token for admin user."""
    response = client.post("/api/auth/login", json={"username": "adminuser", "password": "AdminPass123"})
    data = response.get_json()
    return data["access_token"]


@pytest.fixture
def sample_documents(app, regular_user, admin_user):
    """Create sample documents for testing."""
    with app.app_context():
        # Create documents with different timestamps
        now = datetime.now(timezone.utc)

        # Recent document (within 24h)
        doc1 = Document(
            user_id=regular_user,
            doc_type="email",
            title="Test Email",
            content="Test content",
            tone="professional",
            created_at=now,
        )

        # Older document (more than 24h ago)
        doc2 = Document(
            user_id=admin_user,
            doc_type="report",
            title="Test Report",
            content="Test report content",
            tone="formal",
            structure="executive_summary",
            created_at=now - timedelta(hours=30),
        )

        db.session.add(doc1)
        db.session.add(doc2)
        db.session.commit()


@pytest.fixture
def sample_audit_logs(app, regular_user, admin_user):
    """Create sample audit logs for testing."""
    with app.app_context():
        now = datetime.now(timezone.utc)

        # Recent audit log (within 24h)
        log1 = AuditLog(
            user_id=regular_user,
            action="generate_email",
            entity_type="document",
            entity_id=1,
            details="Generated email document",
            created_at=now,
        )

        # Older audit log (more than 24h ago)
        log2 = AuditLog(
            user_id=admin_user, action="login_success", details="Admin logged in", created_at=now - timedelta(hours=30)
        )

        db.session.add(log1)
        db.session.add(log2)
        db.session.commit()


class TestAdminPing:
    """Tests for admin ping endpoint."""

    def test_admin_ping_success(self, client, admin_user_token):
        """Test admin can access ping endpoint."""
        response = client.get("/api/admin/ping", headers={"Authorization": f"Bearer {admin_user_token}"})

        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Admin access verified"
        assert "user" in data

    def test_admin_ping_forbidden_for_regular_user(self, client, regular_user_token):
        """Test regular user cannot access admin ping endpoint."""
        response = client.get("/api/admin/ping", headers={"Authorization": f"Bearer {regular_user_token}"})

        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert "Admin access required" in data["error"]

    def test_admin_ping_unauthorized_without_token(self, client):
        """Test ping endpoint requires authentication."""
        response = client.get("/api/admin/ping")

        assert response.status_code == 401


class TestAdminAuditLogs:
    """Tests for admin audit logs endpoint."""

    def test_get_audit_logs_success(self, client, admin_user_token, sample_audit_logs):
        """Test admin can retrieve audit logs."""
        response = client.get("/api/admin/audit-logs", headers={"Authorization": f"Bearer {admin_user_token}"})

        assert response.status_code == 200
        data = response.get_json()
        assert "audit_logs" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert len(data["audit_logs"]) > 0

        # Verify audit log structure
        log = data["audit_logs"][0]
        assert "id" in log
        assert "action" in log
        assert "created_at" in log
        assert "username" in log
        # Should not expose sensitive data like password_hash
        assert "password_hash" not in str(log)

    def test_get_audit_logs_pagination(self, client, admin_user_token, sample_audit_logs):
        """Test audit logs pagination."""
        response = client.get(
            "/api/admin/audit-logs?limit=1&offset=0", headers={"Authorization": f"Bearer {admin_user_token}"}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["limit"] == 1
        assert data["offset"] == 0
        assert len(data["audit_logs"]) <= 1

    def test_get_audit_logs_forbidden_for_regular_user(self, client, regular_user_token):
        """Test regular user cannot access audit logs."""
        response = client.get("/api/admin/audit-logs", headers={"Authorization": f"Bearer {regular_user_token}"})

        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert "Admin access required" in data["error"]

    def test_get_audit_logs_unauthorized_without_token(self, client):
        """Test audit logs endpoint requires authentication."""
        response = client.get("/api/admin/audit-logs")

        assert response.status_code == 401


class TestAdminSummary:
    """Tests for admin summary endpoint."""

    def test_get_summary_success(self, client, admin_user_token, sample_documents, sample_audit_logs):
        """Test admin can retrieve system summary."""
        response = client.get("/api/admin/summary", headers={"Authorization": f"Bearer {admin_user_token}"})

        assert response.status_code == 200
        data = response.get_json()

        # Verify all expected metrics are present
        assert "total_users" in data
        assert "total_documents" in data
        assert "documents_last_24h" in data
        assert "recent_events_count" in data

        # Verify metrics are numbers
        assert isinstance(data["total_users"], int)
        assert isinstance(data["total_documents"], int)
        assert isinstance(data["documents_last_24h"], int)
        assert isinstance(data["recent_events_count"], int)

        # With fixtures, we should have at least 2 users (regular + admin)
        assert data["total_users"] >= 2

        # Should have 2 documents total
        assert data["total_documents"] == 2

        # Should have 1 document in last 24h
        assert data["documents_last_24h"] == 1

    def test_get_summary_forbidden_for_regular_user(self, client, regular_user_token):
        """Test regular user cannot access summary."""
        response = client.get("/api/admin/summary", headers={"Authorization": f"Bearer {regular_user_token}"})

        assert response.status_code == 403
        data = response.get_json()
        assert "error" in data
        assert "Admin access required" in data["error"]

    def test_get_summary_unauthorized_without_token(self, client):
        """Test summary endpoint requires authentication."""
        response = client.get("/api/admin/summary")

        assert response.status_code == 401

    def test_get_summary_with_no_data(self, client, admin_user_token):
        """Test summary returns zeros when no data exists."""
        response = client.get("/api/admin/summary", headers={"Authorization": f"Bearer {admin_user_token}"})

        assert response.status_code == 200
        data = response.get_json()

        # Should return 0 for documents (admin user fixture exists)
        assert data["total_documents"] == 0
        assert data["documents_last_24h"] == 0
