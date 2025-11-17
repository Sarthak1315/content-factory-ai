"""
Pytest configuration and shared fixtures
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope="session")
def test_config():
    """Test configuration"""
    return {
        'model': 'gemini-2.0-flash-exp',
        'test_topic': 'AI Trends in 2025',
        'test_session_id': 'test_session_001'
    }