"""Document generation routes for email and report drafting.

This module provides endpoints for generating AI-powered emails and reports
using Google Gemini LLM with proper validation, persistence, and audit logging.
"""

from db import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.document import Document
from services.gemini_service import GeminiError, GeminiService
from services.prompt_engine import PromptEngine
from utils.audit_helpers import create_audit_log
from utils.request_helpers import get_request_id

documents_bp = Blueprint("documents", __name__, url_prefix="/api/documents")

# Valid options for validation
VALID_TONES = ["professional", "casual", "formal", "friendly"]
VALID_STRUCTURES = ["executive_summary", "detailed", "bullet_points"]
MAX_CONTEXT_LENGTH = 5000
MAX_FIELD_LENGTH = 500


def _validate_email_request(data):
    """Validate email generation request data.

    Returns:
        tuple: (is_valid, error_response or validated_data)
    """
    if not data:
        return False, (jsonify({"error": "Request body must be JSON"}), 400)

    context = data.get("context", "").strip()
    if not context:
        return False, (jsonify({"error": "context is required"}), 400)

    if len(context) > MAX_CONTEXT_LENGTH:
        return False, (jsonify({"error": f"context exceeds maximum length of {MAX_CONTEXT_LENGTH} characters"}), 400)

    recipient = data.get("recipient", "").strip() or None
    subject = data.get("subject", "").strip() or None
    tone = data.get("tone", "professional").strip().lower()

    if tone not in VALID_TONES:
        return False, (jsonify({"error": f'Invalid tone. Must be one of: {", ".join(VALID_TONES)}'}), 400)

    if recipient and len(recipient) > MAX_FIELD_LENGTH:
        return False, (jsonify({"error": f"recipient exceeds maximum length of {MAX_FIELD_LENGTH} characters"}), 400)

    if subject and len(subject) > MAX_FIELD_LENGTH:
        return False, (jsonify({"error": f"subject exceeds maximum length of {MAX_FIELD_LENGTH} characters"}), 400)

    return True, {"context": context, "recipient": recipient, "subject": subject, "tone": tone}


def _validate_report_request(data):
    """Validate report generation request data.

    Returns:
        tuple: (is_valid, error_response or validated_data)
    """
    if not data:
        return False, (jsonify({"error": "Request body must be JSON"}), 400)

    topic = data.get("topic", "").strip()
    if not topic:
        return False, (jsonify({"error": "topic is required"}), 400)

    if len(topic) > MAX_CONTEXT_LENGTH:
        return False, (jsonify({"error": f"topic exceeds maximum length of {MAX_CONTEXT_LENGTH} characters"}), 400)

    key_points = data.get("key_points", "").strip() or None
    tone = data.get("tone", "professional").strip().lower()
    structure = data.get("structure", "detailed").strip().lower()

    if tone not in VALID_TONES:
        return False, (jsonify({"error": f'Invalid tone. Must be one of: {", ".join(VALID_TONES)}'}), 400)

    if structure not in VALID_STRUCTURES:
        return False, (jsonify({"error": f'Invalid structure. Must be one of: {", ".join(VALID_STRUCTURES)}'}), 400)

    if key_points and len(key_points) > MAX_CONTEXT_LENGTH:
        return False, (jsonify({"error": f"key_points exceeds maximum length of {MAX_CONTEXT_LENGTH} characters"}), 400)

    return True, {"topic": topic, "key_points": key_points, "tone": tone, "structure": structure}


def _generate_with_gemini(prompt, request_id, user_id, action_name):
    """Generate content using Gemini service.

    Returns:
        tuple: (success, content or error_response)
    """
    try:
        gemini_service = GeminiService()
    except GeminiError:
        return False, (jsonify({"error": "AI service unavailable"}), 503)

    try:
        result = gemini_service.generate_content(prompt=prompt, correlation_id=request_id)
        return True, result["content"]
    except GeminiError as e:
        create_audit_log(
            user_id=user_id,
            action=f"{action_name}_failed",
            entity_type="document",
            details=f"Failed to generate {action_name.split('_')[1]}: {type(e).__name__}",
            request_context_id=request_id,
        )
        return False, (jsonify({"error": f"Failed to generate {action_name.split('_')[1]}. Please try again."}), 500)


