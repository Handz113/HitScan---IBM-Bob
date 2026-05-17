"""
Dead code detection analyzer
"""
import re
import ast
from typing import List, Dict, Any, Set
from .base import BaseAnalyzer
from .language_parser import LanguageParser


class DeadCodeAnalyzer(BaseAnalyzer):
    """Detect dead code and obsolete elements"""
    
    def analyze(self) -> List[Dict[str, Any]]:
        """
        Analyze code for dead code issues
        
        Returns:
            List of dead code findings
        """
        findings = []
        
        # Parse code
        parser = LanguageParser(self.code, self.language)
        if not parser.parse():
            # Fallback to regex-based analysis if parsing fails
            return self._regex_based_analysis()
        
        # Detect unused variables
        findings.extend(self._detect_unused_variables(parser))
        
        # Detect unreachable code
        findings.extend(self._detect_unreachable_code())
        
        # Detect unused imports (Python only)
        if self.language == 'python':
            findings.extend(self._detect_unused_imports(parser))
        
        # Detect unused functions
        findings.extend(self._detect_unused_functions(parser))
        
        return findings
    
    def _detect_unused_variables(self, parser: LanguageParser) -> List[Dict[str, Any]]:
        """Detect variables that are assigned but never used"""
        findings = []
        variables = parser.get_variables()
        
        for var in variables:
            var_name = var['name']
            line_num = var['line']
            
            # Count occurrences of variable name in code
            occurrences = len(re.findall(r'\b' + re.escape(var_name) + r'\b', self.code))
            
            # If only appears once (the assignment), it's unused
            if occurrences == 1:
                findings.append({
                    'type': 'unused_variable',
                    'line': line_num,
                    'code': self.get_line(line_num),
                    'message': f"Variable '{var_name}' is assigned but never used",
                    'severity': 'low',
                    'likelihood': 5
                })
        
        return findings
    
    def _detect_unreachable_code(self) -> List[Dict[str, Any]]:
        """Detect code that can never be executed"""
        findings = []
        
        # Pattern: code after return/break/continue/raise
        return_keywords = ['return', 'break', 'continue', 'raise', 'throw']
        
        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()
            
            # Check if line contains a return/break/continue/raise
            for keyword in return_keywords:
                if re.match(rf'^\s*{keyword}\b', stripped):
                    # Check if there's code after this (not just closing braces/comments)
                    if i < len(self.lines):
                        next_line = self.lines[i].strip()
                        
                        # Skip empty lines and comments
                        if next_line and not next_line.startswith(('#', '//', '/*', '*', '}')):
                            # Check indentation - unreachable if same or greater indent
                            current_indent = len(line) - len(line.lstrip())
                            next_indent = len(self.lines[i]) - len(self.lines[i].lstrip())
                            
                            if next_indent >= current_indent:
                                findings.append({
                                    'type': 'unreachable_code',
                                    'line': i + 1,
                                    'code': next_line,
                                    'message': f"Code after '{keyword}' statement is unreachable",
                                    'severity': 'medium',
                                    'likelihood': 5
                                })
                    break
        
        return findings
    
    def _detect_unused_imports(self, parser: LanguageParser) -> List[Dict[str, Any]]:
        """Detect unused import statements (Python only)"""
        findings = []
        imports = parser.get_imports()
        
        for imp in imports:
            import_name = imp['name']
            line_num = imp['line']
            
            # Skip if empty
            if not import_name:
                continue
            
            # Get base module name
            base_name = import_name.split('.')[0]
            
            # Count occurrences (excluding the import line itself)
            code_without_import = '\n'.join([
                line for i, line in enumerate(self.lines, 1) if i != line_num
            ])
            
            occurrences = len(re.findall(r'\b' + re.escape(base_name) + r'\b', code_without_import))
            
            if occurrences == 0:
                findings.append({
                    'type': 'unused_import',
                    'line': line_num,
                    'code': self.get_line(line_num),
                    'message': f"Import '{import_name}' is never used",
                    'severity': 'low',
                    'likelihood': 4
                })
        
        return findings
    
    def _detect_unused_functions(self, parser: LanguageParser) -> List[Dict[str, Any]]:
        """Detect functions that are defined but never called"""
        findings = []
        functions = parser.get_functions()
        
        for func in functions:
            func_name = func['name']
            line_num = func['line']
            
            # Skip special methods and main functions
            if func_name in ['main', '__init__', '__str__', '__repr__']:
                continue
            if func_name.startswith('__') and func_name.endswith('__'):
                continue
            
            # Count calls to this function (excluding the definition)
            call_pattern = rf'\b{re.escape(func_name)}\s*\('
            calls = len(re.findall(call_pattern, self.code))
            
            # Subtract 1 for the definition itself
            if calls <= 1:
                findings.append({
                    'type': 'unused_function',
                    'line': line_num,
                    'code': self.get_line(line_num),
                    'message': f"Function '{func_name}' is defined but never called",
                    'severity': 'low',
                    'likelihood': 3
                })
        
        return findings
    
    def _regex_based_analysis(self) -> List[Dict[str, Any]]:
        """Fallback regex-based analysis when AST parsing fails"""
        findings = []
        
        # Simple pattern matching for common dead code
        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()
            
            # Detect commented-out code
            if re.match(r'^(#|//)\s*(def|function|class|if|for|while)', stripped):
                findings.append({
                    'type': 'commented_code',
                    'line': i,
                    'code': stripped,
                    'message': "Commented-out code should be removed",
                    'severity': 'low',
                    'likelihood': 3
                })
        
        return findings

# Made with Bob
