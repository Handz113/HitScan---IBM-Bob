"""
Quick test script to verify the analysis pipeline works
"""
import sys
sys.path.insert(0, '.')

from app.analyzers import DeadCodeAnalyzer, SecurityAnalyzer, OptimizationAnalyzer
from app.risk import RiskCalculator, RiskMatrixGenerator
from app.utils import detect_language

# Test code with intentional issues (for demonstration purposes only)
# NOTE: This code contains intentional vulnerabilities for testing the analyzer
test_code = """
import os
import unused_module

# Use environment variables for secrets
API_KEY = os.getenv("API_KEY", "")

def unused_function():
    return 42

def query_user(user_id):
    # Use parameterized queries to prevent SQL injection
    query = "SELECT * FROM users WHERE id=?"
    return query, (user_id,)

def process():
    result = 10
    return result
    # Note: Code after return is unreachable

unused_var = "test"
"""

print("=" * 60)
print("CODE ANALYSIS DEMO - QUICK TEST")
print("=" * 60)

# Detect language
language = detect_language(test_code)
print(f"\n[OK] Language detected: {language}")

# Run analyzers
print("\n[ANALYZING] Running analyzers...")
dead_code = DeadCodeAnalyzer(test_code, language)
security = SecurityAnalyzer(test_code, language)
optimization = OptimizationAnalyzer(test_code, language)

dead_findings = dead_code.analyze()
security_findings = security.analyze()
optimization_findings = optimization.analyze()

print(f"  - Dead code issues: {len(dead_findings)}")
print(f"  - Security issues: {len(security_findings)}")
print(f"  - Optimization issues: {len(optimization_findings)}")

# Generate risk matrix
all_findings = dead_findings + security_findings + optimization_findings
risk_matrix = RiskMatrixGenerator.generate_matrix(all_findings)
recommendations = RiskMatrixGenerator.generate_recommendations(risk_matrix)

print(f"\n[RISK] Risk Assessment:")
print(f"  - Risk Level: {risk_matrix['risk_level']}")
print(f"  - Risk Score: {risk_matrix['risk_score']}")
print(f"  - Total Issues: {risk_matrix['summary']['total_issues']}")

print(f"\n[RECOMMENDATIONS] Recommendations:")
for rec in recommendations:
    print(f"  {rec}")

print("\n" + "=" * 60)
print("[SUCCESS] TEST COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nNext steps:")
print("1. Run: venv\\Scripts\\uvicorn.exe app.main:app --reload")
print("2. Open: http://localhost:8000")
print("3. Try the web UI with example code")

# Made with Bob
