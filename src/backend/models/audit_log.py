"""Audit log model for tracking system actions and events.

This module defines the AuditLog model for maintaining a comprehensive
audit trail of user actions and system events for compliance and traceability.
"""

from datetime import datetime
from typing import Optional

from db import db
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class AuditLog(db.Model):
    """Audit log model for tracking actions and events.

    Attributes:
        id: Primary key identifier
        user_id: Foreign key to User (nullable for system actions)
        action: Action performed (e.g., 'generate_email', 'generate_report', 'login')
        entity_type: Type of entity affected (e.g., 'document', 'user')
        entity_id: ID of affected entity (optional)
        request_context_id: Unique request/session identifier for correlation
        details: Additional context as text (optional)
        created_at: Timestamp of the action
    """

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    request_context_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Relationships
    user = db.relationship("User", back_populates="audit_logs")

    # Composite indexes for efficient audit queries
    __table_args__ = (
        Index("idx_user_created_audit", "user_id", "created_at"),
        Index("idx_action_created", "action", "created_at"),
    )

    def __repr__(self) -> str:
        """String representation of AuditLog."""
        user_info = f"User {self.user_id}" if self.user_id else "System"
        return f"<AuditLog {self.id}: {self.action} by {user_info}>"

    def to_dict(self) -> dict:
        """Convert AuditLog to dictionary representation.

        Returns:
            Dictionary with audit log information
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "request_context_id": self.request_context_id,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
