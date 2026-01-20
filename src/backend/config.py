"""Configuration module for the GenAI Email & Report Drafting System.

This module provides configuration settings for the Flask application,
with focus on database connection and environment-based configuration.
"""

import os
from datetime import timedelta
from typing import Optional


class Config:
    """Base configuration class with common settings."""

    # Database configuration
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("DATABASE_URL", "postgresql://localhost/genai_email_report")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"

    # Application settings
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # JWT Configuration
    JWT_SECRET_KEY: Optional[str] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=24)
    JWT_ALGORITHM: str = "HS256"

    # Gemini AI Configuration
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
    GEMINI_TIMEOUT: int = int(os.getenv("GEMINI_TIMEOUT", "30"))
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))

    # Rate Limiting Configuration
    RATELIMIT_ENABLED: bool = os.getenv("RATELIMIT_ENABLED", "True").lower() == "true"
    RATELIMIT_STORAGE_URL: str = os.getenv("RATELIMIT_STORAGE_URL", "memory://")
    RATELIMIT_STRATEGY: str = os.getenv("RATELIMIT_STRATEGY", "fixed-window")
    RATELIMIT_DEFAULT: str = "200 per day, 50 per hour"
    RATELIMIT_DOCUMENT_GENERATION: str = "10 per minute"

    # CORS Configuration
    CORS_ALLOWED_ORIGINS: str = os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173",
    )

    # Admin bootstrap (optional, for first-time setup)
    ADMIN_BOOTSTRAP_ENABLED: bool = os.getenv("ADMIN_BOOTSTRAP_ENABLED", "False").lower() == "true"
    ADMIN_BOOTSTRAP_USERNAME: Optional[str] = os.getenv("ADMIN_BOOTSTRAP_USERNAME")
    ADMIN_BOOTSTRAP_EMAIL: Optional[str] = os.getenv("ADMIN_BOOTSTRAP_EMAIL")
    ADMIN_BOOTSTRAP_PASSWORD: Optional[str] = os.getenv("ADMIN_BOOTSTRAP_PASSWORD")


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG: bool = True
    SQLALCHEMY_ECHO: bool = True


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG: bool = False
    SQLALCHEMY_ECHO: bool = False


class TestConfig(Config):
    """Test environment configuration."""

    TESTING: bool = True
    PROPAGATE_EXCEPTIONS: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.getenv("TEST_DATABASE_URL", "postgresql://localhost/genai_email_report_test")
    # Explicitly set JWT secret for testing
    JWT_SECRET_KEY: str = "test-jwt-secret-key-for-testing-only"
    SECRET_KEY: str = "test-secret-key-for-testing-only"

    # Test Gemini configuration (mock API key for testing)
    GEMINI_API_KEY: str = "test-gemini-api-key-for-testing-only"

    # Disable rate limiting for tests by default (can be enabled per test)
    RATELIMIT_ENABLED: bool = os.getenv("TEST_RATELIMIT_ENABLED", "False").lower() == "true"


# Configuration dictionary
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestConfig,
}


def get_config(config_name: str = "development") -> Config:
    """Get configuration object based on environment name.

    Args:
        config_name: Name of the configuration environment

    Returns:
        Configuration object for the specified environment
    """
    return config_by_name.get(config_name, DevelopmentConfig)
