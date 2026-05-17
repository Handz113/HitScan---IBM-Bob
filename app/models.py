"""
Pydantic models for request/response validation
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class Language(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"


class Severity(str, Enum):
    """Issue severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IssueCategory(str, Enum):
    """Issue categories"""
    DEAD_CODE = "dead_code"
    SECURITY = "security"
    OPTIMIZATION = "optimization"


class AnalyzeRequest(BaseModel):
    """Request model for code analysis"""
    code: str = Field(..., description="Code snippet to analyze")
    language: Optional[Language] = Field(None, description="Programming language (auto-detected if not provided)")


class Finding(BaseModel):
    """Individual code issue finding"""
    type: str = Field(..., description="Type of issue")
    line: int = Field(..., description="Line number where issue occurs")
    code: str = Field(..., description="Code snippet with the issue")
    message: str = Field(..., description="Description of the issue")
    severity: Severity = Field(..., description="Severity level")
    likelihood: int = Field(..., ge=1, le=5, description="Likelihood score (1-5)")
    cwe: Optional[str] = Field(None, description="CWE identifier for security issues")
    impact: Optional[str] = Field(None, description="Impact type for optimizations")


class CodeMetrics(BaseModel):
    """Code quality metrics"""
    lines_of_code: int
    cyclomatic_complexity: float
    maintainability_index: float


class FindingsGroup(BaseModel):
    """Grouped findings by category"""
    dead_code: List[Finding] = []
    security_issues: List[Finding] = []
    optimizations: List[Finding] = []


class RiskMatrixPoint(BaseModel):
    """Single point in the risk matrix"""
    id: str
    title: str
    severity: int = Field(..., ge=1, le=5)
    likelihood: int = Field(..., ge=1, le=5)
    risk_score: int
    category: IssueCategory
    color: str


class RiskZone(BaseModel):
    """Risk zone definition"""
    min_score: int
    color: str


class RiskVisualization(BaseModel):
    """Visualization configuration for risk matrix"""
    chart_type: str = "scatter"
    x_axis: str = "Likelihood (1-5)"
    y_axis: str = "Severity (1-5)"
    zones: Dict[str, RiskZone]


class RiskSummary(BaseModel):
    """Summary of risk levels"""
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    total_issues: int = 0


class RiskMatrix(BaseModel):
    """Complete risk matrix data"""
    summary: RiskSummary
    risk_score: float
    risk_level: str
    matrix_data: List[RiskMatrixPoint]
    visualization: RiskVisualization


class AnalyzeResponse(BaseModel):
    """Response model for code analysis"""
    analysis_id: str
    timestamp: str
    language: Language
    code_metrics: CodeMetrics
    findings: FindingsGroup
    risk_matrix: RiskMatrix
    recommendations: List[str]
    remediation_prompt: str = Field(..., description="AI-ready prompt for automatic code fixing")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    supported_languages: List[str]

# Made with Bob
