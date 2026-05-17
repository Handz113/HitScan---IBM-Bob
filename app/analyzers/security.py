"""
Security vulnerability scanner
"""
import re
from typing import List, Dict, Any
from .base import BaseAnalyzer


class SecurityAnalyzer(BaseAnalyzer):
    """Detect security vulnerabilities in code"""
    
    # Security patterns with severity and CWE mappings
    SECURITY_PATTERNS = {
        'sql_injection': {
            'patterns': [
                r'execute\s*\(\s*["\'].*%s.*["\']',
                r'execute\s*\(\s*f["\'].*\{.*\}.*["\']',
                r'query\s*=\s*f?["\'].*SELECT.*\{.*\}.*["\']',
                r'cursor\.execute\s*\([^?]*\+',
                r'\.raw\s*\([^?]*\+',
            ],
            'message': 'Potential SQL injection vulnerability - use parameterized queries',
            'severity': 'critical',
            'likelihood': 3,
            'cwe': 'CWE-89'
        },
        'hardcoded_secret': {
            'patterns': [
                r'(password|passwd|pwd|secret|token|api_key|apikey)\s*=\s*["\'][^"\']{8,}["\']',
                r'(PASSWORD|SECRET|TOKEN|API_KEY)\s*=\s*["\'][^"\']{8,}["\']',
                r'Authorization\s*:\s*["\']Bearer\s+[A-Za-z0-9\-_]+["\']',
            ],
            'message': 'Hardcoded secret detected - use environment variables',
            'severity': 'high',
            'likelihood': 5,
            'cwe': 'CWE-798'
        },
        'command_injection': {
            'patterns': [
                r'os\.system\s*\([^)]*\+',
                r'subprocess\.(call|run|Popen)\s*\([^)]*\+',
                r'exec\s*\(',
                r'eval\s*\(',
                r'shell\s*=\s*True',
            ],
            'message': 'Potential command injection - avoid shell=True and string concatenation',
            'severity': 'critical',
            'likelihood': 3,
            'cwe': 'CWE-78'
        },
        'xss_vulnerability': {
            'patterns': [
                r'innerHTML\s*=',
                r'document\.write\s*\(',
                r'\.html\s*\([^)]*\+',
                r'dangerouslySetInnerHTML',
            ],
            'message': 'Potential XSS vulnerability - sanitize user input',
            'severity': 'high',
            'likelihood': 4,
            'cwe': 'CWE-79'
        },
        'path_traversal': {
            'patterns': [
                r'open\s*\([^)]*\+.*["\']\.\./',
                r'File\s*\([^)]*\+',
                r'readFile\s*\([^)]*\+',
            ],
            'message': 'Potential path traversal vulnerability - validate file paths',
            'severity': 'high',
            'likelihood': 3,
            'cwe': 'CWE-22'
        },
        'weak_crypto': {
            'patterns': [
                r'hashlib\.md5\s*\(',
                r'hashlib\.sha1\s*\(',
                r'crypto\.createHash\s*\(\s*["\']md5["\']',
                r'MessageDigest\.getInstance\s*\(\s*["\']MD5["\']',
            ],
            'message': 'Weak cryptographic algorithm - use SHA-256 or stronger',
            'severity': 'medium',
            'likelihood': 4,
            'cwe': 'CWE-327'
        },
        'insecure_random': {
            'patterns': [
                r'random\.random\s*\(',
                r'Math\.random\s*\(',
                r'Random\s*\(\s*\)',
            ],
            'message': 'Insecure random number generator - use secrets module for security',
            'severity': 'medium',
            'likelihood': 3,
            'cwe': 'CWE-338'
        },
        'debug_mode': {
            'patterns': [
                r'DEBUG\s*=\s*True',
                r'debug\s*=\s*true',
                r'app\.debug\s*=\s*True',
            ],
            'message': 'Debug mode enabled - disable in production',
            'severity': 'medium',
            'likelihood': 5,
            'cwe': 'CWE-489'
        },
        'insecure_deserialization': {
            'patterns': [
                r'pickle\.loads?\s*\(',
                r'yaml\.load\s*\([^,)]*\)',
                r'JSON\.parse\s*\(',
            ],
            'message': 'Potential insecure deserialization - validate input',
            'severity': 'high',
            'likelihood': 2,
            'cwe': 'CWE-502'
        },
        'missing_authentication': {
            'patterns': [
                r'@app\.route\s*\([^)]*\)\s*\n\s*def\s+\w+',
                r'app\.(get|post|put|delete)\s*\([^)]*\)\s*,?\s*function',
            ],
            'message': 'Endpoint may lack authentication - verify access controls',
            'severity': 'medium',
            'likelihood': 3,
            'cwe': 'CWE-306'
        }
    }
    
    def analyze(self) -> List[Dict[str, Any]]:
        """
        Analyze code for security vulnerabilities
        
        Returns:
            List of security findings
        """
        findings = []
        
        for issue_type, config in self.SECURITY_PATTERNS.items():
            for pattern in config['patterns']:
                findings.extend(self._find_pattern_matches(
                    pattern,
                    issue_type,
                    config['message'],
                    config['severity'],
                    config['likelihood'],
                    config.get('cwe')
                ))
        
        return findings
    
    def _find_pattern_matches(
        self,
        pattern: str,
        issue_type: str,
        message: str,
        severity: str,
        likelihood: int,
        cwe: str = None
    ) -> List[Dict[str, Any]]:
        """
        Find all matches of a security pattern
        
        Args:
            pattern: Regex pattern to search for
            issue_type: Type of security issue
            message: Description message
            severity: Severity level
            likelihood: Likelihood score
            cwe: CWE identifier
            
        Returns:
            List of findings
        """
        findings = []
        
        for i, line in enumerate(self.lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                finding = {
                    'type': issue_type,
                    'line': i,
                    'code': line.strip(),
                    'message': message,
                    'severity': severity,
                    'likelihood': likelihood
                }
                
                if cwe:
                    finding['cwe'] = cwe
                
                findings.append(finding)
        
        return findings

# Made with Bob
