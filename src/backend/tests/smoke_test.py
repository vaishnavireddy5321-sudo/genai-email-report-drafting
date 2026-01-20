"""Smoke test for database operations.

This script validates that the database schema is properly set up and
all basic CRUD operations work correctly.
"""

import os
import sys

# Set environment variable BEFORE importing anything
os.environ["TEST_DATABASE_URL"] = "sqlite:///:memory:"

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app import create_app  # noqa: E402
from db import db  # noqa: E402
from models.audit_log import AuditLog  # noqa: E402
from models.document import Document  # noqa: E402
from models.user import User  # noqa: E402


def run_smoke_tests():
    """Run smoke tests for database operations."""
    print("=" * 60)
    print("GenAI Email & Report Drafting - Database Smoke Tests")
    print("=" * 60)

    # Create test app with in-memory SQLite database
    app = create_app("test")

    with app.app_context():
        # Create all tables
        print("\n[1/6] Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully")

        # Test 1: Create a user
        print("\n[2/6] Creating test user...")
        user = User(username="testuser", email="test@example.com", password_hash="hashed_password_here", role="USER")
        db.session.add(user)
        db.session.commit()
        print(f"✓ User created: {user}")

        # Test 2: Insert a document
        print("\n[3/6] Creating test document...")
        document = Document(
            user_id=user.id,
            doc_type="email",
            title="Test Email",
            prompt_input="Write a professional email",
            content="This is a test email content.",
            tone="professional",
        )
        db.session.add(document)
        db.session.commit()
        print(f"✓ Document created: {document}")

        # Test 3: Insert an audit log
        print("\n[4/6] Creating test audit log...")
        audit_log = AuditLog(
            user_id=user.id,
            action="generate_email",
            entity_type="document",
            entity_id=document.id,
            request_context_id="test-request-123",
            details="Test document generation",
        )
        db.session.add(audit_log)
        db.session.commit()
        print(f"✓ Audit log created: {audit_log}")

        # Test 4: Query documents by user
        print("\n[5/6] Querying documents by user...")
        user_documents = Document.query.filter_by(user_id=user.id).order_by(Document.created_at.desc()).all()
        print(f"✓ Found {len(user_documents)} document(s) for user {user.username}")
        for doc in user_documents:
            print(f"  - {doc.doc_type}: {doc.title}")

        # Test 5: Query audit logs
        print("\n[6/6] Querying audit logs...")
        audit_logs = AuditLog.query.filter_by(user_id=user.id).order_by(AuditLog.created_at.desc()).all()
        print(f"✓ Found {len(audit_logs)} audit log(s) for user {user.username}")
        for log in audit_logs:
            print(f"  - {log.action} on {log.entity_type} {log.entity_id}")

        # Test relationships
        print("\n[Bonus] Testing relationships...")
        user_from_db = User.query.filter_by(username="testuser").first()
        print(f"✓ User has {len(user_from_db.documents)} document(s)")
        print(f"✓ User has {len(user_from_db.audit_logs)} audit log(s)")

        print("\n" + "=" * 60)
        print("All smoke tests passed! ✓")
        print("=" * 60)
        return True


if __name__ == "__main__":
    try:
        success = run_smoke_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Smoke test failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
