"""Document history routes for retrieving user's generated documents.

This module provides endpoints for fetching document history with proper
user-scoping to prevent cross-user data leakage.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.document import Document

history_bp = Blueprint("history", __name__, url_prefix="/api")


@history_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    """Get document history for the authenticated user.

    Requires:
        Valid JWT token in Authorization header

    Query Parameters:
        limit (int): Optional limit on number of results (default: 50, max: 100)
        offset (int): Optional offset for pagination (default: 0)
        doc_type (str): Optional filter by document type (email or report)

    Returns:
        JSON response with list of user's documents ordered by most recent first
    """
    try:
        # Get authenticated user ID
        user_id = int(get_jwt_identity())

        # Parse query parameters
        limit = request.args.get("limit", 50, type=int)
        offset = request.args.get("offset", 0, type=int)
        doc_type = request.args.get("doc_type", "").strip().lower()

        # Validate parameters
        if limit < 1 or limit > 100:
            return jsonify({"error": "limit must be between 1 and 100"}), 400

        if offset < 0:
            return jsonify({"error": "offset must be non-negative"}), 400

        if doc_type and doc_type not in ["email", "report"]:
            return jsonify({"error": 'doc_type must be either "email" or "report"'}), 400

        # Build query - CRITICAL: Filter by user_id to prevent cross-user leakage
        query = Document.query.filter_by(user_id=user_id)

        # Apply optional type filter
        if doc_type:
            query = query.filter_by(doc_type=doc_type)

        # Order by most recent first
        query = query.order_by(Document.created_at.desc())

        # Get total count before pagination
        total_count = query.count()

        # Apply pagination
        documents = query.limit(limit).offset(offset).all()

        # Convert to minimal metadata for UI
        document_list = []
        for doc in documents:
            document_list.append(
                {
                    "id": doc.id,
                    "doc_type": doc.doc_type,
                    "title": doc.title,
                    "tone": doc.tone,
                    "structure": doc.structure,
                    "created_at": doc.created_at.isoformat() if doc.created_at else None,
                    "content_preview": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                }
            )

        return (
            jsonify(
                {
                    "documents": document_list,
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": (offset + limit) < total_count,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": f"Failed to retrieve history: {str(e)}"}), 500


@history_bp.route("/history/<int:document_id>", methods=["GET"])
@jwt_required()
def get_document_detail(document_id: int):
    """Get full details of a specific document.

    Requires:
        Valid JWT token in Authorization header

    Path Parameters:
        document_id: ID of the document to retrieve

    Returns:
        JSON response with full document details
    """
    try:
        # Get authenticated user ID
        user_id = int(get_jwt_identity())

        # Query document - CRITICAL: Filter by user_id to prevent cross-user access
        document = Document.query.filter_by(id=document_id, user_id=user_id).first()

        if not document:
            return jsonify({"error": "Document not found"}), 404

        return jsonify({"document": document.to_dict()}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to retrieve document: {str(e)}"}), 500
