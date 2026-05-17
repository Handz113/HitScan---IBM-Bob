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
    
    // Parse recommendations to extract severity and text
    const severityBadges = {
        'CRITICAL': '<span class="inline-flex items-center gap-1.5 px-3 py-1 bg-red-100 text-red-800 text-xs font-bold rounded-md"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>CRITICAL</span>',
        'HIGH': '<span class="inline-flex items-center gap-1.5 px-3 py-1 bg-orange-100 text-orange-800 text-xs font-bold rounded-md"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>HIGH</span>',
        'MEDIUM': '<span class="inline-flex items-center gap-1.5 px-3 py-1 bg-yellow-100 text-yellow-800 text-xs font-bold rounded-md"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>MEDIUM</span>',
        'LOW': '<span class="inline-flex items-center gap-1.5 px-3 py-1 bg-green-100 text-green-800 text-xs font-bold rounded-md"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>LOW</span>',
        'URGENT': '<span class="inline-flex items-center gap-1.5 px-3 py-1 bg-red-100 text-red-800 text-xs font-bold rounded-md"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>URGENT</span>'
    };
    
    data.recommendations.forEach(rec => {
        const div = document.createElement('div');
        div.className = 'flex items-start gap-3 p-3 border border-gray-200 rounded-lg mb-2 hover:bg-gray-50 transition-colors';
        
        // Try to extract severity from recommendation text
        let badge = '';
        let text = rec;
        
        for (const [severity, badgeHtml] of Object.entries(severityBadges)) {
            const pattern = new RegExp(`\\[${severity}\\]`, 'i');
            if (pattern.test(rec)) {
                badge = badgeHtml;
                text = rec.replace(pattern, '').trim();
                break;
            }
        }
        
        div.innerHTML = `
            ${badge}
            <span class="text-gray-700 flex-1">${text}</span>
        `;
        
        recList.appendChild(div);
    });
    
    // Display findings
    displayFindings('security', data.findings.security_issues);
    displayFindings('dead-code', data.findings.dead_code);
    displayFindings('optimization', data.findings.optimizations);
    
    // Display AI fix prompt
    currentRemediationPrompt = data.remediation_prompt;
    document.getElementById('ai-fix-prompt').textContent = data.remediation_prompt;
    
    // Show first tab
    showTab('security');
}

// Copy prompt to clipboard
function copyPromptToClipboard() {
    if (!currentRemediationPrompt) {
        alert('No prompt available to copy');
        return;
    }
    
    navigator.clipboard.writeText(currentRemediationPrompt).then(() => {
        // Show success feedback
        const button = event.target.closest('button');
        const originalText = button.innerHTML;
        button.innerHTML = `
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            Copied!
        `;
        button.classList.add('bg-green-600');
        button.classList.remove('bg-purple-600');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('bg-green-600');
            button.classList.add('bg-purple-600');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard. Please try selecting and copying manually.');
    });
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
    
    // Color scheme based on issue type and category
    const getIssueColors = (type, severity, category) => {
        // Security issues - red/pink tones
        if (category === 'security' || type.includes('injection') || type.includes('xss')) {
            return {
                bg: 'bg-red-50',
                border: 'border-red-200',
                text: 'text-red-800',
                title: 'text-red-900',
                icon: 'text-red-600'
            };
        }
        
        // Hardcoded secrets - beige/tan
        if (type.includes('secret') || type.includes('hardcoded')) {
            return {
                bg: 'bg-orange-50',
                border: 'border-orange-200',
                text: 'text-orange-800',
                title: 'text-orange-900',
                icon: 'text-orange-600'
            };
        }
        
        // Debug mode - light yellow
        if (type.includes('debug')) {
            return {
                bg: 'bg-yellow-50',
                border: 'border-yellow-200',
                text: 'text-yellow-800',
                title: 'text-yellow-900',
                icon: 'text-yellow-600'
            };
        }
        
        // Dead code (unused, unreachable) - light green/mint
        if (category === 'dead-code' || type.includes('unused') || type.includes('unreachable')) {
            return {
                bg: 'bg-green-50',
                border: 'border-green-200',
                text: 'text-green-800',
                title: 'text-green-900',
                icon: 'text-green-600'
            };
        }
        
        // Optimizations - light yellow
        if (category === 'optimization') {
            return {
                bg: 'bg-yellow-50',
                border: 'border-yellow-200',
                text: 'text-yellow-800',
                title: 'text-yellow-900',
                icon: 'text-yellow-600'
            };
        }
        
        // Default based on severity
        const severityColors = {
            critical: { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-800', title: 'text-red-900', icon: 'text-red-600' },
            high: { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-800', title: 'text-orange-900', icon: 'text-orange-600' },
            medium: { bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-800', title: 'text-yellow-900', icon: 'text-yellow-600' },
            low: { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-800', title: 'text-green-900', icon: 'text-green-600' }
        };
        
        return severityColors[severity] || severityColors.medium;
    };
    
    const getSeverityBadge = (severity) => {
        const badges = {
            critical: '<span class="px-3 py-1 bg-red-600 text-white text-xs font-bold rounded-md">CRITICAL</span>',
            high: '<span class="px-3 py-1 bg-orange-600 text-white text-xs font-bold rounded-md">HIGH</span>',
            medium: '<span class="px-3 py-1 bg-yellow-600 text-white text-xs font-bold rounded-md">MEDIUM</span>',
            low: '<span class="px-3 py-1 bg-green-600 text-white text-xs font-bold rounded-md">LOW</span>'
        };
        return badges[severity] || badges.medium;
    };
    
    findings.forEach(finding => {
        const colors = getIssueColors(finding.type.toLowerCase(), finding.severity, category);
        const div = document.createElement('div');
        div.className = `${colors.bg} border ${colors.border} rounded-lg p-4 mb-4`;
        
        div.innerHTML = `
            <div class="flex items-start gap-3 mb-3">
                <svg class="w-6 h-6 ${colors.icon} flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
                <div class="flex-1">
                    <div class="flex justify-between items-start mb-2">
                        <div class="font-bold ${colors.title} text-lg">${finding.type.replace(/_/g, ' ').toUpperCase()}</div>
                        <div class="flex items-center gap-2">
                            ${getSeverityBadge(finding.severity)}
                            <span class="text-sm ${colors.text}">Line ${finding.line}</span>
                        </div>
                    </div>
                    <div class="text-sm mb-3 ${colors.text}">${finding.message}</div>
                    <div class="bg-gray-900 text-gray-100 p-3 rounded-lg text-sm font-mono overflow-x-auto">
                        ${escapeHtml(finding.code)}
                    </div>
                    ${finding.cwe ? `<div class="text-xs mt-2 ${colors.text}">${finding.cwe}</div>` : ''}
                </div>
            </div>
        `;
        
        container.appendChild(div);
    });
}

function showTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('bg-white', 'text-gray-900', 'shadow-sm');
        btn.classList.add('text-gray-700');
    });
    
    const activeTab = document.getElementById(`tab-${tabName}`);
    activeTab.classList.remove('text-gray-700');
    activeTab.classList.add('bg-white', 'text-gray-900', 'shadow-sm');
    
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

// Store the current remediation prompt
let currentRemediationPrompt = '';
