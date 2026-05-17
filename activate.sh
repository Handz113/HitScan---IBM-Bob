#!/bin/bash
# Activate virtual environment for Bash/Zsh
echo -e "\033[0;32mActivating virtual environment...\033[0m"
source ./venv/bin/activate
echo ""
echo -e "\033[0;32mVirtual environment activated!\033[0m"
echo ""
echo -e "\033[0;33mQuick commands:\033[0m"
echo -e "\033[0;36m  Start server: uvicorn app.main:app --reload\033[0m"
echo -e "\033[0;36m  Run test:     python test_analysis.py\033[0m"
echo -e "\033[0;36m  Open browser: http://localhost:8000\033[0m"
echo ""

# Made with Bob