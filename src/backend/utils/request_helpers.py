"""Request handling utilities.

This module provides helper functions for handling HTTP requests,
including request ID generation and correlation tracking.
"""

import uuid

from flask import request


def get_request_id() -> str:
    """Get or generate request correlation ID from headers.

    Returns:
        Request correlation ID (from X-Request-Id header or generated)
    """
    return request.headers.get("X-Request-Id", str(uuid.uuid4()))
