# GitHub Repository Analysis Feature

## Overview

The HitScan tool now supports analyzing entire GitHub repositories in addition to code snippets. This feature allows you to clone public repositories and perform comprehensive code analysis across all supported files.

## Features Implemented

### 1. Repository Cloning
- Automatic cloning of GitHub repositories using GitPython
- Shallow clone (depth=1) for faster performance
- Automatic cleanup of temporary directories

### 2. Multi-File Analysis
- Analyzes up to 100 files by default (configurable up to 500)
- Supports Python, JavaScript, and Java files
- Automatic file type detection based on extensions
- Intelligent filtering of non-code files and directories

### 3. Aggregated Reporting
- Repository-wide statistics
- Total issues across all files
- Issues per 1000 lines metric
- Breakdown by category (dead code, security, optimization)
- Breakdown by severity level

### 4. File Comparison
- Side-by-side comparison of all analyzed files
- Issue density calculation (issues per 100 lines)
- Sortable by various metrics
- Color-coded severity indicators

### 5. Detailed Findings
- Per-file detailed analysis
- Line number references for each finding
- Categorized by issue type
- Full context for each issue

## Architecture

### Backend Components

#### `app/utils/github_handler.py`
- `GitHubRepoHandler` class for repository operations
- URL parsing for GitHub repositories
- Repository cloning with error handling
- Code file discovery with filtering
- Automatic cleanup

#### `app/analyzers/repository.py`
- `RepositoryAnalyzer` class for multi-file analysis
- Orchestrates analysis across all files
- Aggregates results from individual analyzers
- Generates comparison metrics
- Calculates repository-wide statistics

#### `app/models_repo.py`
- Pydantic models for repository analysis
- Request/response validation
- Type safety for API endpoints

#### `app/main.py` (updated)
- New `/analyze-repo` endpoint
- Integration with repository analyzer
- Error handling for repository operations

### Frontend Components

#### `static/repo.html`
- Dedicated UI for repository analysis
- Repository URL input
- Configurable max files setting
- Results visualization sections

#### `static/repo.js`
- API integration for repository analysis
- Dynamic results rendering
- Chart.js integration for visualizations
- File comparison table generation
- Detailed findings display

## Usage

### Web Interface

1. Navigate to http://localhost:8000
2. Click "📦 Analyze Repository" button
3. Enter a GitHub repository URL
4. Optionally adjust max files to analyze
5. Click "Analyze Repository"
6. Wait for analysis to complete (1-2 minutes)
7. Review comprehensive results

### API Usage

```bash
curl -X POST http://localhost:8000/analyze-repo \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/owner/repository",
    "max_files": 100
  }'
```

## File Filtering

### Included Extensions
- Python: `.py`
- JavaScript: `.js`, `.jsx`, `.ts`, `.tsx`
- Java: `.java`
- C/C++: `.c`, `.cpp`, `.h`, `.hpp`
- C#: `.cs`
- Go: `.go`
- Ruby: `.rb`
- PHP: `.php`
- Swift: `.swift`
- Kotlin: `.kt`
- Rust: `.rs`
- Scala: `.scala`

### Excluded Directories
- `node_modules`
- `venv`, `env`
- `.git`
- `__pycache__`
- `dist`, `build`, `target`
- `.idea`, `.vscode`
- `vendor`, `packages`
- `.next`, `out`

### File Size Limits
- Maximum file size: 1MB
- Empty files are skipped
- Binary files are automatically excluded

## Performance Considerations

1. **Shallow Cloning**: Uses `depth=1` to clone only the latest commit
2. **File Limits**: Default 100 files, max 500 to prevent timeouts
3. **Parallel Processing**: Could be added in future for faster analysis
4. **Cleanup**: Automatic removal of temporary directories
5. **Caching**: Could be implemented for repeated analyses

## Limitations

1. **Public Repositories Only**: No authentication support yet
2. **Single Branch**: Only analyzes the default branch
3. **No History**: Analyzes current state only, no historical trends
4. **File Limit**: Maximum 500 files per analysis
5. **Size Limit**: Files over 1MB are skipped
6. **Synchronous**: Analysis is blocking (could be async in future)

## Future Enhancements

- [ ] Private repository support with GitHub tokens
- [ ] Branch selection
- [ ] Historical analysis and trend tracking
- [ ] Asynchronous processing with job queue
- [ ] Result caching and persistence
- [ ] Comparison between different commits/branches
- [ ] Export reports to PDF/HTML
- [ ] Integration with CI/CD pipelines
- [ ] Webhook support for automatic analysis
- [ ] Team collaboration features

## Dependencies

New dependencies added to `requirements.txt`:
- `GitPython==3.1.40` - Git repository operations
- `requests==2.31.0` - HTTP requests (for future API features)

## Cross-Platform Compatibility

The repository analysis feature works on both:
- ✅ **Linux** - Full support with bash scripts
- ✅ **Windows** - Full support with batch/PowerShell scripts
- ✅ **macOS** - Full support (uses Linux scripts)

All Windows-specific files remain unchanged for your team members.

## Testing

To test the repository analysis feature:

```bash
# Start the server
./run.sh  # Linux/Mac
run.bat   # Windows

# Open browser
http://localhost:8000

# Click "Analyze Repository"
# Enter: https://github.com/your-test-repo
# Click "Analyze Repository"
```

## Troubleshooting

**Git not found error:**
```bash
# Linux
sudo apt-get install git

# Mac
brew install git
```

**Permission denied:**
```bash
chmod +x run.sh activate.sh
```

**Repository too large:**
- Reduce max_files parameter
- Choose a smaller repository for testing

**Analysis timeout:**
- Reduce max_files
- Check network connection
- Ensure repository is accessible

---

Made with Bob 🤖