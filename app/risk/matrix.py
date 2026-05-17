"""
Risk matrix generator
"""
from typing import List, Dict, Any
from .calculator import RiskCalculator


class RiskMatrixGenerator:
    """Generate risk matrix visualization data"""
    
    @staticmethod
    def generate_matrix(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate risk matrix from findings
        
        Args:
            findings: List of all findings
            
        Returns:
            Risk matrix data structure
        """
        # Calculate overall risk
        overall_risk = RiskCalculator.calculate_overall_risk(findings)
        
        # Generate matrix data points
        matrix_data = []
        
        for idx, finding in enumerate(findings):
            severity = finding.get('severity', 'low')
            likelihood = finding.get('likelihood', 1)
            risk_score = RiskCalculator.calculate_risk_score(severity, likelihood)
            risk_level = RiskCalculator.get_risk_level(risk_score)
            
            # Determine category
            finding_type = finding.get('type', 'unknown')
            if 'security' in finding_type or finding.get('cwe'):
                category = 'security'
            elif 'dead' in finding_type or 'unused' in finding_type or 'unreachable' in finding_type:
                category = 'dead_code'
            else:
                category = 'optimization'
            
            # Create matrix point
            matrix_point = {
                'id': f"finding-{idx + 1}",
                'title': finding.get('message', 'Unknown issue')[:50],
                'severity': RiskCalculator.SEVERITY_MAP.get(severity.lower(), 1),
                'likelihood': likelihood,
                'risk_score': risk_score,
                'category': category,
                'color': RiskCalculator.get_color_for_risk(risk_level)
            }
            
            matrix_data.append(matrix_point)
        
        # Generate visualization config
        visualization = {
            'chart_type': 'scatter',
            'x_axis': 'Likelihood (1-5)',
            'y_axis': 'Severity (1-5)',
            'zones': {
                'critical': {
                    'min_score': 16,
                    'color': '#dc2626'
                },
                'high': {
                    'min_score': 12,
                    'color': '#f59e0b'
                },
                'medium': {
                    'min_score': 6,
                    'color': '#fbbf24'
                },
                'low': {
                    'min_score': 0,
                    'color': '#10b981'
                }
            }
        }
        
        return {
            'summary': overall_risk['summary'],
            'risk_score': overall_risk['risk_score'],
            'risk_level': overall_risk['risk_level'],
            'matrix_data': matrix_data,
            'visualization': visualization
        }
    
    @staticmethod
    def generate_recommendations(risk_matrix: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on risk matrix
        
        Args:
            risk_matrix: Risk matrix data
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        summary = risk_matrix['summary']
        
        # Critical issues
        if summary['critical'] > 0:
            recommendations.append(
                f"[CRITICAL] Address {summary['critical']} critical security issue{'s' if summary['critical'] > 1 else ''} immediately"
            )
        
        # High issues
        if summary['high'] > 0:
            recommendations.append(
                f"[HIGH] Refactor {summary['high']} high-risk area{'s' if summary['high'] > 1 else ''} before production"
            )
        
        # Medium issues
        if summary['medium'] > 0:
            recommendations.append(
                f"[MEDIUM] Review {summary['medium']} medium-priority issue{'s' if summary['medium'] > 1 else ''} for code quality"
            )
        
        # Low issues
        if summary['low'] > 0:
            recommendations.append(
                f"[LOW] Consider optimizing {summary['low']} low-priority item{'s' if summary['low'] > 1 else ''} for maintainability"
            )
        
        # Overall recommendation
        if summary['total_issues'] == 0:
            recommendations.append("[OK] No issues detected - code looks good!")
        elif risk_matrix['risk_level'] == 'CRITICAL':
            recommendations.append("[URGENT] This code has critical security vulnerabilities that must be fixed")
        elif risk_matrix['risk_level'] == 'HIGH':
            recommendations.append("[WARNING] This code requires significant improvements before deployment")
        elif risk_matrix['risk_level'] == 'MEDIUM':
            recommendations.append("[INFO] This code would benefit from refactoring and optimization")
        else:
            recommendations.append("[OK] This code is in good shape with minor improvements needed")
        
        return recommendations

# Made with Bob
