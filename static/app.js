// Initialize CodeMirror
let editor;
let riskChart;

document.addEventListener('DOMContentLoaded', function() {
    editor = CodeMirror.fromTextArea(document.getElementById('code-input'), {
        lineNumbers: true,
        mode: 'python',
        theme: 'default',
        indentUnit: 4,
        tabSize: 4,
        lineWrapping: true
    });
    
    // Load default example
    loadExample('python');
});

// Example code snippets
const examples = {
    python: `# Example Python code with issues
import os
import sys
import unused_module

API_KEY = "sk-1234567890abcdef"  # Hardcoded secret
DEBUG = True

def unused_function():
    """This function is never called"""
    return 42

def calculate_total(items):
    total = 0
    for i in range(len(items)):  # Inefficient loop
        total += items[i]
    return total

def query_user(user_id):
    # SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id={user_id}"
    return query

def process_data():
    result = calculate_total([1, 2, 3])
    return result
    print("This code is unreachable")  # Dead code

# Unused variable
unused_var = "never used"
`,
    
    javascript: `// Example JavaScript code with issues
const API_KEY = 'abc123secret';  // Hardcoded secret

function unusedFunction() {
    return 42;
}

function processData(userInput) {
    // XSS vulnerability
    document.getElementById('output').innerHTML = userInput;
    
    // Inefficient loop
    let result = '';
    for (let i = 0; i < items.length; i++) {
        result += items[i];  // String concatenation in loop
    }
    
    return result;
}

function queryDatabase(userId) {
    // SQL injection risk
    const query = "SELECT * FROM users WHERE id=" + userId;
    return query;
}

// Unreachable code
function example() {
    return true;
    console.log("Never executed");
}

// Unused variable
const unusedVar = "not used anywhere";
`,
    
    java: `// Example Java code with issues
import java.sql.*;
import java.util.*;

public class Example {
    private static final String API_KEY = "secret123";  // Hardcoded
    
    public void unusedMethod() {
        System.out.println("Never called");
    }
    
    public String queryUser(String userId) {
        // SQL injection vulnerability
        String query = "SELECT * FROM users WHERE id=" + userId;
        return query;
    }
    
    public int calculateTotal(List<Integer> items) {
        int total = 0;
        // Inefficient loop
        for (int i = 0; i < items.size(); i++) {
            total += items.get(i);
        }
        return total;
    }
    
    public void unreachableCode() {
        return;
        System.out.println("Never executed");  // Dead code
    }
}
`
};

function loadExample(language) {
    editor.setValue(examples[language]);
    document.getElementById('language').value = language;
    
    // Update CodeMirror mode
    const modes = {
        python: 'python',
        javascript: 'javascript',
        java: 'text/x-java'
    };
    editor.setOption('mode', modes[language]);
}

async function analyzeCode() {
    const code = editor.getValue();
    const language = document.getElementById('language').value;
    
    if (!code.trim()) {
        alert('Please enter some code to analyze');
        return;
    }
    
    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('analyze-btn').disabled = true;
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                language: language || null
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('analyze-btn').disabled = false;
    }
}

function displayResults(data) {
    // Show results section
    document.getElementById('results').classList.remove('hidden');
    
    // Update summary cards
    const riskLevel = data.risk_matrix.risk_level;
    const riskColors = {
        'CRITICAL': 'text-red-600',
        'HIGH': 'text-orange-600',
        'MEDIUM': 'text-yellow-600',
        'LOW': 'text-green-600'
    };
    
    document.getElementById('risk-level').textContent = riskLevel;
    document.getElementById('risk-level').className = `text-2xl font-bold ${riskColors[riskLevel]}`;
    document.getElementById('total-issues').textContent = data.risk_matrix.summary.total_issues;
    document.getElementById('loc').textContent = data.code_metrics.lines_of_code;
    document.getElementById('complexity').textContent = data.code_metrics.cyclomatic_complexity;
    
    // Update counts
    document.getElementById('count-security').textContent = data.findings.security_issues.length;
    document.getElementById('count-dead-code').textContent = data.findings.dead_code.length;
    document.getElementById('count-optimization').textContent = data.findings.optimizations.length;
    
    // Display risk matrix chart
    displayRiskMatrix(data.risk_matrix);
    
    // Display recommendations
    const recList = document.getElementById('recommendations');
    recList.innerHTML = '';
    data.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.className = 'text-gray-700';
        li.textContent = rec;
        recList.appendChild(li);
    });
    
    // Display findings
    displayFindings('security', data.findings.security_issues);
    displayFindings('dead-code', data.findings.dead_code);
    displayFindings('optimization', data.findings.optimizations);
    
    // Show first tab
    showTab('security');
}

function displayRiskMatrix(riskMatrix) {
    const ctx = document.getElementById('risk-chart').getContext('2d');
    
    // Destroy existing chart
    if (riskChart) {
        riskChart.destroy();
    }
    
    // Prepare data
    const datasets = {
        security: { label: 'Security', data: [], backgroundColor: '#dc2626' },
        dead_code: { label: 'Dead Code', data: [], backgroundColor: '#f59e0b' },
        optimization: { label: 'Optimization', data: [], backgroundColor: '#10b981' }
    };
    
    riskMatrix.matrix_data.forEach(point => {
        datasets[point.category].data.push({
            x: point.likelihood,
            y: point.severity,
            r: 10,
            title: point.title
        });
    });
    
    // Create chart
    riskChart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: Object.values(datasets).filter(ds => ds.data.length > 0)
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Risk Matrix: Severity vs Likelihood'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw.title;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Likelihood (1-5)'
                    },
                    min: 0,
                    max: 6,
                    ticks: {
                        stepSize: 1
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Severity (1-5)'
                    },
                    min: 0,
                    max: 6,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

function displayFindings(category, findings) {
    const container = document.getElementById(`findings-${category}`);
    container.innerHTML = '';
    
    if (findings.length === 0) {
        container.innerHTML = '<p class="text-gray-500">No issues found in this category.</p>';
        return;
    }
    
    const severityColors = {
        critical: 'bg-red-100 text-red-800 border-red-200',
        high: 'bg-orange-100 text-orange-800 border-orange-200',
        medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
        low: 'bg-green-100 text-green-800 border-green-200'
    };
    
    findings.forEach(finding => {
        const div = document.createElement('div');
        div.className = `border-l-4 p-4 mb-4 ${severityColors[finding.severity]}`;
        
        div.innerHTML = `
            <div class="flex justify-between items-start mb-2">
                <div class="font-semibold">${finding.type.replace(/_/g, ' ').toUpperCase()}</div>
                <div class="text-sm">Line ${finding.line}</div>
            </div>
            <div class="text-sm mb-2">${finding.message}</div>
            <div class="bg-gray-800 text-gray-100 p-2 rounded text-sm font-mono overflow-x-auto">
                ${escapeHtml(finding.code)}
            </div>
            ${finding.cwe ? `<div class="text-xs mt-2 text-gray-600">${finding.cwe}</div>` : ''}
        `;
        
        container.appendChild(div);
    });
}

function showTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('border-blue-600', 'text-blue-600');
        btn.classList.add('border-transparent', 'text-gray-600');
    });
    
    document.getElementById(`tab-${tabName}`).classList.remove('border-transparent', 'text-gray-600');
    document.getElementById(`tab-${tabName}`).classList.add('border-blue-600', 'text-blue-600');
    
    // Show/hide content
    document.querySelectorAll('.findings-tab').forEach(tab => {
        tab.classList.add('hidden');
    });
    
    document.getElementById(`findings-${tabName}`).classList.remove('hidden');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Made with Bob
