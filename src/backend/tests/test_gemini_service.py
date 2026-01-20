"""Unit tests for GeminiService module."""

import os
from unittest.mock import Mock, patch

import pytest
from services.gemini_service import GeminiAPIError, GeminiError, GeminiRateLimitError, GeminiService, GeminiTimeoutError


class TestGeminiServiceInitialization:
    """Tests for GeminiService initialization."""

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_init_with_api_key_parameter(self, mock_model_class, mock_configure):
        """Test initialization with API key parameter."""
        service = GeminiService(api_key="test-api-key")

        assert service.api_key == "test-api-key"
        assert service.model_name == "gemini-3-flash-preview"
        assert service.timeout == 30
        mock_configure.assert_called_once_with(api_key="test-api-key")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_init_with_environment_variable(self, mock_model_class, mock_configure):
        """Test initialization with GEMINI_API_KEY environment variable."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "env-api-key"}):
            service = GeminiService()

            assert service.api_key == "env-api-key"
            mock_configure.assert_called_once_with(api_key="env-api-key")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_init_with_custom_model(self, mock_model_class, mock_configure):
        """Test initialization with custom model name."""
        service = GeminiService(api_key="test-key", model_name="gemini-3-flash-preview-vision")

        assert service.model_name == "gemini-3-flash-preview-vision"

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_init_with_custom_timeout(self, mock_model_class, mock_configure):
        """Test initialization with custom timeout."""
        service = GeminiService(api_key="test-key", timeout=60)

        assert service.timeout == 60

    def test_init_without_api_key_raises_error(self):
        """Test that initialization without API key raises error."""
        # Clear environment variable if it exists
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(GeminiError, match="API key not configured"):
                GeminiService()

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_init_logs_no_secrets(self, mock_model_class, mock_configure, caplog):
        """Test that initialization does not log API key."""
        _ = GeminiService(api_key="secret-api-key-12345")

        # Check that API key is not in any log message
        for record in caplog.records:
            assert "secret-api-key-12345" not in record.message
            assert "secret-api-key-12345" not in str(record.args)


class TestGeminiServiceGeneration:
    """Tests for content generation methods."""

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_generate_content_success(self, mock_model_class, mock_configure):
        """Test successful content generation."""
        # Setup mock response
        mock_response = Mock()
        mock_response.text = "Generated email content here."

        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")

        result = service.generate_content(prompt="Write an email", correlation_id="test-123")

        assert result["content"] == "Generated email content here."
        assert result["model"] == "gemini-3-flash-preview"
        assert result["correlation_id"] == "test-123"
        assert "timestamp" in result
        assert "latency_ms" in result
        assert isinstance(result["latency_ms"], int)

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_generate_content_auto_correlation_id(self, mock_model_class, mock_configure):
        """Test that correlation ID is generated if not provided."""
        mock_response = Mock()
        mock_response.text = "Test content"

        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")
        result = service.generate_content(prompt="Test")

        assert "correlation_id" in result
        assert len(result["correlation_id"]) > 0

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_generate_content_with_temperature(self, mock_model_class, mock_configure):
        """Test content generation with custom temperature."""
        mock_response = Mock()
        mock_response.text = "Test content"

        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")
        result = service.generate_content(prompt="Test", temperature=0.9)

        assert result["content"] == "Test content"

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_generate_content_empty_prompt_raises_error(self, mock_model_class, mock_configure):
        """Test that empty prompt raises ValueError."""
        service = GeminiService(api_key="test-key")

        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            service.generate_content(prompt="")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_generate_content_invalid_temperature_raises_error(self, mock_model_class, mock_configure):
        """Test that invalid temperature raises ValueError."""
        service = GeminiService(api_key="test-key")

        with pytest.raises(ValueError, match="Temperature must be between"):
            service.generate_content(prompt="Test", temperature=1.5)

        with pytest.raises(ValueError, match="Temperature must be between"):
            service.generate_content(prompt="Test", temperature=-0.1)

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_generate_content_normalizes_output(self, mock_model_class, mock_configure):
        """Test that output is normalized."""
        # Response with excessive whitespace and mixed line endings
        mock_response = Mock()
        mock_response.text = "  \r\nTest content\r\n\n\n\n\nExtra lines  \r\n"

        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")
        result = service.generate_content(prompt="Test")

        # Should be normalized (trimmed, consistent newlines, no excessive blanks)
        content = result["content"]
        assert not content.startswith(" ")
        assert not content.endswith(" ")
        assert "\r\n" not in content
        assert "\n\n\n" not in content


class TestGeminiServiceErrorHandling:
    """Tests for error handling in GeminiService."""

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_rate_limit_error(self, mock_model_class, mock_configure):
        """Test handling of rate limit errors."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("Rate limit exceeded")
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")

        with pytest.raises(GeminiRateLimitError, match="Rate limit"):
            service.generate_content(prompt="Test")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_quota_error(self, mock_model_class, mock_configure):
        """Test handling of quota errors."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("Quota exceeded")
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")

        with pytest.raises(GeminiRateLimitError):
            service.generate_content(prompt="Test")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_timeout_error(self, mock_model_class, mock_configure):
        """Test handling of timeout errors."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("Request timed out")
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")

        with pytest.raises(GeminiTimeoutError, match="timed out"):
            service.generate_content(prompt="Test")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_api_key_error(self, mock_model_class, mock_configure):
        """Test handling of API key errors."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("Invalid API key")
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")

        with pytest.raises(GeminiAPIError, match="authentication failed"):
            service.generate_content(prompt="Test")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_network_error(self, mock_model_class, mock_configure):
        """Test handling of network errors."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("Network connection failed")
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")

        with pytest.raises(GeminiAPIError, match="Network error"):
            service.generate_content(prompt="Test")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_generic_error(self, mock_model_class, mock_configure):
        """Test handling of generic errors."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("Unknown error")
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")

        with pytest.raises(GeminiAPIError):
            service.generate_content(prompt="Test")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_empty_response_error(self, mock_model_class, mock_configure):
        """Test handling of empty API response."""
        mock_response = Mock()
        mock_response.text = None

        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")

        # Empty response will be caught by generic handler
        with pytest.raises(GeminiAPIError):
            service.generate_content(prompt="Test")

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_error_logging_no_secrets(self, mock_model_class, mock_configure, caplog):
        """Test that errors are logged without exposing secrets."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API key abc123 is invalid")
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="secret-key-12345")

        try:
            service.generate_content(prompt="Test", correlation_id="test-id")
        except GeminiAPIError:
            pass

        # Check that secret API key is not in logs
        for record in caplog.records:
            assert "secret-key-12345" not in record.message
            assert "secret-key-12345" not in str(record.args)

        # Verify that error was logged
        assert len(caplog.records) > 0


