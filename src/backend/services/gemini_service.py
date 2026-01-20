"""Google Gemini integration service for AI content generation.

This module provides a wrapper around the Google Gemini API with
production-grade error handling, timeout management, and diagnostic logging.
"""

import logging
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

# Configure logger for this module
logger = logging.getLogger(__name__)


class GeminiError(Exception):
    """Base exception for Gemini service errors."""

    pass


class GeminiAPIError(GeminiError):
    """Exception for API-related errors (network, auth, etc)."""

    pass


class GeminiRateLimitError(GeminiError):
    """Exception for rate limit errors."""

    pass


class GeminiTimeoutError(GeminiError):
    """Exception for timeout errors."""

    pass


class GeminiService:
    """Service wrapper for Google Gemini API integration.

    This class handles all interactions with the Google Gemini API,
    including configuration, error handling, timeout management,
    and diagnostic logging.

    Attributes:
        api_key: Google Gemini API key (from environment)
        model_name: Name of the Gemini model to use
        timeout: Request timeout in seconds
    """

    # Default configuration
    DEFAULT_MODEL = "gemini-3-flash-preview"
    DEFAULT_TIMEOUT = 30  # seconds
    DEFAULT_TEMPERATURE = 0.7
    MAX_OUTPUT_TOKENS = 2048

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None, timeout: Optional[int] = None):
        """Initialize Gemini service.

        Args:
            api_key: Google Gemini API key (defaults to GEMINI_API_KEY env var)
            model_name: Model name to use (defaults to gemini-3-flash-preview)
            timeout: Request timeout in seconds (defaults to 30)

        Raises:
            GeminiError: If API key is not provided and not found in environment
        """
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise GeminiError(
                "Gemini API key not configured. Set GEMINI_API_KEY environment variable " "or pass api_key parameter."
            )

        self.model_name = model_name or os.getenv("GEMINI_MODEL") or self.DEFAULT_MODEL
        self.timeout = timeout or self.DEFAULT_TIMEOUT

        # Initialize the Gemini client
        try:
            import google.generativeai as genai

            self._genai = genai

            # Configure the API key (but don't log it)
            genai.configure(api_key=self.api_key)

            # Initialize the model
            self._model = genai.GenerativeModel(self.model_name)

            logger.info(
                "GeminiService initialized successfully", extra={"model": self.model_name, "timeout": self.timeout}
            )

        except ImportError as e:
            raise GeminiError(
                "google-generativeai package not installed. " "Run: pip install google-generativeai"
            ) from e
        except Exception as e:
            # Log error without exposing API key
            logger.error("Failed to initialize Gemini service", extra={"error_type": type(e).__name__})
            raise GeminiError(f"Failed to initialize Gemini service: {str(e)}") from e

    def generate_content(  # noqa: C901
        self, prompt: str, temperature: Optional[float] = None, correlation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate content using Gemini API.

        This method sends a prompt to the Gemini API and returns the generated
        content with metadata. It includes comprehensive error handling and
        diagnostic logging.

        Args:
            prompt: The prompt text to send to Gemini
            temperature: Sampling temperature (0.0 to 1.0), defaults to 0.7
            correlation_id: Optional correlation ID for request tracking

        Returns:
            Dictionary containing:
                - content: Generated text content
                - model: Model name used
                - timestamp: Generation timestamp
                - correlation_id: Request correlation ID
                - latency_ms: Request latency in milliseconds

        Raises:
            GeminiAPIError: For API-related errors
            GeminiRateLimitError: For rate limit errors
            GeminiTimeoutError: For timeout errors
            GeminiError: For other errors
        """
        correlation_id, temperature = self._prepare_request(prompt, temperature, correlation_id)

        # Log request (without prompt content to avoid log bloat)
        logger.info(
            "Gemini API request initiated",
            extra={
                "correlation_id": correlation_id,
                "model": self.model_name,
                "prompt_length": len(prompt),
                "temperature": temperature,
            },
        )

        content, latency_ms = self._call_gemini(prompt, temperature, correlation_id)

        return {
            "content": content,
            "model": self.model_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "correlation_id": correlation_id,
            "latency_ms": latency_ms,
        }

    @staticmethod
    def _normalize_output(content: str) -> str:
        """Normalize generated content output.

        Ensures consistent whitespace and newline handling for storage
        and downstream processing.

        Args:
            content: Raw content from Gemini API

        Returns:
            Normalized content string
        """
        if not content:
            return ""

        # Strip leading/trailing whitespace
        content = content.strip()

        # Normalize line endings to Unix style
        content = content.replace("\r\n", "\n").replace("\r", "\n")

        # Remove excessive blank lines (more than 2 consecutive newlines)
        import re

        content = re.sub(r"\n{3,}", "\n\n", content)

        return content

    def _prepare_request(
        self, prompt: str, temperature: Optional[float], correlation_id: Optional[str]
    ) -> tuple[str, float]:
        """Prepare and validate request parameters."""
        if correlation_id is None:
            correlation_id = str(uuid.uuid4())

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        if temperature is None:
            temperature = self.DEFAULT_TEMPERATURE

        if not 0.0 <= temperature <= 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0")

        return correlation_id, temperature

    def _call_gemini(self, prompt: str, temperature: float, correlation_id: str) -> tuple[str, int]:
        """Call Gemini API and return normalized content with latency."""
        start_time = time.time()

        try:
            generation_config = self._genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=self.MAX_OUTPUT_TOKENS,
            )

            response = self._model.generate_content(prompt, generation_config=generation_config)
            latency_ms = self._latency_ms(start_time)

            if not response or not response.text:
                raise GeminiAPIError("API returned empty response")

            content = self._normalize_output(response.text)

            logger.info(
                "Gemini API request completed successfully",
                extra={"correlation_id": correlation_id, "latency_ms": latency_ms, "content_length": len(content)},
            )

            return content, latency_ms

        except self._genai.types.BlockedPromptException as e:
            self._raise_gemini_error(
                log_method=logger.warning,
                message="Gemini API blocked prompt (safety filters)",
                user_message=(
                    "Content generation blocked due to safety filters. " "Please revise your input and try again."
                ),
                correlation_id=correlation_id,
                start_time=start_time,
                error_type="blocked_prompt",
                exc_cls=GeminiAPIError,
                original=e,
            )

        except self._genai.types.StopCandidateException as e:
            self._raise_gemini_error(
                log_method=logger.warning,
                message="Gemini API stopped generation",
                user_message="Content generation stopped. Please try again or modify your input.",
                correlation_id=correlation_id,
                start_time=start_time,
                error_type="stop_candidate",
                exc_cls=GeminiAPIError,
                original=e,
            )

        except Exception as e:
            self._handle_generic_exception(e, correlation_id, start_time)

        return "", self._latency_ms(start_time)

    @staticmethod
    def _latency_ms(start_time: float) -> int:
        """Calculate latency in milliseconds."""
        return int((time.time() - start_time) * 1000)

    def _raise_gemini_error(
        self,
        log_method,
        message: str,
        user_message: str,
        correlation_id: str,
        start_time: float,
        error_type: str,
        exc_cls,
        original: Exception,
    ):
        """Log and raise a Gemini-related error with consistent metadata."""
        latency_ms = self._latency_ms(start_time)
        log_method(
            message,
            extra={"correlation_id": correlation_id, "latency_ms": latency_ms, "error_type": error_type},
        )
        raise exc_cls(user_message) from original

    def _handle_generic_exception(self, error: Exception, correlation_id: str, start_time: float):
        """Classify and raise generic Gemini exceptions with minimal branching."""
        latency_ms = self._latency_ms(start_time)
        error_msg = str(error).lower()

        def _raise(exc_cls, user_msg, error_type):
            logger.error(
                "Gemini API request failed",
                extra={"correlation_id": correlation_id, "latency_ms": latency_ms, "error_type": error_type},
            )
            raise exc_cls(user_msg) from error

        conditions = [
            (
                lambda msg: any(token in msg for token in ["rate", "quota", "429"]),
                GeminiRateLimitError,
                "Rate limit exceeded. Please try again later.",
                "rate_limit",
            ),
            (
                lambda msg: "timeout" in msg or "timed out" in msg,
                GeminiTimeoutError,
                "Request timed out. Please try again.",
                "timeout",
            ),
            (
                lambda msg: "api" in msg and "key" in msg,
                GeminiAPIError,
                "API authentication failed. Please check your API key configuration.",
                "auth_error",
            ),
            (
                lambda msg: "network" in msg or "connection" in msg,
                GeminiAPIError,
                "Network error occurred. Please check your connection and try again.",
                "network_error",
            ),
        ]

        for predicate, exc_cls, user_msg, error_type in conditions:
            if predicate(error_msg):
                _raise(exc_cls, user_msg, error_type)

        _raise(GeminiAPIError, "An error occurred while generating content. Please try again.", type(error).__name__)

    def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the Gemini service.

        Verifies that the service is properly configured and can
        communicate with the Gemini API.

        Returns:
            Dictionary with health status information
        """
        try:
            # Try a simple generation with minimal prompt
            test_response = self.generate_content(
                prompt="Respond with 'OK' only.", temperature=0.0, correlation_id="health-check"
            )

            return {
                "status": "healthy",
                "model": self.model_name,
                "latency_ms": test_response.get("latency_ms"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            logger.error("Gemini service health check failed", extra={"error_type": type(e).__name__})

            return {
                "status": "unhealthy",
                "model": self.model_name,
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
