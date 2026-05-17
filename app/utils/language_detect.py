"""
Language detection utility
"""
import re
from typing import Optional


def detect_language(code: str) -> Optional[str]:
    """
    Detect programming language from code snippet
    
    Args:
        code: Code snippet to analyze
        
    Returns:
        Detected language or None
    """
    code = code.strip()
    
    # Python indicators
    python_patterns = [
        r'^\s*def\s+\w+\s*\(',
        r'^\s*class\s+\w+',
        r'^\s*import\s+\w+',
        r'^\s*from\s+\w+\s+import',
        r'^\s*@\w+',
        r':\s*$',  # Colon at end of line (common in Python)
        r'^\s*if\s+.*:\s*$',
        r'^\s*for\s+.*:\s*$',
        r'^\s*while\s+.*:\s*$',
    ]
    
    # JavaScript indicators
    javascript_patterns = [
        r'^\s*function\s+\w+\s*\(',
        r'^\s*const\s+\w+\s*=',
        r'^\s*let\s+\w+\s*=',
        r'^\s*var\s+\w+\s*=',
        r'=>',  # Arrow function
        r'console\.log',
        r'require\s*\(',
        r'module\.exports',
        r'^\s*class\s+\w+\s*{',
    ]
    
    # Java indicators
    java_patterns = [
        r'^\s*public\s+class\s+\w+',
        r'^\s*private\s+\w+\s+\w+',
        r'^\s*public\s+static\s+void\s+main',
        r'^\s*import\s+java\.',
        r'System\.out\.println',
        r'^\s*@Override',
        r'^\s*public\s+\w+\s+\w+\s*\(',
    ]
    
    # Count matches for each language
    python_score = sum(1 for pattern in python_patterns if re.search(pattern, code, re.MULTILINE))
    javascript_score = sum(1 for pattern in javascript_patterns if re.search(pattern, code, re.MULTILINE))
    java_score = sum(1 for pattern in java_patterns if re.search(pattern, code, re.MULTILINE))
    
    # Return language with highest score
    scores = {
        'python': python_score,
        'javascript': javascript_score,
        'java': java_score
    }
    
    max_score = max(scores.values())
    if max_score == 0:
        return None
    
    return max(scores, key=scores.get)

# Made with Bob
