"""Prompt Engine module for constructing AI prompts.

This module provides a structured approach to building prompts
for email and report generation using Google Gemini LLM.
"""

from enum import Enum
from typing import Optional


class ToneType(str, Enum):
    """Enumeration of valid tone types for content generation."""

    PROFESSIONAL = "professional"
    CASUAL = "casual"
    FORMAL = "formal"
    FRIENDLY = "friendly"


class ReportStructureType(str, Enum):
    """Enumeration of valid report structure types."""

    EXECUTIVE_SUMMARY = "executive_summary"
    DETAILED = "detailed"
    BULLET_POINTS = "bullet_points"


class PromptEngine:
    """Engine for constructing structured prompts for AI content generation.

    This class provides methods to build well-formed prompts with proper
    role definition, task framing, tone constraints, and format guidance.
    All prompts are project-specific and follow zero-copy policy.
    """

    # Role definition for the AI assistant
    ROLE_DEFINITION = (
        "You are an expert professional communication assistant specializing in "
        "corporate and academic writing. Your task is to generate clear, well-structured, "
        "and contextually appropriate content for business and academic environments."
    )

    # Maximum input length to prevent excessive API usage
    MAX_INPUT_LENGTH = 5000

    @staticmethod
    def validate_input(user_input: str, field_name: str = "input") -> str:
        """Validate and sanitize user input.

        Args:
            user_input: Raw user input to validate
            field_name: Name of the field for error messages

        Returns:
            Validated and trimmed input string

        Raises:
            ValueError: If input is empty or exceeds maximum length
        """
        if not user_input or not user_input.strip():
            raise ValueError(f"{field_name} cannot be empty")

        trimmed = user_input.strip()

        if len(trimmed) > PromptEngine.MAX_INPUT_LENGTH:
            raise ValueError(f"{field_name} exceeds maximum length of {PromptEngine.MAX_INPUT_LENGTH} characters")

        return trimmed

    @staticmethod
    def validate_tone(tone: str) -> str:
        """Validate tone parameter.

        Args:
            tone: Tone type to validate

        Returns:
            Validated tone string

        Raises:
            ValueError: If tone is not valid
        """
        try:
            return ToneType(tone.lower()).value
        except (ValueError, AttributeError):
            valid_tones = [t.value for t in ToneType]
            raise ValueError(f"Invalid tone '{tone}'. Must be one of: {', '.join(valid_tones)}")

    @staticmethod
    def validate_structure(structure: Optional[str]) -> Optional[str]:
        """Validate report structure parameter.

        Args:
            structure: Structure type to validate (optional)

        Returns:
            Validated structure string or None

        Raises:
            ValueError: If structure is provided but not valid
        """
        if structure is None:
            return None

        try:
            return ReportStructureType(structure.lower()).value
        except (ValueError, AttributeError):
            valid_structures = [s.value for s in ReportStructureType]
            raise ValueError(f"Invalid structure '{structure}'. Must be one of: {', '.join(valid_structures)}")

    @classmethod
    def build_email_prompt(
        cls, context: str, recipient: Optional[str] = None, subject: Optional[str] = None, tone: str = "professional"
    ) -> str:
        """Build a structured prompt for email generation.

        This method constructs a comprehensive prompt that guides the AI to
        generate a professional email with appropriate structure and tone.

        Args:
            context: The main content or purpose of the email
            recipient: Optional recipient information (e.g., "manager", "client")
            subject: Optional subject line or topic
            tone: Desired tone (professional, casual, formal, friendly)

        Returns:
            Complete prompt string for Gemini API

        Raises:
            ValueError: If inputs are invalid
        """
        # Validate inputs
        context = cls.validate_input(context, "context")
        tone = cls.validate_tone(tone)

        # Build prompt components
        prompt_parts = [cls.ROLE_DEFINITION]

        # Task definition
        prompt_parts.append(
            "\n\n## Task\n"
            "Generate a professional email based on the provided context. "
            "The email should be clear, concise, and appropriate for workplace communication."
        )

        # Tone constraints
        tone_guidance = {
            ToneType.PROFESSIONAL: (
                "Use a professional and respectful tone. Maintain formality while being approachable. "
                "Avoid overly casual language or slang."
            ),
            ToneType.CASUAL: (
                "Use a casual and friendly tone while maintaining professionalism. "
                "It's acceptable to be conversational, but remain respectful."
            ),
            ToneType.FORMAL: (
                "Use a formal and reserved tone. Maintain proper business etiquette and avoid contractions. "
                "Use formal salutations and closings."
            ),
            ToneType.FRIENDLY: (
                "Use a warm and friendly tone while remaining professional. "
                "Show enthusiasm and approachability in your language."
            ),
        }

        prompt_parts.append(f"\n\n## Tone\n{tone_guidance[ToneType(tone)]}")

        # Format requirements
        prompt_parts.append(
            "\n\n## Format Requirements\n"
            "- Include an appropriate greeting\n"
            "- Structure the content in clear paragraphs\n"
            "- Use proper spacing between sections\n"
            "- Include a professional closing\n"
            "- Do NOT include a subject line in the body (it will be handled separately)"
        )

        # Context and optional details
        prompt_parts.append(f"\n\n## Context\n{context}")

        if recipient:
            recipient = cls.validate_input(recipient, "recipient")
            prompt_parts.append(f"\n\n## Recipient\n{recipient}")

        if subject:
            subject = cls.validate_input(subject, "subject")
            prompt_parts.append(f"\n\n## Subject/Topic\n{subject}")

        # Final instruction
        prompt_parts.append(
            "\n\n## Output\n" "Generate the email content now. Include only the email body without subject line."
        )

        return "".join(prompt_parts)

    @classmethod
    def build_report_prompt(
        cls, topic: str, key_points: Optional[str] = None, tone: str = "professional", structure: str = "detailed"
    ) -> str:
        """Build a structured prompt for report generation.

        This method constructs a comprehensive prompt that guides the AI to
        generate a professional report with appropriate structure and depth.

        Args:
            topic: The main topic or title of the report
            key_points: Optional key points or data to include
            tone: Desired tone (professional, formal)
            structure: Report structure type (executive_summary, detailed, bullet_points)

        Returns:
            Complete prompt string for Gemini API

        Raises:
            ValueError: If inputs are invalid
        """
        # Validate inputs
        topic = cls.validate_input(topic, "topic")
        tone = cls.validate_tone(tone)
        structure = cls.validate_structure(structure) or ReportStructureType.DETAILED.value

        # Build prompt components
        prompt_parts = [cls.ROLE_DEFINITION]

        # Task definition
        prompt_parts.append(
            "\n\n## Task\n"
            "Generate a comprehensive report based on the provided topic and requirements. "
            "The report should be well-organized, informative, and suitable for professional presentation."
        )

        # Tone constraints (reports typically use professional or formal)
        tone_guidance = {
            ToneType.PROFESSIONAL: (
                "Use a professional and objective tone. Present information clearly and factually. "
                "Maintain consistency throughout the report."
            ),
            ToneType.FORMAL: (
                "Use a formal and academic tone. Employ precise language and avoid contractions. "
                "Structure content with proper headings and logical flow."
            ),
            ToneType.CASUAL: (
                "Use a casual yet informative tone. Present information in an accessible way "
                "while maintaining credibility and clarity."
            ),
            ToneType.FRIENDLY: (
                "Use an approachable and engaging tone. Make complex information accessible "
                "while maintaining professionalism and accuracy."
            ),
        }

        prompt_parts.append(f"\n\n## Tone\n{tone_guidance[ToneType(tone)]}")

        # Structure guidance
        structure_guidance = {
            ReportStructureType.EXECUTIVE_SUMMARY: (
                "- Start with a concise executive summary (2-3 paragraphs)\n"
                "- Highlight key findings and recommendations\n"
                "- Focus on high-level insights and actionable conclusions\n"
                "- Keep the overall length concise (500-800 words)"
            ),
            ReportStructureType.DETAILED: (
                "- Include a brief introduction\n"
                "- Organize content into clear sections with headings\n"
                "- Provide detailed analysis and supporting information\n"
                "- Include a conclusion section summarizing key takeaways\n"
                "- Aim for comprehensive coverage (1000-1500 words)"
            ),
            ReportStructureType.BULLET_POINTS: (
                "- Use bullet points for main ideas\n"
                "- Organize into logical categories or sections\n"
                "- Keep each point concise and focused\n"
                "- Use sub-bullets for supporting details where appropriate\n"
                "- Prioritize clarity and scannability"
            ),
        }

        prompt_parts.append(f"\n\n## Structure\n{structure_guidance[ReportStructureType(structure)]}")

        # Format requirements
        prompt_parts.append(
            "\n\n## Format Requirements\n"
            "- Use clear section headings (use ## for main sections)\n"
            "- Maintain consistent formatting throughout\n"
            "- Use proper paragraph spacing\n"
            "- Ensure logical flow between sections\n"
            "- Do NOT include page numbers or date stamps"
        )

        # Topic and optional details
        prompt_parts.append(f"\n\n## Topic\n{topic}")

        if key_points:
            key_points = cls.validate_input(key_points, "key_points")
            prompt_parts.append(f"\n\n## Key Points to Address\n{key_points}")

        # Final instruction
        prompt_parts.append(
            "\n\n## Output\n"
            "Generate the complete report now. Include appropriate headings and sections "
            "based on the structure specified above."
        )

        return "".join(prompt_parts)
