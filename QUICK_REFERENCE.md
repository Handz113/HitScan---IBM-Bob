# Quick Reference Card - Code Analysis Demo

## 🚀 Start Commands

```bash
# Quick start
run.bat

# Manual start
venv\Scripts\activate
venv\Scripts\uvicorn.exe app.main:app --reload

# Test without UI
venv\Scripts\python.exe test_analysis.py
```

## 🌐 URLs

- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📡 API Examples

### Analyze Code
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"API_KEY='secret123'\", \"language\": \"python\"}"
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 🎯 Demo Flow (5 min)

1. **Intro** (30s): Problem statement
2. **Load Example** (30s): Click "Python Example"
3. **Analyze** (2m): Click analyze, show results
4. **API Demo** (1m): Show curl command
5. **Use Cases** (1m): List applications
6. **Close** (30s): Impact statement

## 📊 Key Numbers

- **11 issues** detected in example
- **<2 seconds** analysis time
- **3 languages** supported
- **30+ security patterns**
- **Zero infrastructure** needed

## 🎤 Key Talking Points

1. "Automated code analysis with visual Risk Matrix"
2. "Detects security vulnerabilities before they reach production"
3. "Fast, accurate, and actionable results"
4. "Easy CI/CD integration via REST API"
5. "Lightweight - runs anywhere, no Docker needed"

## 🔥 Strong Closing

> "Imagine running this on every pull request. Security issues caught before production. Dead code cleaned up automatically. Developers learning in real-time. That's the power of automated code analysis."

## 🚨 Backup Plan

If UI fails:
1. Run: `venv\Scripts\python.exe test_analysis.py`
2. Show curl command output
3. Say: "Backend is solid, just a frontend issue"

## ❓ Common Questions

**Q: vs SonarQube?**  
A: Lightweight & fast, complementary tool

**Q: Entire projects?**  
A: Currently single-file, natural next step

**Q: Custom rules?**  
A: Architecture supports it, easy to add

**Q: Accuracy?**  
A: AST-based, industry standards (OWASP, CWE)

## 📁 Important Files

- `README.md` - Setup instructions
- `DEMO_GUIDE.md` - Full presentation script
- `PROJECT_SUMMARY.md` - Complete overview
- `test_analysis.py` - Quick test

## ✅ Pre-Demo Checklist

- [ ] Server running
- [ ] Browser open to localhost:8000
- [ ] Example buttons work
- [ ] Curl command ready
- [ ] Know your talking points
- [ ] Backup plan ready

---

**You're ready! Good luck! 🚀**