# Code Analysis Demo Tool 🔍

A lightweight, single-use demo tool that analyzes code snippets and entire GitHub repositories for dead code, security vulnerabilities, and optimization opportunities. Built for hackathon presentation with Python/FastAPI backend and minimal web UI.

## Features

✨ **Multi-Language Support**: Analyzes Python, JavaScript, and Java code
🔒 **Security Scanning**: Detects SQL injection, XSS, hardcoded secrets, and more
🧹 **Dead Code Detection**: Finds unused variables, functions, imports, and unreachable code
⚡ **Optimization Analysis**: Identifies inefficient patterns and complexity issues
📊 **Risk Matrix**: Visual severity vs. likelihood matrix with color-coded zones
📦 **GitHub Repository Analysis**: Clone and analyze entire repositories
📈 **Aggregated Reporting**: Repository-wide statistics and file comparisons
🎯 **Zero Infrastructure**: No Docker, no database, runs locally in minutes

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation & Running

#### Option 1: Quick Start Script (Recommended)

**Windows:**
```bash
# Double-click run.bat or run in terminal:
run.bat
```

**Linux/Mac:**
```bash
# Make executable (first time only):
chmod +x run.sh

# Run the script:
./run.sh
```

The script will automatically:
- Create virtual environment if needed
- Install dependencies
- Start the FastAPI server

#### Option 2: Manual Setup

1. **Clone or navigate to the project directory**:
```bash
# Windows
cd f:/IBMBob

# Linux/Mac
cd /path/to/HitScan---IBM-Bob
```

2. **Create and activate virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Start the server**:
```bash
uvicorn app.main:app --reload --port 8000
```

**Access the web UI**:
Open your browser and navigate to:
```
http://localhost:8000
```

**Test the API directly**:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"x = 1\ny = 2\", \"language\": \"python\"}"
```

## Project Structure

```
code-analysis-demo/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── base.py            # Base analyzer class
│   │   ├── dead_code.py       # Dead code detector
│   │   ├── security.py        # Security scanner
│   │   ├── optimization.py    # Optimization analyzer
│   │   └── language_parser.py # Multi-language AST parser
│   ├── risk/
│   │   ├── __init__.py
│   │   ├── calculator.py      # Risk scoring logic
│   │   └── matrix.py          # Risk matrix generator
│   └── utils/
│       ├── __init__.py
│       └── language_detect.py # Language detection
├── static/
│   ├── index.html             # Web UI
│   └── app.js                 # Frontend logic
├── tests/
│   └── sample_code/           # Test code snippets
│       └── sample.py
├── requirements.txt
├── README.md
└── CODE_ANALYSIS_DEMO_PLAN.md
```

## Usage

### Web UI - Code Snippet Analysis

1. **Load Example Code**: Click one of the example buttons (Python/JavaScript/Java)
2. **Or Paste Your Code**: Enter your own code in the editor
3. **Select Language**: Choose language or leave as "Auto-detect"
4. **Click Analyze**: Wait for results (typically <2 seconds)
5. **Review Results**:
   - Summary cards show risk level, total issues, LOC, complexity
   - Risk Matrix visualizes findings by severity and likelihood
   - Recommendations provide actionable next steps
   - Findings tabs show detailed issues by category

### Web UI - Repository Analysis

1. **Navigate to Repository Analysis**: Click "📦 Analyze Repository" button
2. **Enter GitHub URL**: Paste a GitHub repository URL (e.g., `https://github.com/owner/repo`)
3. **Set Max Files**: Choose how many files to analyze (default: 100)
4. **Click Analyze Repository**: Wait for cloning and analysis (may take 1-2 minutes)
5. **Review Results**:
   - Repository-wide statistics and issue breakdown
   - Most problematic files ranked by issue density
   - File comparison table with detailed metrics
   - Per-file detailed findings with line numbers

### API Endpoints

#### POST `/analyze`
Analyze code snippet and return risk matrix.

**Request**:
```json
{
  "code": "def unused(): pass\nx = 1",
  "language": "python"
}
```

**Response**:
```json
{
  "analysis_id": "uuid",
  "timestamp": "2026-05-17T02:00:00Z",
  "language": "python",
  "code_metrics": {
    "lines_of_code": 2,
    "cyclomatic_complexity": 1.0,
    "maintainability_index": 100.0
  },
  "findings": {
    "dead_code": [...],
    "security_issues": [...],
    "optimizations": [...]
  },
  "risk_matrix": {
    "summary": {...},
    "risk_score": 5.2,
    "risk_level": "MEDIUM",
    "matrix_data": [...],
    "visualization": {...}
  },
  "recommendations": [...]
}
```

#### POST `/analyze-repo`
Analyze a GitHub repository.

**Request**:
```json
{
  "repo_url": "https://github.com/owner/repository",
  "max_files": 100
}
```

