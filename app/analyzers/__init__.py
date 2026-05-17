"""
Code analyzers
"""
from .base import BaseAnalyzer
from .dead_code import DeadCodeAnalyzer
from .security import SecurityAnalyzer
from .optimization import OptimizationAnalyzer
from .language_parser import LanguageParser

__all__ = [
    'BaseAnalyzer',
    'DeadCodeAnalyzer',
    'SecurityAnalyzer',
    'OptimizationAnalyzer',
    'LanguageParser'
]

# Made with Bob
