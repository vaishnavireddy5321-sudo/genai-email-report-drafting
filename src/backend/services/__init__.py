"""Services package for GenAI Email & Report Drafting System.

This package contains service layer modules for AI integration
and business logic processing.
"""

from .gemini_service import GeminiService
from .prompt_engine import PromptEngine

__all__ = ["PromptEngine", "GeminiService"]
