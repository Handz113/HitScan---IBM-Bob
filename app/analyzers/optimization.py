"""
Code optimization analyzer
"""
import re
import ast
from typing import List, Dict, Any
from .base import BaseAnalyzer
from .language_parser import LanguageParser


class OptimizationAnalyzer(BaseAnalyzer):
    """Detect code optimization opportunities"""
    
    def analyze(self) -> List[Dict[str, Any]]:
        """
        Analyze code for optimization opportunities
        
        Returns:
            List of optimization findings
        """
        findings = []
        
        # Detect inefficient patterns
        findings.extend(self._detect_inefficient_loops())
        findings.extend(self._detect_redundant_operations())
        findings.extend(self._detect_string_concatenation())
        findings.extend(self._detect_nested_loops())
        
        # Calculate complexity metrics
        findings.extend(self._check_complexity())
        
        return findings
    
    def _detect_inefficient_loops(self) -> List[Dict[str, Any]]:
        """Detect inefficient loop patterns"""
        findings = []
        
        # Python: for i in range(len(items))
        pattern1 = r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\('
        
        # Repeated list access in loop
        pattern2 = r'for.*:\s*\n\s*.*\[\w+\]'
        
        for i, line in enumerate(self.lines, 1):
            if re.search(pattern1, line):
                findings.append({
                    'type': 'inefficient_loop',
                    'line': i,
                    'code': line.strip(),
                    'message': "Use 'for item in items:' instead of indexing",
                    'severity': 'low',
                    'likelihood': 2,
                    'impact': 'performance'
                })
        
        return findings
    
    def _detect_redundant_operations(self) -> List[Dict[str, Any]]:
        """Detect redundant operations"""
        findings = []
        
        patterns = [
            (r'str\s*\(\s*str\s*\(', 'Redundant string conversion'),
            (r'int\s*\(\s*int\s*\(', 'Redundant integer conversion'),
            (r'list\s*\(\s*list\s*\(', 'Redundant list conversion'),
            (r'\.strip\s*\(\s*\)\s*\.strip\s*\(\s*\)', 'Redundant strip() call'),
            (r'\.lower\s*\(\s*\)\s*\.lower\s*\(\s*\)', 'Redundant lower() call'),
        ]
        
        for i, line in enumerate(self.lines, 1):
            for pattern, message in patterns:
                if re.search(pattern, line):
                    findings.append({
                        'type': 'redundant_operation',
                        'line': i,
                        'code': line.strip(),
                        'message': message,
                        'severity': 'low',
                        'likelihood': 3,
                        'impact': 'performance'
                    })
        
        return findings
    
    def _detect_string_concatenation(self) -> List[Dict[str, Any]]:
        """Detect inefficient string concatenation in loops"""
        findings = []
        
        # Look for string concatenation inside loops
        in_loop = False
        loop_start = 0
        
        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()
            
            # Detect loop start
            if re.match(r'(for|while)\s+', stripped):
                in_loop = True
                loop_start = i
            
            # Detect loop end (simplified - checks indentation)
            elif in_loop and line and not line[0].isspace():
                in_loop = False
            
            # Check for string concatenation in loop
            if in_loop and ('+=' in line or '= ' in line and '+' in line):
                if re.search(r'["\'].*\+|.*\+.*["\']', line):
                    findings.append({
                        'type': 'inefficient_string_concat',
                        'line': i,
                        'code': line.strip(),
                        'message': 'Use list append and join() for string concatenation in loops',
                        'severity': 'low',
                        'likelihood': 2,
                        'impact': 'performance'
                    })
        
        return findings
    
    def _detect_nested_loops(self) -> List[Dict[str, Any]]:
        """Detect deeply nested loops (potential O(n²) or worse)"""
        findings = []
        
        loop_depth = 0
        loop_stack = []
        
        for i, line in enumerate(self.lines, 1):
            stripped = line.strip()
            indent = len(line) - len(line.lstrip())
            
            # Detect loop start
            if re.match(r'(for|while)\s+', stripped):
                loop_depth += 1
                loop_stack.append((i, indent))
                
                # Warn about nested loops (depth > 2)
                if loop_depth > 2:
                    findings.append({
                        'type': 'deeply_nested_loop',
                        'line': i,
                        'code': line.strip(),
                        'message': f'Deeply nested loop (depth {loop_depth}) - consider refactoring',
                        'severity': 'medium',
                        'likelihood': 2,
                        'impact': 'performance'
                    })
            
            # Detect loop end (simplified)
            elif loop_stack and indent <= loop_stack[-1][1] and not stripped:
                if loop_depth > 0:
                    loop_depth -= 1
                    loop_stack.pop()
        
        return findings
    
    def _check_complexity(self) -> List[Dict[str, Any]]:
        """Check cyclomatic complexity"""
        findings = []
        
        # Try to use radon for Python
        if self.language == 'python':
            try:
                from radon.complexity import cc_visit
                from radon.metrics import mi_visit
                
                # Calculate cyclomatic complexity
                complexity_results = cc_visit(self.code)
                
                for result in complexity_results:
                    if result.complexity > 10:
                        findings.append({
                            'type': 'high_complexity',
                            'line': result.lineno,
                            'code': f"Function '{result.name}'",
                            'message': f'High cyclomatic complexity ({result.complexity}) - consider refactoring',
                            'severity': 'medium',
                            'likelihood': 3,
                            'impact': 'maintainability'
                        })
                
                # Calculate maintainability index
                mi_results = mi_visit(self.code, multi=True)
                if mi_results and mi_results < 20:
                    findings.append({
                        'type': 'low_maintainability',
                        'line': 1,
                        'code': 'Overall code',
                        'message': f'Low maintainability index ({mi_results:.1f}) - code is hard to maintain',
                        'severity': 'medium',
                        'likelihood': 4,
                        'impact': 'maintainability'
                    })
                    
            except ImportError:
                pass  # Radon not available, skip complexity analysis
            except Exception:
                pass  # Parsing error, skip
        
        # Simple heuristic: count decision points
        decision_keywords = ['if', 'elif', 'else', 'for', 'while', 'case', 'catch', '&&', '||']
        decision_count = sum(
            line.count(keyword) for line in self.lines for keyword in decision_keywords
        )
        
        if decision_count > 20:
            findings.append({
                'type': 'high_decision_count',
                'line': 1,
                'code': 'Overall code',
                'message': f'High number of decision points ({decision_count}) - consider simplifying',
                'severity': 'low',
                'likelihood': 3,
                'impact': 'maintainability'
            })
        
        return findings

# Made with Bob
