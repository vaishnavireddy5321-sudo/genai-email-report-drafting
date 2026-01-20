"""Unit tests for PromptEngine module."""

import pytest
from services.prompt_engine import PromptEngine, ReportStructureType, ToneType


class TestPromptEngineValidation:
    """Tests for input validation methods."""

    def test_validate_input_valid(self):
        """Test validation with valid input."""
        result = PromptEngine.validate_input("  Test input  ", "test")
        assert result == "Test input"

    def test_validate_input_empty_string(self):
        """Test validation with empty string."""
        with pytest.raises(ValueError, match="test cannot be empty"):
            PromptEngine.validate_input("", "test")

    def test_validate_input_whitespace_only(self):
        """Test validation with whitespace only."""
        with pytest.raises(ValueError, match="test cannot be empty"):
            PromptEngine.validate_input("   ", "test")

    def test_validate_input_max_length(self):
        """Test validation with input exceeding max length."""
        long_input = "x" * (PromptEngine.MAX_INPUT_LENGTH + 1)
        with pytest.raises(ValueError, match="exceeds maximum length"):
            PromptEngine.validate_input(long_input, "test")

    def test_validate_tone_valid_professional(self):
        """Test tone validation with valid professional tone."""
        result = PromptEngine.validate_tone("professional")
        assert result == "professional"

    def test_validate_tone_case_insensitive(self):
        """Test tone validation is case insensitive."""
        result = PromptEngine.validate_tone("PROFESSIONAL")
        assert result == "professional"

    def test_validate_tone_invalid(self):
        """Test tone validation with invalid tone."""
        with pytest.raises(ValueError, match="Invalid tone"):
            PromptEngine.validate_tone("invalid_tone")

    def test_validate_structure_valid(self):
        """Test structure validation with valid structure."""
        result = PromptEngine.validate_structure("detailed")
        assert result == "detailed"

    def test_validate_structure_none(self):
        """Test structure validation with None."""
        result = PromptEngine.validate_structure(None)
        assert result is None

    def test_validate_structure_invalid(self):
        """Test structure validation with invalid structure."""
        with pytest.raises(ValueError, match="Invalid structure"):
            PromptEngine.validate_structure("invalid_structure")


class TestEmailPromptGeneration:
    """Tests for email prompt generation."""

    def test_build_email_prompt_basic(self):
        """Test basic email prompt generation."""
        prompt = PromptEngine.build_email_prompt(context="Request a meeting", tone="professional")

        # Verify essential components are present
        assert "professional communication assistant" in prompt
        assert "Request a meeting" in prompt
        assert "Task" in prompt
        assert "Tone" in prompt
        assert "Format Requirements" in prompt
        assert "greeting" in prompt.lower()
        assert "closing" in prompt.lower()

    def test_build_email_prompt_with_recipient(self):
        """Test email prompt with recipient information."""
        prompt = PromptEngine.build_email_prompt(
            context="Request budget approval", recipient="Finance Manager", tone="formal"
        )

        assert "Request budget approval" in prompt
        assert "Finance Manager" in prompt
        assert "Recipient" in prompt
        assert "formal" in prompt.lower()

    def test_build_email_prompt_with_subject(self):
        """Test email prompt with subject."""
        prompt = PromptEngine.build_email_prompt(
            context="Announce new policy", subject="Updated Leave Policy", tone="professional"
        )

        assert "Announce new policy" in prompt
        assert "Updated Leave Policy" in prompt
        assert "Subject/Topic" in prompt

    def test_build_email_prompt_all_parameters(self):
        """Test email prompt with all parameters."""
        prompt = PromptEngine.build_email_prompt(
            context="Schedule team building event",
            recipient="All Team Members",
            subject="Team Outing Next Month",
            tone="friendly",
        )

        assert "Schedule team building event" in prompt
        assert "All Team Members" in prompt
        assert "Team Outing Next Month" in prompt
        assert "friendly" in prompt.lower()

    def test_build_email_prompt_tone_guidance(self):
        """Test that different tones produce different guidance."""
        professional_prompt = PromptEngine.build_email_prompt(context="Test context", tone="professional")

        casual_prompt = PromptEngine.build_email_prompt(context="Test context", tone="casual")

        formal_prompt = PromptEngine.build_email_prompt(context="Test context", tone="formal")

        # Each should have distinct tone guidance
        assert "professional" in professional_prompt.lower()
        assert "casual" in casual_prompt.lower()
        assert "formal" in formal_prompt.lower()

        # They should not all be identical
        assert professional_prompt != casual_prompt
        assert casual_prompt != formal_prompt

    def test_build_email_prompt_empty_context(self):
        """Test email prompt with empty context."""
        with pytest.raises(ValueError):
            PromptEngine.build_email_prompt(context="")

    def test_build_email_prompt_invalid_tone(self):
        """Test email prompt with invalid tone."""
        with pytest.raises(ValueError):
            PromptEngine.build_email_prompt(context="Test", tone="invalid")

    def test_build_email_prompt_stability(self):
        """Test that same inputs produce same output (prompt stability)."""
        prompt1 = PromptEngine.build_email_prompt(
            context="Test context", recipient="Manager", subject="Test subject", tone="professional"
        )

        prompt2 = PromptEngine.build_email_prompt(
            context="Test context", recipient="Manager", subject="Test subject", tone="professional"
        )

        assert prompt1 == prompt2


