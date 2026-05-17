"""
FastAPI application for code analysis
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid
from datetime import datetime
from typing import List
import requests
import re

from .models import (
    AnalyzeRequest,
    AnalyzeResponse,
    HealthResponse,
    Finding,
    FindingsGroup,
    CodeMetrics
)
from .models_repo import (
    AnalyzeRepoRequest,
    AnalyzeRepoResponse,
    ListFilesRequest,
    ListFilesResponse
)
from .utils import detect_language
from .utils.prompt_generator import AIFixPromptGenerator
from .analyzers import (
    DeadCodeAnalyzer,
    SecurityAnalyzer,
    OptimizationAnalyzer
)
from .analyzers.repository import RepositoryAnalyzer
from .risk import RiskCalculator, RiskMatrixGenerator

# Create FastAPI app
app = FastAPI(
    title="Code Analysis Demo Tool",
    description="Analyze code for dead code, security issues, and optimization opportunities",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve the web UI"""
    return FileResponse("static/index.html")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        supported_languages=["python", "javascript", "java"]
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest):
    """
    Analyze code snippet and return risk matrix
    
    Args:
        request: Code analysis request
        
    Returns:
        Complete analysis with risk matrix
    """
    try:
        # Detect language if not provided
        language = request.language
        if not language:
            detected = detect_language(request.code)
            if not detected:
                raise HTTPException(
                    status_code=400,
                    detail="Could not detect language. Please specify language explicitly."
                )
            language = detected
        
        # Validate language
        if language not in ["python", "javascript", "java"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {language}"
            )
        
        # Run analyzers
        dead_code_analyzer = DeadCodeAnalyzer(request.code, language)
        security_analyzer = SecurityAnalyzer(request.code, language)
        optimization_analyzer = OptimizationAnalyzer(request.code, language)
        
        dead_code_findings = dead_code_analyzer.analyze()
        security_findings = security_analyzer.analyze()
        optimization_findings = optimization_analyzer.analyze()
        
        # Convert to Finding objects
        findings_group = FindingsGroup(
            dead_code=[Finding(**f) for f in dead_code_findings],
            security_issues=[Finding(**f) for f in security_findings],
            optimizations=[Finding(**f) for f in optimization_findings]
        )
        
        # Combine all findings for risk calculation
        all_findings = dead_code_findings + security_findings + optimization_findings
        
        # Generate risk matrix
        risk_matrix = RiskMatrixGenerator.generate_matrix(all_findings)
        recommendations = RiskMatrixGenerator.generate_recommendations(risk_matrix)
        
        # Calculate code metrics
        lines_of_code = len(request.code.split('\n'))
        
        # Try to calculate complexity (Python only)
        complexity = 1.0
        maintainability = 100.0
        
        if language == 'python':
            try:
                from radon.complexity import cc_visit
                from radon.metrics import mi_visit
                
                complexity_results = cc_visit(request.code)
                if complexity_results:
                    complexity = sum(r.complexity for r in complexity_results) / len(complexity_results)
                
                mi_result = mi_visit(request.code, multi=True)
                if mi_result:
                    maintainability = mi_result
            except:
                pass  # Use defaults if radon fails
        
        code_metrics = CodeMetrics(
            lines_of_code=lines_of_code,
            cyclomatic_complexity=round(complexity, 1),
            maintainability_index=round(maintainability, 1)
        )
        
        # Generate AI fix prompt
        findings_dict = {
            'dead_code': dead_code_findings,
            'security_issues': security_findings,
            'optimizations': optimization_findings
        }
        
        remediation_prompt = AIFixPromptGenerator.generate_fix_prompt(
            code=request.code,
            language=language,
            findings=findings_dict,
            code_metrics={
                'lines_of_code': lines_of_code,
                'cyclomatic_complexity': round(complexity, 1),
                'maintainability_index': round(maintainability, 1)
            }
        )
        
        # Create response
        response = AnalyzeResponse(
            analysis_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat() + 'Z',
            language=language,
            code_metrics=code_metrics,
            findings=findings_group,
            risk_matrix=risk_matrix,
            recommendations=recommendations,
            remediation_prompt=remediation_prompt
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )



@app.post("/list-repo-files")
async def list_repository_files(request: ListFilesRequest):
    """
    List all code files in a GitHub repository without analyzing
    
    Args:
        request: Repository listing request with GitHub URL
        
    Returns:
        List of all code files in the repository
    """
    try:
        # Validate GitHub URL
        if not ('github.com' in request.repo_url):
            raise HTTPException(
                status_code=400,
                detail="Only GitHub repositories are supported"
            )
        
        # Create repository analyzer
        analyzer = RepositoryAnalyzer(request.repo_url)
        
        # List files
        result = analyzer.list_files(max_files=request.max_files)
        
        return ListFilesResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list repository files: {str(e)}"
        )


@app.post("/analyze-repo")
async def analyze_repository(request: AnalyzeRepoRequest):
    """
    Analyze a GitHub repository
    
    Args:
        request: Repository analysis request with GitHub URL
        
    Returns:
        Complete repository analysis with aggregated results
    """
    try:
        # Validate GitHub URL
        if not ('github.com' in request.repo_url):
            raise HTTPException(
                status_code=400,
                detail="Only GitHub repositories are supported"
            )
        
        # Create repository analyzer
        analyzer = RepositoryAnalyzer(request.repo_url)
        
        # Analyze repository
        result = analyzer.analyze(
            max_files=request.max_files,
            selected_files=request.selected_files
        )
        
        # Check for errors
        if 'error' in result:
            return RepoErrorResponse(**result)
        
        # Generate repository-wide AI fix prompt
        repo_info = {
            'owner': result['owner'],
            'repo_name': result['repo_name'],
            'repo_url': result['repo_url']
        }
        
        remediation_prompt = AIFixPromptGenerator.generate_repository_fix_prompt(
            repo_info=repo_info,
            file_results=result['file_results'],
            aggregated_stats=result['aggregated_stats']
        )
        
        # Add prompt to result
        result['remediation_prompt'] = remediation_prompt
        
        return AnalyzeRepoResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Repository analysis failed: {str(e)}"
        )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
