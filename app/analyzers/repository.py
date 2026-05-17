"""
Repository analyzer for analyzing entire GitHub repositories
"""
from typing import List, Dict, Any, Optional
from collections import defaultdict
from ..utils.github_handler import GitHubRepoHandler
from .dead_code import DeadCodeAnalyzer
from .security import SecurityAnalyzer
from .optimization import OptimizationAnalyzer


class RepositoryAnalyzer:
    """Analyze entire repositories with aggregated results"""
    
    def __init__(self, repo_url: str):
        self.repo_url = repo_url
        self.handler = GitHubRepoHandler()
        self.files_analyzed = []
        self.total_findings = {
            'dead_code': [],
            'security_issues': [],
            'optimizations': []
        }
    
    def list_files(self, max_files: int = 500) -> Dict[str, Any]:
        """
        List all code files in the repository without analyzing
        
        Args:
            max_files: Maximum number of files to list
            
        Returns:
            Dictionary with repository info and file list
        """
        try:
            # Parse GitHub URL
            owner, repo_name = self.handler.parse_github_url(self.repo_url)
            
            # Clone repository
            repo_path = self.handler.clone_repository(self.repo_url)
            
            # Get code files
            code_files = self.handler.get_code_files(max_files=max_files)
            
            # Format file info
            file_list = []
            for file_info in code_files:
                language = self.handler.detect_language_from_extension(file_info['extension'])
                file_list.append({
                    'path': file_info['path'],
                    'extension': file_info['extension'],
                    'size': file_info['size'],
                    'language': language
                })
            
            return {
                'owner': owner,
                'repo_name': repo_name,
                'repo_url': self.repo_url,
                'total_files': len(file_list),
                'files': file_list
            }
            
        finally:
            # Always cleanup
            self.handler.cleanup()
    
    def analyze(self, max_files: int = 100, selected_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze repository and return aggregated results
        
        Args:
            max_files: Maximum number of files to analyze
            selected_files: Optional list of specific file paths to analyze
            
        Returns:
            Dictionary with aggregated analysis results
        """
        try:
            # Parse GitHub URL
            owner, repo_name = self.handler.parse_github_url(self.repo_url)
            
            # Clone repository
            repo_path = self.handler.clone_repository(self.repo_url)
            
            # Get code files
            code_files = self.handler.get_code_files(max_files=max_files)
            
            # Filter by selected files if provided
            if selected_files:
                code_files = [f for f in code_files if f['path'] in selected_files]
            
            if not code_files:
                return {
                    'error': 'No code files found in repository',
                    'owner': owner,
                    'repo_name': repo_name
                }
            
            # Analyze each file
            file_results = []
            total_lines = 0
            languages_found = set()
            
            for file_info in code_files:
                file_path = file_info['path']
                content = file_info['content']
                extension = file_info['extension']
                
                # Detect language
                language = self.handler.detect_language_from_extension(extension)
                if not language:
                    continue
                
                languages_found.add(language)
                
                try:
                    # Run analyzers
                    dead_code_analyzer = DeadCodeAnalyzer(content, language)
                    security_analyzer = SecurityAnalyzer(content, language)
                    optimization_analyzer = OptimizationAnalyzer(content, language)
                    
                    dead_code_findings = dead_code_analyzer.analyze()
                    security_findings = security_analyzer.analyze()
                    optimization_findings = optimization_analyzer.analyze()
                    
                    # Add file path to each finding
                    for finding in dead_code_findings:
                        finding['file'] = file_path
                        self.total_findings['dead_code'].append(finding)
                    
                    for finding in security_findings:
                        finding['file'] = file_path
                        self.total_findings['security_issues'].append(finding)
                    
                    for finding in optimization_findings:
                        finding['file'] = file_path
                        self.total_findings['optimizations'].append(finding)
                    
                    # Store file result
                    file_result = {
                        'path': file_path,
                        'language': language,
                        'lines': len(content.split('\n')),
                        'size': file_info['size'],
                        'findings_count': {
                            'dead_code': len(dead_code_findings),
                            'security': len(security_findings),
                            'optimization': len(optimization_findings)
                        },
                        'findings': {
                            'dead_code': dead_code_findings,
                            'security_issues': security_findings,
                            'optimizations': optimization_findings
                        }
                    }
                    file_results.append(file_result)
                    total_lines += file_result['lines']
                    
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
                    continue
            
            # Calculate aggregated statistics
            aggregated_stats = self._calculate_aggregated_stats(
                file_results, total_lines, languages_found
            )
            
            # Generate file comparison
            file_comparison = self._generate_file_comparison(file_results)
            
            return {
                'owner': owner,
                'repo_name': repo_name,
                'repo_url': self.repo_url,
                'files_analyzed': len(file_results),
                'total_lines': total_lines,
                'languages': list(languages_found),
                'aggregated_stats': aggregated_stats,
                'file_results': file_results,
                'file_comparison': file_comparison,
                'total_findings': self.total_findings
            }
            
        finally:
            # Always cleanup
            self.handler.cleanup()
    
    def _calculate_aggregated_stats(
        self, 
        file_results: List[Dict], 
        total_lines: int,
        languages: set
    ) -> Dict[str, Any]:
        """Calculate aggregated statistics across all files"""
        
        total_dead_code = len(self.total_findings['dead_code'])
        total_security = len(self.total_findings['security_issues'])
        total_optimization = len(self.total_findings['optimizations'])
        total_issues = total_dead_code + total_security + total_optimization
        
        # Count by severity
        severity_counts = defaultdict(int)
        for finding in (self.total_findings['dead_code'] + 
                       self.total_findings['security_issues'] + 
                       self.total_findings['optimizations']):
            severity_counts[finding.get('severity', 'MEDIUM')] += 1
        
        # Count by category
        category_counts = defaultdict(int)
        for finding in (self.total_findings['dead_code'] + 
                       self.total_findings['security_issues'] + 
                       self.total_findings['optimizations']):
            category_counts[finding.get('category', 'unknown')] += 1
        
        # Find most problematic files
        file_issue_counts = []
        for file_result in file_results:
            total_file_issues = sum(file_result['findings_count'].values())
            if total_file_issues > 0:
                file_issue_counts.append({
                    'path': file_result['path'],
                    'issues': total_file_issues,
                    'breakdown': file_result['findings_count']
                })
        
        file_issue_counts.sort(key=lambda x: x['issues'], reverse=True)
        
        return {
            'total_issues': total_issues,
            'total_lines': total_lines,
            'issues_per_1000_lines': round((total_issues / total_lines * 1000), 2) if total_lines > 0 else 0,
            'breakdown': {
                'dead_code': total_dead_code,
                'security': total_security,
                'optimization': total_optimization
            },
            'by_severity': dict(severity_counts),
            'by_category': dict(category_counts),
            'most_problematic_files': file_issue_counts[:10],
            'languages_analyzed': list(languages)
        }
    
    def _generate_file_comparison(self, file_results: List[Dict]) -> List[Dict]:
        """Generate comparison data between files"""
        
        comparison = []
        for file_result in file_results:
            total_issues = sum(file_result['findings_count'].values())
            
            comparison.append({
                'path': file_result['path'],
                'language': file_result['language'],
                'lines': file_result['lines'],
                'total_issues': total_issues,
                'issues_per_100_lines': round((total_issues / file_result['lines'] * 100), 2) if file_result['lines'] > 0 else 0,
                'dead_code': file_result['findings_count']['dead_code'],
                'security': file_result['findings_count']['security'],
                'optimization': file_result['findings_count']['optimization']
            })
        
        # Sort by issues per 100 lines (issue density)
        comparison.sort(key=lambda x: x['issues_per_100_lines'], reverse=True)
        
        return comparison

# Made with Bob