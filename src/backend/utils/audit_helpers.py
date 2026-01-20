"""Audit logging utilities.

This module provides helper functions for creating audit log entries
to track user actions and system events.
"""

from db import db
from models.audit_log import AuditLog


def create_audit_log(
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int = None,
    details: str = None,
    request_context_id: str = None,
) -> None:
    """Create an audit log entry.

    Args:
        user_id: ID of the user performing the action
        action: Action being performed
        entity_type: Type of entity affected
        entity_id: ID of affected entity
        details: Additional context
        request_context_id: Correlation ID for request tracking
    """
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details,
        request_context_id=request_context_id,
    )
    db.session.add(audit_log)
    db.session.commit()
