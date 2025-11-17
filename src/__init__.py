"""
Content Factory AI - Multi-Agent Content Creation System
Built for Google/Kaggle 5-Day AI Agents Intensive Capstone Project

A sophisticated multi-agent system that researches, writes, fact-checks,
and optimizes content across multiple platforms.
"""

__version__ = "1.0.0"
__author__ = "Sarthak Patel"
__email__ = "sarthakpatel1315@gmail.com"

# Core components
from .orchestrator import ContentFactoryOrchestrator

# Expose main components
__all__ = [
    'ContentFactoryOrchestrator',
]