"""Unit tests for document history endpoints.

This module tests document history retrieval with proper user-scoping
to prevent cross-user data leakage.
"""

from datetime import datetime, timedelta, timezone

import pytest
from app import create_app
from db import db
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
def test_users(app):
    """Create two test users and return their tokens."""
    with app.app_context():
        # User 1
        user1 = User(username="testuser1", email="test1@example.com", role="USER")
        user1.set_password("TestPass123")
        db.session.add(user1)

        # User 2
        user2 = User(username="testuser2", email="test2@example.com", role="USER")
        user2.set_password("TestPass123")
        db.session.add(user2)

        db.session.commit()
        user1_id = user1.id
        user2_id = user2.id

    # Create tokens
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token1 = create_access_token(identity=str(user1_id), additional_claims={"role": "USER"})
        token2 = create_access_token(identity=str(user2_id), additional_claims={"role": "USER"})

    return {"user1": {"token": token1, "user_id": user1_id}, "user2": {"token": token2, "user_id": user2_id}}


@pytest.fixture
def sample_documents(app, test_users):
    """Create sample documents for testing."""
    with app.app_context():
        user1_id = test_users["user1"]["user_id"]
        user2_id = test_users["user2"]["user_id"]

        # User 1 documents
        doc1 = Document(
            user_id=user1_id,
            doc_type="email",
            title="Email 1",
            content="Content of email 1",
            tone="professional",
            created_at=datetime.now(timezone.utc) - timedelta(hours=3),
        )
        doc2 = Document(
            user_id=user1_id,
            doc_type="report",
            title="Report 1",
            content="Content of report 1",
            tone="formal",
            structure="detailed",
            created_at=datetime.now(timezone.utc) - timedelta(hours=2),
        )
        doc3 = Document(
            user_id=user1_id,
            doc_type="email",
            title="Email 2",
            content="Content of email 2",
            tone="casual",
            created_at=datetime.now(timezone.utc) - timedelta(hours=1),
        )

        # User 2 documents (to test isolation)
        doc4 = Document(
            user_id=user2_id,
            doc_type="email",
            title="User2 Email",
            content="Content of user2 email",
            tone="professional",
        )

        db.session.add_all([doc1, doc2, doc3, doc4])
        db.session.commit()

        return {"user1_docs": [doc1.id, doc2.id, doc3.id], "user2_docs": [doc4.id]}


class TestHistoryEndpoint:
    """Tests for document history endpoint."""

    def test_get_history_requires_auth(self, client):
        """Test that history endpoint requires authentication."""
        response = client.get("/api/history")
        assert response.status_code == 401

    def test_get_history_returns_user_documents_only(self, client, test_users, sample_documents, app):
        """Test that users only see their own documents."""
        # User 1 requests history
        response = client.get("/api/history", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'})

        assert response.status_code == 200
        data = response.get_json()
        assert "documents" in data
        assert len(data["documents"]) == 3  # User 1 has 3 documents

        # Verify all returned documents belong to user 1
        for doc in data["documents"]:
            assert doc["id"] in sample_documents["user1_docs"]
            assert doc["id"] not in sample_documents["user2_docs"]

        # User 2 requests history
        response = client.get("/api/history", headers={"Authorization": f'Bearer {test_users["user2"]["token"]}'})

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["documents"]) == 1  # User 2 has 1 document
        assert data["documents"][0]["id"] in sample_documents["user2_docs"]

    def test_get_history_ordered_by_recent_first(self, client, test_users, sample_documents):
        """Test that documents are ordered by most recent first."""
        response = client.get("/api/history", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'})

        assert response.status_code == 200
        data = response.get_json()
        documents = data["documents"]

        # Verify documents are in descending order by created_at
        for i in range(len(documents) - 1):
            current_time = datetime.fromisoformat(documents[i]["created_at"])
            next_time = datetime.fromisoformat(documents[i + 1]["created_at"])
            assert current_time >= next_time

    def test_get_history_with_pagination(self, client, test_users, sample_documents):
        """Test history pagination."""
        # Get first 2 documents
        response = client.get(
            "/api/history?limit=2&offset=0", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["documents"]) == 2
        assert data["total"] == 3
        assert data["limit"] == 2
        assert data["offset"] == 0
        assert data["has_more"] is True

        # Get next document
        response = client.get(
            "/api/history?limit=2&offset=2", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["documents"]) == 1
        assert data["has_more"] is False

    def test_get_history_filter_by_type(self, client, test_users, sample_documents):
        """Test filtering history by document type."""
        # Filter for emails only
        response = client.get(
            "/api/history?doc_type=email", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["total"] == 2  # User 1 has 2 emails

        for doc in data["documents"]:
            assert doc["doc_type"] == "email"

        # Filter for reports only
        response = client.get(
            "/api/history?doc_type=report", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["total"] == 1  # User 1 has 1 report
        assert data["documents"][0]["doc_type"] == "report"

    def test_get_history_invalid_limit(self, client, test_users):
        """Test validation of limit parameter."""
        # Limit too high
        response = client.get(
            "/api/history?limit=101", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'}
        )
        assert response.status_code == 400

        # Limit too low
        response = client.get(
            "/api/history?limit=0", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'}
        )
        assert response.status_code == 400

    def test_get_history_invalid_doc_type(self, client, test_users):
        """Test validation of doc_type parameter."""
        response = client.get(
            "/api/history?doc_type=invalid", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'}
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_get_history_contains_metadata(self, client, test_users, sample_documents):
        """Test that history response contains necessary metadata."""
        response = client.get("/api/history", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'})

        assert response.status_code == 200
        data = response.get_json()

        # Check first document has required fields
        doc = data["documents"][0]
        assert "id" in doc
        assert "doc_type" in doc
        assert "title" in doc
        assert "tone" in doc
        assert "created_at" in doc
        assert "content_preview" in doc

        # For reports, should have structure field
        report_doc = [d for d in data["documents"] if d["doc_type"] == "report"][0]
        assert "structure" in report_doc


class TestDocumentDetailEndpoint:
    """Tests for document detail endpoint."""

    def test_get_document_detail_requires_auth(self, client):
        """Test that document detail endpoint requires authentication."""
        response = client.get("/api/history/1")
        assert response.status_code == 401

    def test_get_document_detail_success(self, client, test_users, sample_documents, app):
        """Test retrieving full document details."""
        doc_id = sample_documents["user1_docs"][0]

        response = client.get(
            f"/api/history/{doc_id}", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "document" in data
        assert data["document"]["id"] == doc_id
        assert "content" in data["document"]

    def test_get_document_detail_cross_user_blocked(self, client, test_users, sample_documents):
        """Test that users cannot access other users' documents."""
        # User 2's document ID
        user2_doc_id = sample_documents["user2_docs"][0]

        # User 1 tries to access User 2's document
        response = client.get(
            f"/api/history/{user2_doc_id}", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'}
        )

        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_get_document_detail_not_found(self, client, test_users):
        """Test retrieving non-existent document."""
        response = client.get("/api/history/99999", headers={"Authorization": f'Bearer {test_users["user1"]["token"]}'})

        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
