"""
Pydantic models for repository analysis
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ListFilesRequest(BaseModel):
    """Request model for listing repository files"""
    repo_url: str = Field(..., description="GitHub repository URL")
    max_files: int = Field(default=500, ge=1, le=500, description="Maximum number of files to list")


class FileInfo(BaseModel):
    """Information about a single file"""
    path: str
    extension: str
    size: int
    language: Optional[str] = None


class ListFilesResponse(BaseModel):
    """Response model for listing repository files"""
    owner: str
    repo_name: str
    repo_url: str
    total_files: int
    files: List[FileInfo]


class AnalyzeRepoRequest(BaseModel):
    """Request model for repository analysis"""
    repo_url: str = Field(..., description="GitHub repository URL")
    max_files: int = Field(default=100, ge=1, le=500, description="Maximum number of files to analyze")
    selected_files: Optional[List[str]] = Field(default=None, description="List of specific file paths to analyze")


class FileAnalysisResult(BaseModel):
    """Analysis result for a single file"""
    path: str
    language: str
    lines: int
    size: int
    findings_count: Dict[str, int]
    findings: Dict[str, List[Dict[str, Any]]]


class AggregatedStats(BaseModel):
    """Aggregated statistics across all files"""
    total_issues: int
    total_lines: int
    issues_per_1000_lines: float
    breakdown: Dict[str, int]
    by_severity: Dict[str, int]
    by_category: Dict[str, int]
    most_problematic_files: List[Dict[str, Any]]
    languages_analyzed: List[str]


class FileComparison(BaseModel):
    """Comparison data for a file"""
    path: str
    language: str
    lines: int
    total_issues: int
    issues_per_100_lines: float
    dead_code: int
    security: int
    optimization: int


class AnalyzeRepoResponse(BaseModel):
    """Response model for repository analysis"""
    owner: str
    repo_name: str
    repo_url: str
    files_analyzed: int
    total_lines: int
    languages: List[str]
    aggregated_stats: AggregatedStats
    file_results: List[FileAnalysisResult]
    file_comparison: List[FileComparison]
    total_findings: Dict[str, List[Dict[str, Any]]]


class RepoErrorResponse(BaseModel):
    """Error response for repository analysis"""
    error: str
    owner: Optional[str] = None
    repo_name: Optional[str] = None

# Made with Bob