"""User model for authentication and authorization.

This module defines the User model for storing user account information,
including authentication credentials and role-based access control.
"""

from datetime import datetime

from db import db
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """User model for authentication and role management.

    Attributes:
        id: Primary key identifier
        username: Unique username for login
        email: Unique email address
        password_hash: Hashed password (never store plain text)
        role: User role (USER or ADMIN)
        created_at: Timestamp of user creation
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="USER")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    documents = db.relationship("Document", back_populates="user", cascade="all, delete-orphan")
    audit_logs = db.relationship("AuditLog", back_populates="user", passive_deletes=True)

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User {self.username} ({self.role})>"

    def set_password(self, password: str) -> None:
        """Hash and set the user's password.

        Args:
            password: Plain text password to hash
        """
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password: str) -> bool:
        """Verify the provided password against stored hash.

        Args:
            password: Plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        """Convert User to dictionary representation.

        Returns:
            Dictionary with user information (excluding password_hash)
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
