"""
Configuration and fixtures for pytest.
"""

import pytest
import sys
import os

# Add the app directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def sample_content():
    """Sample content for testing."""
    return "This is sample content for testing purposes."

@pytest.fixture
def sample_background():
    """Sample user background for testing."""
    return "software engineer with experience in Python and AI"