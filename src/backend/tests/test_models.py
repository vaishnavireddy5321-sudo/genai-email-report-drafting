"""Unit tests for database models."""

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


class TestUserModel:
    """Tests for User model."""

    def test_create_user(self, app):
        """Test creating a user."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed_password", role="USER")
            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.username == "testuser"
            assert user.email == "test@example.com"
            assert user.role == "USER"
            assert user.created_at is not None

    def test_user_to_dict(self, app):
        """Test user to_dict method."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed_password", role="ADMIN")
            db.session.add(user)
            db.session.commit()

            user_dict = user.to_dict()
            assert user_dict["username"] == "testuser"
            assert user_dict["email"] == "test@example.com"
            assert user_dict["role"] == "ADMIN"
            assert "password_hash" not in user_dict

    def test_unique_username(self, app):
        """Test that username must be unique."""
        with app.app_context():
            user1 = User(username="testuser", email="test1@example.com", password_hash="hash1", role="USER")
            db.session.add(user1)
            db.session.commit()

            user2 = User(username="testuser", email="test2@example.com", password_hash="hash2", role="USER")
            db.session.add(user2)

            with pytest.raises(Exception):
                db.session.commit()


class TestDocumentModel:
    """Tests for Document model."""

    def test_create_document(self, app):
        """Test creating a document."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed_password", role="USER")
            db.session.add(user)
            db.session.commit()

            document = Document(
                user_id=user.id,
                doc_type="email",
                title="Test Email",
                prompt_input="Write an email",
                content="Email content here",
                tone="professional",
            )
            db.session.add(document)
            db.session.commit()

            assert document.id is not None
            assert document.user_id == user.id
            assert document.doc_type == "email"
            assert document.title == "Test Email"
            assert document.created_at is not None

    def test_document_user_relationship(self, app):
        """Test relationship between document and user."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed_password", role="USER")
            db.session.add(user)
            db.session.commit()

            document = Document(
                user_id=user.id,
                doc_type="report",
                content="Report content",
                tone="formal",
                structure="executive_summary",
            )
            db.session.add(document)
            db.session.commit()

            # Test forward relationship
            assert document.user.username == "testuser"

            # Test backward relationship
            assert len(user.documents) == 1
            assert user.documents[0].id == document.id

    def test_query_documents_by_user(self, app):
        """Test querying documents by user."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed_password", role="USER")
            db.session.add(user)
            db.session.commit()

            # Create multiple documents
            for i in range(3):
                doc = Document(user_id=user.id, doc_type="email", content=f"Content {i}", tone="professional")
                db.session.add(doc)
            db.session.commit()

            # Query documents
            docs = Document.query.filter_by(user_id=user.id).order_by(Document.created_at.desc()).all()

            assert len(docs) == 3


class TestAuditLogModel:
    """Tests for AuditLog model."""

    def test_create_audit_log(self, app):
        """Test creating an audit log."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed_password", role="USER")
            db.session.add(user)
            db.session.commit()

            audit_log = AuditLog(
                user_id=user.id, action="login", request_context_id="req-123", details="User logged in successfully"
            )
            db.session.add(audit_log)
            db.session.commit()

            assert audit_log.id is not None
            assert audit_log.user_id == user.id
            assert audit_log.action == "login"
            assert audit_log.created_at is not None

    def test_audit_log_nullable_user(self, app):
        """Test that audit log can have nullable user_id for system actions."""
        with app.app_context():
            audit_log = AuditLog(user_id=None, action="system_startup", details="System started")
            db.session.add(audit_log)
            db.session.commit()

            assert audit_log.id is not None
            assert audit_log.user_id is None
            assert audit_log.action == "system_startup"

    def test_query_audit_logs_by_user(self, app):
        """Test querying audit logs by user."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed_password", role="USER")
            db.session.add(user)
            db.session.commit()

            # Create multiple audit logs
            for i in range(5):
                log = AuditLog(user_id=user.id, action=f"action_{i}", request_context_id=f"req-{i}")
                db.session.add(log)
            db.session.commit()

            # Query logs
            logs = AuditLog.query.filter_by(user_id=user.id).order_by(AuditLog.created_at.desc()).all()

            assert len(logs) == 5


class TestCascadeDelete:
    """Tests for cascade delete behavior."""

    def test_delete_user_cascades_documents(self, app):
        """Test that deleting a user also deletes their documents."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed_password", role="USER")
            db.session.add(user)
            db.session.commit()

            document = Document(user_id=user.id, doc_type="email", content="Test content", tone="professional")
            db.session.add(document)
            db.session.commit()

            doc_id = document.id

            # Delete user
            db.session.delete(user)
            db.session.commit()

            # Check document is also deleted
            deleted_doc = Document.query.filter_by(id=doc_id).first()
            assert deleted_doc is None

    def test_delete_user_preserves_audit_logs(self, app):
        """Test that deleting a user preserves audit logs with null user_id."""
        with app.app_context():
            user = User(username="testuser", email="test@example.com", password_hash="hashed_password", role="USER")
            db.session.add(user)
            db.session.commit()

            audit_log = AuditLog(user_id=user.id, action="test_action")
            db.session.add(audit_log)
            db.session.commit()

            log_id = audit_log.id

            # Delete user
            db.session.delete(user)
            db.session.commit()

            # Check audit log is preserved and user_id is set to null
            preserved_log = AuditLog.query.filter_by(id=log_id).first()
            assert preserved_log is not None
            assert preserved_log.user_id is None
