"""Document model for storing generated emails and reports.

This module defines the Document model for persisting AI-generated
content with associated metadata and user ownership.
"""

from datetime import datetime
from typing import Optional

from db import db
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column


class Document(db.Model):
    """Document model for storing generated content.

    Attributes:
        id: Primary key identifier
        user_id: Foreign key to User who generated the document
        doc_type: Type of document (email or report)
        title: Optional title or subject line
        prompt_input: Sanitized user input/context (optional for audit)
        content: Generated document content
        tone: Tone used for generation (professional, casual, formal, friendly)
        structure: Structure type for reports (executive_summary, detailed, bullet_points)
        created_at: Timestamp of document generation
    """

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    doc_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    prompt_input: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tone: Mapped[str] = mapped_column(String(50), nullable=False)
    structure: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Relationships
    user = db.relationship("User", back_populates="documents")

    # Composite index for efficient user history queries
    __table_args__ = (Index("idx_user_created", "user_id", "created_at"),)

    def __repr__(self) -> str:
        """String representation of Document."""
        return f"<Document {self.id} ({self.doc_type}) by User {self.user_id}>"

    def to_dict(self) -> dict:
        """Convert Document to dictionary representation.

        Returns:
            Dictionary with document information
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "doc_type": self.doc_type,
            "title": self.title,
            "prompt_input": self.prompt_input,
            "content": self.content,
            "tone": self.tone,
            "structure": self.structure,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