**Response**:
```json
{
  "owner": "owner",
  "repo_name": "repository",
  "files_analyzed": 45,
  "total_lines": 5234,
  "languages": ["python", "javascript"],
  "aggregated_stats": {
    "total_issues": 127,
    "issues_per_1000_lines": 24.3,
    "breakdown": {
      "dead_code": 45,
      "security": 12,
      "optimization": 70
    },
    "most_problematic_files": [...]
  },
  "file_comparison": [...],
  "file_results": [...]
}
```

#### GET `/health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "supported_languages": ["python", "javascript", "java"]
}
```

## Detection Capabilities

### Dead Code
- ✅ Unused variables
- ✅ Unused functions
- ✅ Unused imports (Python)
- ✅ Unreachable code after return/break
- ✅ Commented-out code

### Security Issues
- ✅ SQL injection vulnerabilities
- ✅ Hardcoded secrets (API keys, passwords)
- ✅ Command injection risks
- ✅ XSS vulnerabilities
- ✅ Path traversal risks
- ✅ Weak cryptographic algorithms
- ✅ Insecure random number generation
- ✅ Debug mode enabled
- ✅ Insecure deserialization
- ✅ Missing authentication checks

### Optimization Opportunities
- ✅ Inefficient loop patterns
- ✅ Redundant operations
- ✅ String concatenation in loops
- ✅ Deeply nested loops
- ✅ High cyclomatic complexity
- ✅ Low maintainability index

## Risk Matrix

The tool generates a 5×5 risk matrix mapping **Severity** (1-5) vs **Likelihood** (1-5):

```
Severity
   5 │ 🟢  🟡  🟡  🟠  🔴
   4 │ 🟢  🟡  🟠  🟠  🔴
   3 │ 🟢  🟡  🟠  🔴  🔴
   2 │ 🟢  🟢  🟡  🟠  🔴
   1 │ 🟢  🟢  🟢  🟡  🟠
     └─────────────────────
       1   2   3   4   5  Likelihood

🟢 Low Risk (1-5)
🟡 Medium Risk (6-11)
🟠 High Risk (12-15)
🔴 Critical Risk (16-25)
```

## Demo Presentation Tips

1. **Start with the Problem**: Show real-world code with security issues
2. **Live Demo**: Paste vulnerable code, click analyze, show results
3. **Highlight Risk Matrix**: Visual representation is compelling
4. **Show API**: Demonstrate curl command for technical audience
5. **Discuss Use Cases**: CI/CD integration, pre-commit hooks, code reviews

## Helper Scripts

### Activation Scripts

For convenience, activation scripts are provided to quickly activate the virtual environment:

**Windows (PowerShell):**
```powershell
.\activate.ps1
```

**Linux/Mac (Bash/Zsh):**
```bash
source activate.sh
# or
. activate.sh
```

These scripts will activate the virtual environment and display helpful commands.

## Troubleshooting

**Import errors when running**:
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

**Permission denied on Linux/Mac**:
```bash
# Make scripts executable
chmod +x run.sh activate.sh
```

**Port 8000 already in use**:
```bash
# Use a different port
uvicorn app.main:app --reload --port 8080
```

**Language detection fails**:
- Explicitly specify the language in the request
- Ensure code has clear language-specific syntax

## Development

**Run with auto-reload**:
```bash
uvicorn app.main:app --reload
```

**Test with sample code**:
```bash
# The sample.py file contains intentional issues for testing
python -c "
import requests
with open('tests/sample_code/sample.py') as f:
    code = f.read()
response = requests.post('http://localhost:8000/analyze', 
    json={'code': code, 'language': 'python'})
print(response.json())
"
```

## Limitations

- **Single-file analysis only**: Does not analyze project dependencies
- **Pattern-based detection**: May have false positives/negatives
- **No persistent storage**: Results are not saved
- **Limited language coverage**: Only Python, JavaScript, Java
- **Simplified complexity metrics**: Basic heuristics for non-Python code

## Future Enhancements

- 🔮 Add more languages (Go, Rust, C++)
- 🤖 Machine learning for smarter detection
- 🔗 GitHub/GitLab API integration
- 📈 Historical trend analysis
- 👥 Team collaboration features
- ⚙️ Custom rule configuration
- 💾 Result persistence and reporting

## License

This is a demo tool created for hackathon presentation. Use at your own discretion.

## Credits

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Esprima](https://esprima.org/) - JavaScript parser
- [javalang](https://github.com/c2nes/javalang) - Java parser
- [Radon](https://radon.readthedocs.io/) - Python complexity metrics
- [Bandit](https://bandit.readthedocs.io/) - Python security linter
- [CodeMirror](https://codemirror.net/) - Code editor
- [Chart.js](https://www.chartjs.org/) - Visualization library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS

---

**Ready to analyze some code? Start the server and open http://localhost:8000** 🚀