class TestGeminiServiceOutputNormalization:
    """Tests for output normalization."""

    def test_normalize_output_strips_whitespace(self):
        """Test that normalization strips leading/trailing whitespace."""
        result = GeminiService._normalize_output("  test content  ")
        assert result == "test content"

    def test_normalize_output_unix_line_endings(self):
        """Test that normalization converts to Unix line endings."""
        result = GeminiService._normalize_output("line1\r\nline2\rline3\n")
        assert "\r\n" not in result
        assert "\r" not in result
        assert result == "line1\nline2\nline3"

    def test_normalize_output_excessive_blank_lines(self):
        """Test that normalization removes excessive blank lines."""
        result = GeminiService._normalize_output("line1\n\n\n\nline2")
        assert result == "line1\n\nline2"

    def test_normalize_output_empty_string(self):
        """Test normalization of empty string."""
        result = GeminiService._normalize_output("")
        assert result == ""

    def test_normalize_output_none(self):
        """Test normalization of None."""
        result = GeminiService._normalize_output(None)
        assert result == ""


class TestGeminiServiceHealthCheck:
    """Tests for health check functionality."""

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_health_check_success(self, mock_model_class, mock_configure):
        """Test successful health check."""
        mock_response = Mock()
        mock_response.text = "OK"

        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")
        health = service.health_check()

        assert health["status"] == "healthy"
        assert health["model"] == "gemini-3-flash-preview"
        assert "latency_ms" in health
        assert "timestamp" in health

    @patch("google.generativeai.configure")
    @patch("google.generativeai.GenerativeModel")
    def test_health_check_failure(self, mock_model_class, mock_configure):
        """Test health check when service is unhealthy."""
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("Service unavailable")
        mock_model_class.return_value = mock_model

        service = GeminiService(api_key="test-key")
        health = service.health_check()

        assert health["status"] == "unhealthy"
        assert health["model"] == "gemini-3-flash-preview"
        assert "error" in health
        assert "timestamp" in health
