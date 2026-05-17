"""
AI Fix Prompt Generator
Generates detailed prompts for AI assistants to automatically fix code issues
"""
from typing import List, Dict, Any


class AIFixPromptGenerator:
    """Generate AI-ready prompts for code remediation"""
    
    @staticmethod
    def generate_fix_prompt(
        code: str,
        language: str,
        findings: Dict[str, List[Dict[str, Any]]],
        code_metrics: Dict[str, Any] = None,
        file_path: str = None
    ) -> str:
        """
        Generate a comprehensive AI fix prompt
        
        Args:
            code: The original code to be fixed
            language: Programming language
            findings: Dictionary with dead_code, security_issues, optimizations
            code_metrics: Optional code metrics
            file_path: Optional file path for context
            
        Returns:
            Formatted prompt string ready for AI consumption
        """
        
        # Count issues
        dead_code_count = len(findings.get('dead_code', []))
        security_count = len(findings.get('security_issues', []))
        optimization_count = len(findings.get('optimizations', []))
        total_issues = dead_code_count + security_count + optimization_count
        
        if total_issues == 0:
            return AIFixPromptGenerator._generate_no_issues_prompt(code, language, file_path)
        
        # Build the prompt
        prompt_parts = []
        
        # Header
        prompt_parts.append("# CODE REMEDIATION REQUEST")
        prompt_parts.append("")
        prompt_parts.append("You are an expert code refactoring assistant. I need you to fix the issues found in the following code.")
        prompt_parts.append("")
        
        # Context
        prompt_parts.append("## CONTEXT")
        prompt_parts.append(f"- **Language**: {language.title()}")
        if file_path:
            prompt_parts.append(f"- **File**: {file_path}")
        if code_metrics:
            prompt_parts.append(f"- **Lines of Code**: {code_metrics.get('lines_of_code', 'N/A')}")
            prompt_parts.append(f"- **Cyclomatic Complexity**: {code_metrics.get('cyclomatic_complexity', 'N/A')}")
        prompt_parts.append(f"- **Total Issues Found**: {total_issues}")
        prompt_parts.append(f"  - Dead Code: {dead_code_count}")
        prompt_parts.append(f"  - Security Issues: {security_count}")
        prompt_parts.append(f"  - Optimization Opportunities: {optimization_count}")
        prompt_parts.append("")
        
        # Original Code
        prompt_parts.append("## ORIGINAL CODE")
        prompt_parts.append("```" + language)
        prompt_parts.append(code)
        prompt_parts.append("```")
        prompt_parts.append("")
        
        # Issues Found
        prompt_parts.append("## ISSUES IDENTIFIED")
        prompt_parts.append("")
        
        # Dead Code Issues
        if dead_code_count > 0:
            prompt_parts.append("### 🧹 Dead Code Issues")
            prompt_parts.append("")
            for i, issue in enumerate(findings.get('dead_code', []), 1):
                prompt_parts.append(f"**{i}. {issue.get('category', 'Unknown')}** (Severity: {issue.get('severity', 'MEDIUM')})")
                prompt_parts.append(f"   - **Issue**: {issue.get('message', 'No description')}")
                if issue.get('line'):
                    prompt_parts.append(f"   - **Location**: Line {issue['line']}")
                if issue.get('suggestion'):
                    prompt_parts.append(f"   - **Suggestion**: {issue['suggestion']}")
                prompt_parts.append("")
        
        # Security Issues
        if security_count > 0:
            prompt_parts.append("### 🔒 Security Vulnerabilities")
            prompt_parts.append("")
            for i, issue in enumerate(findings.get('security_issues', []), 1):
                prompt_parts.append(f"**{i}. {issue.get('category', 'Unknown')}** (Severity: {issue.get('severity', 'HIGH')})")
                prompt_parts.append(f"   - **Issue**: {issue.get('message', 'No description')}")
                if issue.get('line'):
                    prompt_parts.append(f"   - **Location**: Line {issue['line']}")
                if issue.get('suggestion'):
                    prompt_parts.append(f"   - **Fix**: {issue['suggestion']}")
                prompt_parts.append("")
        
        # Optimization Issues
        if optimization_count > 0:
            prompt_parts.append("### ⚡ Optimization Opportunities")
            prompt_parts.append("")
            for i, issue in enumerate(findings.get('optimizations', []), 1):
                prompt_parts.append(f"**{i}. {issue.get('category', 'Unknown')}** (Severity: {issue.get('severity', 'LOW')})")
                prompt_parts.append(f"   - **Issue**: {issue.get('message', 'No description')}")
                if issue.get('line'):
                    prompt_parts.append(f"   - **Location**: Line {issue['line']}")
                if issue.get('suggestion'):
                    prompt_parts.append(f"   - **Improvement**: {issue['suggestion']}")
                prompt_parts.append("")
        
        # Instructions
        prompt_parts.append("## YOUR TASK")
        prompt_parts.append("")
        prompt_parts.append("Please refactor the code above following these instructions:")
        prompt_parts.append("")
        prompt_parts.append("1. **Fix all security vulnerabilities** - These are critical and must be addressed first")
        prompt_parts.append("2. **Remove all dead code** - Eliminate unused variables, functions, imports, and unreachable code")
        prompt_parts.append("3. **Apply optimizations** - Improve performance and code quality where identified")
        prompt_parts.append("4. **Maintain functionality** - Ensure the refactored code works exactly like the original")
        prompt_parts.append("5. **Preserve code style** - Keep the same indentation, naming conventions, and structure where possible")
        prompt_parts.append("6. **Add comments** - Document any significant changes or security fixes")
        prompt_parts.append("")
        
        # Output Format
        prompt_parts.append("## OUTPUT FORMAT")
        prompt_parts.append("")
        prompt_parts.append("Please provide:")
        prompt_parts.append("")
        prompt_parts.append("1. **The complete refactored code** in a code block")
        prompt_parts.append("2. **A summary of changes** explaining what was fixed and why")
        prompt_parts.append("3. **Any remaining concerns** or recommendations for further improvement")
        prompt_parts.append("")
        prompt_parts.append("---")
        prompt_parts.append("")
        prompt_parts.append("**Note**: This prompt was automatically generated by HitScan Code Analysis Tool")
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def _generate_no_issues_prompt(code: str, language: str, file_path: str = None) -> str:
        """Generate prompt when no issues are found"""
        prompt_parts = []
        
        prompt_parts.append("# CODE REVIEW - NO ISSUES FOUND ✅")
        prompt_parts.append("")
        prompt_parts.append("Great news! The automated analysis found no significant issues in this code.")
        prompt_parts.append("")
        prompt_parts.append("## CODE ANALYZED")
        prompt_parts.append(f"- **Language**: {language.title()}")
        if file_path:
            prompt_parts.append(f"- **File**: {file_path}")
        prompt_parts.append("")
        prompt_parts.append("```" + language)
        prompt_parts.append(code)
        prompt_parts.append("```")
        prompt_parts.append("")
        prompt_parts.append("## ANALYSIS RESULTS")
        prompt_parts.append("")
        prompt_parts.append("✅ No dead code detected")
        prompt_parts.append("✅ No security vulnerabilities found")
        prompt_parts.append("✅ No obvious optimization opportunities")
        prompt_parts.append("")
        prompt_parts.append("However, if you'd like a human expert review or have specific concerns, feel free to ask!")
        
        return "\n".join(prompt_parts)
    
    @staticmethod
    def generate_repository_fix_prompt(
        repo_info: Dict[str, Any],
        file_results: List[Dict[str, Any]],
        aggregated_stats: Dict[str, Any]
    ) -> str:
        """
        Generate AI fix prompt for entire repository
        
        Args:
            repo_info: Repository information (owner, name, url)
            file_results: List of file analysis results
            aggregated_stats: Aggregated statistics
            
        Returns:
            Formatted prompt for repository-wide fixes
        """
        prompt_parts = []
        
        # Header
        prompt_parts.append("# REPOSITORY-WIDE CODE REMEDIATION REQUEST")
        prompt_parts.append("")
        prompt_parts.append("You are an expert code refactoring assistant. I need you to help fix issues across multiple files in a repository.")
        prompt_parts.append("")
        
        # Repository Context
        prompt_parts.append("## REPOSITORY CONTEXT")
        prompt_parts.append(f"- **Repository**: {repo_info.get('owner', 'Unknown')}/{repo_info.get('repo_name', 'Unknown')}")
        prompt_parts.append(f"- **URL**: {repo_info.get('repo_url', 'N/A')}")
        prompt_parts.append(f"- **Files Analyzed**: {len(file_results)}")
        prompt_parts.append(f"- **Total Lines**: {aggregated_stats.get('total_lines', 0):,}")
        prompt_parts.append(f"- **Languages**: {', '.join(aggregated_stats.get('languages_analyzed', []))}")
        prompt_parts.append("")
        
        # Overall Statistics
        breakdown = aggregated_stats.get('breakdown', {})
        prompt_parts.append("## OVERALL ISSUES")
        prompt_parts.append(f"- **Total Issues**: {aggregated_stats.get('total_issues', 0)}")
        prompt_parts.append(f"  - Dead Code: {breakdown.get('dead_code', 0)}")
        prompt_parts.append(f"  - Security Issues: {breakdown.get('security', 0)}")
        prompt_parts.append(f"  - Optimizations: {breakdown.get('optimization', 0)}")
        prompt_parts.append(f"- **Issue Density**: {aggregated_stats.get('issues_per_1000_lines', 0)} issues per 1000 lines")
        prompt_parts.append("")
        
        # Most Problematic Files
        problematic = aggregated_stats.get('most_problematic_files', [])[:5]
        if problematic:
            prompt_parts.append("## MOST PROBLEMATIC FILES")
            prompt_parts.append("")
            for i, file_info in enumerate(problematic, 1):
                prompt_parts.append(f"{i}. **{file_info['path']}** - {file_info['issues']} issues")
                breakdown = file_info.get('breakdown', {})
                prompt_parts.append(f"   - Dead Code: {breakdown.get('dead_code', 0)}, Security: {breakdown.get('security', 0)}, Optimization: {breakdown.get('optimization', 0)}")
            prompt_parts.append("")
        
        # Detailed File Issues
        prompt_parts.append("## DETAILED ISSUES BY FILE")
        prompt_parts.append("")
        
        for file_result in file_results:
            findings = file_result.get('findings', {})
            total_file_issues = sum(file_result.get('findings_count', {}).values())
            
            if total_file_issues == 0:
                continue
            
            prompt_parts.append(f"### 📄 {file_result['path']}")
            prompt_parts.append(f"**Language**: {file_result['language']} | **Lines**: {file_result['lines']} | **Issues**: {total_file_issues}")
            prompt_parts.append("")
            
            # Dead Code
            if findings.get('dead_code'):
                prompt_parts.append("**Dead Code:**")
                for issue in findings['dead_code'][:3]:  # Limit to top 3
                    prompt_parts.append(f"- Line {issue.get('line', '?')}: {issue.get('message', 'No description')}")
                if len(findings['dead_code']) > 3:
                    prompt_parts.append(f"- ... and {len(findings['dead_code']) - 3} more")
                prompt_parts.append("")
            
            # Security
            if findings.get('security_issues'):
                prompt_parts.append("**Security Issues:**")
                for issue in findings['security_issues'][:3]:
                    prompt_parts.append(f"- Line {issue.get('line', '?')}: {issue.get('message', 'No description')}")
                if len(findings['security_issues']) > 3:
                    prompt_parts.append(f"- ... and {len(findings['security_issues']) - 3} more")
                prompt_parts.append("")
            
            # Optimizations
            if findings.get('optimizations'):
                prompt_parts.append("**Optimizations:**")
                for issue in findings['optimizations'][:3]:
                    prompt_parts.append(f"- Line {issue.get('line', '?')}: {issue.get('message', 'No description')}")
                if len(findings['optimizations']) > 3:
                    prompt_parts.append(f"- ... and {len(findings['optimizations']) - 3} more")
                prompt_parts.append("")
        
        # Instructions
        prompt_parts.append("## YOUR TASK")
        prompt_parts.append("")
        prompt_parts.append("Please help me create a remediation plan for this repository:")
        prompt_parts.append("")
        prompt_parts.append("1. **Prioritize the fixes** - Start with security issues, then dead code, then optimizations")
        prompt_parts.append("2. **Focus on the most problematic files first** - These have the highest issue density")
        prompt_parts.append("3. **Provide file-by-file fixes** - For each file, show the refactored code")
        prompt_parts.append("4. **Explain your changes** - Document why each change was made")
        prompt_parts.append("5. **Maintain consistency** - Keep coding style consistent across files")
        prompt_parts.append("")
        prompt_parts.append("## RECOMMENDED APPROACH")
        prompt_parts.append("")
        prompt_parts.append("Start with the most critical files and provide:")
        prompt_parts.append("- The complete refactored code for each file")
        prompt_parts.append("- A summary of changes made")
        prompt_parts.append("- Any cross-file dependencies or concerns")
        prompt_parts.append("")
        prompt_parts.append("---")
        prompt_parts.append("")
        prompt_parts.append("**Note**: This prompt was automatically generated by HitScan Code Analysis Tool")
        
        return "\n".join(prompt_parts)

# Made with Bob