@documents_bp.route("/email:generate", methods=["POST"])
@jwt_required()
def generate_email():
    """Generate an email draft using AI.

    Rate Limited: 10 requests per minute per IP address.

    Requires:
        Valid JWT token in Authorization header

    Request JSON:
        context (str): Main content or purpose of the email (required, max 5000 chars)
        recipient (str): Optional recipient information
        subject (str): Optional subject line or topic
        tone (str): Desired tone (professional, casual, formal, friendly), default: professional

    Returns:
        JSON response with generated email content and metadata
    """
    try:
        request_id = get_request_id()
        user_id = int(get_jwt_identity())

        # Validate request
        is_valid, result = _validate_email_request(request.get_json())
        if not is_valid:
            return result

        validated = result

        # Build prompt
        try:
            prompt = PromptEngine.build_email_prompt(
                context=validated["context"],
                recipient=validated["recipient"],
                subject=validated["subject"],
                tone=validated["tone"],
            )
        except ValueError as e:
            return jsonify({"error": f"Invalid input: {str(e)}"}), 400

        # Generate content
        success, gen_result = _generate_with_gemini(prompt, request_id, user_id, "generate_email")
        if not success:
            return gen_result

        generated_content = gen_result

        # Create document record
        document = Document(
            user_id=user_id,
            doc_type="email",
            title=validated["subject"],
            prompt_input=validated["context"],
            content=generated_content,
            tone=validated["tone"],
            structure=None,
        )
        db.session.add(document)
        db.session.commit()

        # Create audit log
        create_audit_log(
            user_id=user_id,
            action="generate_email",
            entity_type="document",
            entity_id=document.id,
            details=f"Generated email with tone: {validated['tone']}",
            request_context_id=request_id,
        )

        return (
            jsonify(
                {"message": "Email generated successfully", "document": document.to_dict(), "request_id": request_id}
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@documents_bp.route("/report:generate", methods=["POST"])
@jwt_required()
def generate_report():
    """Generate a report draft using AI.

    Rate Limited: 10 requests per minute per IP address.

    Requires:
        Valid JWT token in Authorization header

    Request JSON:
        topic (str): Main topic or title of the report (required, max 5000 chars)
        key_points (str): Optional key points or data to include
        tone (str): Desired tone (professional, formal, casual, friendly), default: professional
        structure (str): Report structure (executive_summary, detailed, bullet_points), default: detailed

    Returns:
        JSON response with generated report content and metadata
    """
    try:
        request_id = get_request_id()
        user_id = int(get_jwt_identity())

        # Validate request
        is_valid, result = _validate_report_request(request.get_json())
        if not is_valid:
            return result

        validated = result

        # Build prompt
        try:
            prompt = PromptEngine.build_report_prompt(
                topic=validated["topic"],
                key_points=validated["key_points"],
                tone=validated["tone"],
                structure=validated["structure"],
            )
        except ValueError as e:
            return jsonify({"error": f"Invalid input: {str(e)}"}), 400

        # Generate content
        success, gen_result = _generate_with_gemini(prompt, request_id, user_id, "generate_report")
        if not success:
            return gen_result

        generated_content = gen_result

        # Create document record
        document = Document(
            user_id=user_id,
            doc_type="report",
            title=validated["topic"],
            prompt_input=validated["key_points"],
            content=generated_content,
            tone=validated["tone"],
            structure=validated["structure"],
        )
        db.session.add(document)
        db.session.commit()

        # Create audit log
        create_audit_log(
            user_id=user_id,
            action="generate_report",
            entity_type="document",
            entity_id=document.id,
            details=f"Generated report with tone: {validated['tone']}, structure: {validated['structure']}",
            request_context_id=request_id,
        )

        return (
            jsonify(
                {"message": "Report generated successfully", "document": document.to_dict(), "request_id": request_id}
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
