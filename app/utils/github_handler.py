"""
GitHub repository handler for cloning and managing repositories
"""
import os
import shutil
import tempfile
from typing import Optional, List, Tuple
from pathlib import Path
import git
from urllib.parse import urlparse

class GitHubRepoHandler:
    """Handle GitHub repository operations"""
    
    # Supported code file extensions
    CODE_EXTENSIONS = {
        '.py', '.js', '.java', '.ts', '.jsx', '.tsx',
        '.c', '.cpp', '.h', '.hpp', '.cs', '.go',
        '.rb', '.php', '.swift', '.kt', '.rs', '.scala'
    }
    
    # Files/directories to skip
    SKIP_PATTERNS = {
        'node_modules', 'venv', 'env', '.git', '__pycache__',
        'dist', 'build', 'target', '.idea', '.vscode',
        'vendor', 'packages', '.next', 'out'
    }
    
    def __init__(self):
        self.temp_dir = None
        self.repo_path = None
    
    def parse_github_url(self, url: str) -> Tuple[str, str]:
        """
        Parse GitHub URL to extract owner and repo name
        
        Args:
            url: GitHub repository URL
            
        Returns:
            Tuple of (owner, repo_name)
        """
        # Handle different GitHub URL formats
        # https://github.com/owner/repo
        # https://github.com/owner/repo.git
        # git@github.com:owner/repo.git
        
        if url.startswith('git@'):
            # SSH format
            parts = url.replace('git@github.com:', '').replace('.git', '').split('/')
        else:
            # HTTPS format
            parsed = urlparse(url)
            parts = parsed.path.strip('/').replace('.git', '').split('/')
        
        if len(parts) >= 2:
            return parts[0], parts[1]
        raise ValueError(f"Invalid GitHub URL format: {url}")
    
    def clone_repository(self, repo_url: str) -> str:
        """
        Clone a GitHub repository to a temporary directory
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Path to cloned repository
        """
        try:
            # Create temporary directory
            self.temp_dir = tempfile.mkdtemp(prefix='hitscan_repo_')
            
            # Clone repository
            print(f"Cloning repository from {repo_url}...")
            git.Repo.clone_from(repo_url, self.temp_dir, depth=1)
            
            self.repo_path = self.temp_dir
            return self.repo_path
            
        except git.GitCommandError as e:
            self.cleanup()
            raise Exception(f"Failed to clone repository: {str(e)}")
    
    def get_code_files(self, max_files: int = 100) -> List[dict]:
        """
        Get all code files from the cloned repository
        
        Args:
            max_files: Maximum number of files to analyze
            
        Returns:
            List of file information dictionaries
        """
        if not self.repo_path:
            raise Exception("No repository cloned")
        
        code_files = []
        repo_path = Path(self.repo_path)
        
        for file_path in repo_path.rglob('*'):
            # Skip if we've reached max files
            if len(code_files) >= max_files:
                break
            
            # Skip directories
            if file_path.is_dir():
                continue
            
            # Skip files in excluded directories
            if any(skip in file_path.parts for skip in self.SKIP_PATTERNS):
                continue
            
            # Check if it's a code file
            if file_path.suffix.lower() in self.CODE_EXTENSIONS:
                try:
                    # Get relative path from repo root
                    rel_path = file_path.relative_to(repo_path)
                    
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Skip empty files or very large files (>1MB)
                    if not content or len(content) > 1_000_000:
                        continue
                    
                    code_files.append({
                        'path': str(rel_path),
                        'full_path': str(file_path),
                        'content': content,
                        'extension': file_path.suffix,
                        'size': len(content)
                    })
                    
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}")
                    continue
        
        return code_files
    
    def detect_language_from_extension(self, extension: str) -> Optional[str]:
        """
        Detect programming language from file extension
        
        Args:
            extension: File extension (e.g., '.py')
            
        Returns:
            Language name or None
        """
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'javascript',
            '.tsx': 'javascript',
            '.java': 'java',
        }
        return extension_map.get(extension.lower())
    
    def cleanup(self):
        """Remove temporary directory and cloned repository"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print(f"Cleaned up temporary directory: {self.temp_dir}")
            except Exception as e:
                print(f"Warning: Could not clean up {self.temp_dir}: {e}")
            finally:
                self.temp_dir = None
                self.repo_path = None
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.cleanup()

# Made with Bob