"""Pytest configuration for backend tests."""

import os
import sys

# Set environment variable BEFORE importing anything
os.environ["TEST_DATABASE_URL"] = "sqlite:///:memory:"

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
