"""
Dataframe Package - A simple CSV data processing library.

This package provides tools for reading, analyzing, and manipulating CSV data.
"""

# Import the main class and submodules
from . import stats
from .dataframe import Dataframe

# Define public API
__all__ = ["Dataframe", "stats"]

# Package metadata
__version__ = "1.0.0"
__author__ = "fa3el kheer"