class TestReportPromptGeneration:
    """Tests for report prompt generation."""

    def test_build_report_prompt_basic(self):
        """Test basic report prompt generation."""
        prompt = PromptEngine.build_report_prompt(topic="Q4 Sales Analysis", tone="professional")

        # Verify essential components are present
        assert "professional communication assistant" in prompt
        assert "Q4 Sales Analysis" in prompt
        assert "Task" in prompt
        assert "Tone" in prompt
        assert "Structure" in prompt
        assert "Format Requirements" in prompt
        assert "section headings" in prompt.lower()

    def test_build_report_prompt_with_key_points(self):
        """Test report prompt with key points."""
        prompt = PromptEngine.build_report_prompt(
            topic="Market Research Report",
            key_points="Focus on competitor analysis and market trends",
            tone="professional",
        )

        assert "Market Research Report" in prompt
        assert "competitor analysis and market trends" in prompt
        assert "Key Points to Address" in prompt

    def test_build_report_prompt_executive_summary(self):
        """Test report prompt with executive summary structure."""
        prompt = PromptEngine.build_report_prompt(
            topic="Project Status Update", structure="executive_summary", tone="professional"
        )

        assert "Project Status Update" in prompt
        assert "executive summary" in prompt.lower()
        assert "concise" in prompt.lower()

    def test_build_report_prompt_detailed_structure(self):
        """Test report prompt with detailed structure."""
        prompt = PromptEngine.build_report_prompt(
            topic="Annual Performance Review", structure="detailed", tone="formal"
        )

        assert "Annual Performance Review" in prompt
        assert "detailed" in prompt.lower()
        assert "comprehensive" in prompt.lower()

    def test_build_report_prompt_bullet_points(self):
        """Test report prompt with bullet points structure."""
        prompt = PromptEngine.build_report_prompt(
            topic="Project Milestones", structure="bullet_points", tone="professional"
        )

        assert "Project Milestones" in prompt
        assert "bullet" in prompt.lower()

    def test_build_report_prompt_all_parameters(self):
        """Test report prompt with all parameters."""
        prompt = PromptEngine.build_report_prompt(
            topic="Security Audit Results",
            key_points="Identify vulnerabilities and recommendations",
            tone="formal",
            structure="detailed",
        )

        assert "Security Audit Results" in prompt
        assert "vulnerabilities and recommendations" in prompt
        assert "formal" in prompt.lower()
        assert "detailed" in prompt.lower()

    def test_build_report_prompt_structure_differences(self):
        """Test that different structures produce different guidance."""
        exec_prompt = PromptEngine.build_report_prompt(topic="Test", structure="executive_summary")

        detailed_prompt = PromptEngine.build_report_prompt(topic="Test", structure="detailed")

        bullet_prompt = PromptEngine.build_report_prompt(topic="Test", structure="bullet_points")

        # Each should be distinct
        assert exec_prompt != detailed_prompt
        assert detailed_prompt != bullet_prompt
        assert exec_prompt != bullet_prompt

    def test_build_report_prompt_empty_topic(self):
        """Test report prompt with empty topic."""
        with pytest.raises(ValueError):
            PromptEngine.build_report_prompt(topic="")

    def test_build_report_prompt_invalid_tone(self):
        """Test report prompt with invalid tone."""
        with pytest.raises(ValueError):
            PromptEngine.build_report_prompt(topic="Test", tone="invalid")

    def test_build_report_prompt_invalid_structure(self):
        """Test report prompt with invalid structure."""
        with pytest.raises(ValueError):
            PromptEngine.build_report_prompt(topic="Test", structure="invalid")

    def test_build_report_prompt_default_structure(self):
        """Test that default structure is used when not specified."""
        prompt = PromptEngine.build_report_prompt(topic="Test Report")

        # Should include detailed structure by default
        assert "detailed" in prompt.lower()

    def test_build_report_prompt_stability(self):
        """Test that same inputs produce same output (prompt stability)."""
        prompt1 = PromptEngine.build_report_prompt(
            topic="Test Report", key_points="Key point 1", tone="professional", structure="detailed"
        )

        prompt2 = PromptEngine.build_report_prompt(
            topic="Test Report", key_points="Key point 1", tone="professional", structure="detailed"
        )

        assert prompt1 == prompt2


class TestPromptEngineEnums:
    """Tests for enum types."""

    def test_tone_type_values(self):
        """Test that all expected tone types exist."""
        expected_tones = ["professional", "casual", "formal", "friendly"]
        actual_tones = [t.value for t in ToneType]

        assert set(expected_tones) == set(actual_tones)

    def test_report_structure_type_values(self):
        """Test that all expected structure types exist."""
        expected_structures = ["executive_summary", "detailed", "bullet_points"]
        actual_structures = [s.value for s in ReportStructureType]

        assert set(expected_structures) == set(actual_structures)
