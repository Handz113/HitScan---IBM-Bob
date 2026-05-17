"""
Risk scoring calculator
"""
from typing import Dict, List, Any


class RiskCalculator:
    """Calculate risk scores from findings"""
    
    # Severity to numeric mapping
    SEVERITY_MAP = {
        'critical': 5,
        'high': 4,
        'medium': 3,
        'low': 2,
        'info': 1
    }
    
    # Risk level thresholds (severity × likelihood)
    RISK_THRESHOLDS = {
        'critical': 16,  # 16-25
        'high': 12,      # 12-15
        'medium': 6,     # 6-11
        'low': 0         # 1-5
    }
    
    @staticmethod
    def calculate_risk_score(severity: str, likelihood: int) -> int:
        """
        Calculate risk score from severity and likelihood
        
        Args:
            severity: Severity level (critical/high/medium/low)
            likelihood: Likelihood score (1-5)
            
        Returns:
            Risk score (1-25)
        """
        severity_value = RiskCalculator.SEVERITY_MAP.get(severity.lower(), 1)
        return severity_value * likelihood
    
    @staticmethod
    def get_risk_level(risk_score: int) -> str:
        """
        Get risk level from risk score
        
        Args:
            risk_score: Calculated risk score
            
        Returns:
            Risk level (CRITICAL/HIGH/MEDIUM/LOW)
        """
        if risk_score >= RiskCalculator.RISK_THRESHOLDS['critical']:
            return 'CRITICAL'
        elif risk_score >= RiskCalculator.RISK_THRESHOLDS['high']:
            return 'HIGH'
        elif risk_score >= RiskCalculator.RISK_THRESHOLDS['medium']:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    @staticmethod
    def get_color_for_risk(risk_level: str) -> str:
        """
        Get color code for risk level
        
        Args:
            risk_level: Risk level
            
        Returns:
            Hex color code
        """
        colors = {
            'CRITICAL': '#dc2626',  # Red
            'HIGH': '#f59e0b',      # Orange
            'MEDIUM': '#fbbf24',    # Yellow
            'LOW': '#10b981'        # Green
        }
        return colors.get(risk_level, '#6b7280')
    
    @staticmethod
    def calculate_overall_risk(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate overall risk metrics from all findings
        
        Args:
            findings: List of all findings
            
        Returns:
            Dictionary with risk metrics
        """
        if not findings:
            return {
                'risk_score': 0.0,
                'risk_level': 'LOW',
                'summary': {
                    'critical': 0,
                    'high': 0,
                    'medium': 0,
                    'low': 0,
                    'total_issues': 0
                }
            }
        
        # Count findings by severity
        summary = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0,
            'total_issues': len(findings)
        }
        
        total_risk = 0
        
        for finding in findings:
            severity = finding.get('severity', 'low').lower()
            likelihood = finding.get('likelihood', 1)
            
            # Count by severity
            if severity in summary:
                summary[severity] += 1
            
            # Add to total risk
            risk_score = RiskCalculator.calculate_risk_score(severity, likelihood)
            total_risk += risk_score
        
        # Calculate average risk score
        avg_risk_score = total_risk / len(findings) if findings else 0
        
        # Determine overall risk level
        # Weight critical and high issues more heavily
        weighted_score = (
            summary['critical'] * 5 +
            summary['high'] * 3 +
            summary['medium'] * 2 +
            summary['low'] * 1
        )
        
        if summary['critical'] > 0:
            overall_level = 'CRITICAL'
        elif summary['high'] > 2 or weighted_score > 15:
            overall_level = 'HIGH'
        elif summary['medium'] > 3 or weighted_score > 8:
            overall_level = 'MEDIUM'
        else:
            overall_level = 'LOW'
        
        return {
            'risk_score': round(avg_risk_score, 1),
            'risk_level': overall_level,
            'summary': summary
        }

# Made with Bob
