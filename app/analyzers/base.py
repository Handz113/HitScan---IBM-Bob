"""
Base analyzer class
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseAnalyzer(ABC):
    """Base class for all code analyzers"""
    
    def __init__(self, code: str, language: str):
        """
        Initialize analyzer
        
        Args:
            code: Code snippet to analyze
            language: Programming language
        """
        self.code = code
        self.language = language
        self.lines = code.split('\n')
    
    @abstractmethod
    def analyze(self) -> List[Dict[str, Any]]:
        """
        Analyze code and return findings
        
        Returns:
            List of findings with type, line, code, message, severity, likelihood
        """
        pass
    
    def get_line(self, line_num: int) -> str:
        """
        Get code at specific line number
        
        Args:
            line_num: Line number (1-based)
            
        Returns:
            Code at that line or empty string
        """
        if 0 < line_num <= len(self.lines):
            return self.lines[line_num - 1].strip()
        return ""
    
    def get_line_range(self, start: int, end: int) -> str:
        """
        Get code in a line range
        
        Args:
            start: Start line (1-based, inclusive)
            end: End line (1-based, inclusive)
            
        Returns:
            Code in that range
        """
        if start < 1 or end > len(self.lines) or start > end:
            return ""
        return '\n'.join(self.lines[start-1:end])

# Made with Bob
