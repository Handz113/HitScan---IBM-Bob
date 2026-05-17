// Repository Analysis JavaScript

let breakdownChart;
let repositoryFiles = [];
let currentRepoUrl = '';

async function listRepositoryFiles() {
    const repoUrl = document.getElementById('repo-url').value.trim();
    const maxFiles = parseInt(document.getElementById('max-files').value);
    
    // Validate input
    if (!repoUrl) {
        showError('Please enter a GitHub repository URL');
        return;
    }
    
    if (!repoUrl.includes('github.com')) {
        showError('Please enter a valid GitHub repository URL');
        return;
    }
    
    // Show loading, hide other sections
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('file-selection').classList.add('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    document.getElementById('list-btn').disabled = true;
    
    try {
        const response = await fetch('/list-repo-files', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                repo_url: repoUrl,
                max_files: maxFiles
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to list files');
        }
        
        // Store data
        repositoryFiles = data.files;
        currentRepoUrl = repoUrl;
        
        // Display file selection
        displayFileSelection(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('list-btn').disabled = false;
    }
}

function displayFileSelection(data) {
    const fileList = document.getElementById('file-list');
    const fileSelection = document.getElementById('file-selection');
    
    fileList.innerHTML = '';
    
    // Group files by directory
    const filesByDir = {};
    data.files.forEach(file => {
        const dir = file.path.includes('/') ? file.path.substring(0, file.path.lastIndexOf('/')) : 'root';
        if (!filesByDir[dir]) {
            filesByDir[dir] = [];
        }
        filesByDir[dir].push(file);
    });
    
    // Create checkboxes grouped by directory
    Object.keys(filesByDir).sort().forEach(dir => {
        const dirDiv = document.createElement('div');
        dirDiv.className = 'mb-3';
        
        const dirHeader = document.createElement('div');
        dirHeader.className = 'font-semibold text-gray-700 mb-2 text-sm';
        dirHeader.textContent = dir === 'root' ? '📁 Root' : `📁 ${dir}`;
        dirDiv.appendChild(dirHeader);
        
        filesByDir[dir].forEach(file => {
            const fileDiv = document.createElement('label');
            fileDiv.className = 'flex items-center p-2 hover:bg-gray-50 rounded cursor-pointer';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = file.path;
            checkbox.checked = true;
            checkbox.className = 'mr-3 h-4 w-4 text-blue-600 rounded';
            checkbox.onchange = updateSelectedCount;
            
            const fileName = file.path.split('/').pop();
            const langBadge = file.language ? 
                `<span class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs">${file.language}</span>` : '';
            const sizeBadge = `<span class="ml-2 text-xs text-gray-500">${formatFileSize(file.size)}</span>`;
            
            fileDiv.innerHTML = `
                ${checkbox.outerHTML}
                <span class="flex-1">
                    <span class="text-gray-800">${fileName}</span>
                    ${langBadge}
                    ${sizeBadge}
                </span>
            `;
            
            dirDiv.appendChild(fileDiv);
        });
        
        fileList.appendChild(dirDiv);
    });
    
    // Update counts
    document.getElementById('total-count').textContent = data.files.length;
    updateSelectedCount();
    
    // Show file selection and analyze button
    fileSelection.classList.remove('hidden');
    document.getElementById('analyze-btn').classList.remove('hidden');
}

function updateSelectedCount() {
    const checkboxes = document.querySelectorAll('#file-list input[type="checkbox"]');
    const selectedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
    document.getElementById('selected-count').textContent = selectedCount;
}

function selectAllFiles() {
    const checkboxes = document.querySelectorAll('#file-list input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = true);
    updateSelectedCount();
}

function selectNoneFiles() {
    const checkboxes = document.querySelectorAll('#file-list input[type="checkbox"]');
    checkboxes.forEach(cb => cb.checked = false);
    updateSelectedCount();
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

async function analyzeRepository() {
    const repoUrl = currentRepoUrl || document.getElementById('repo-url').value.trim();
    const maxFiles = parseInt(document.getElementById('max-files').value);
    
    // Get selected files
    const checkboxes = document.querySelectorAll('#file-list input[type="checkbox"]:checked');
    const selectedFiles = Array.from(checkboxes).map(cb => cb.value);
    
    // Validate
    if (selectedFiles.length === 0) {
        showError('Please select at least one file to analyze');
        return;
    }
    
    // Show loading, hide results and errors
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    document.getElementById('analyze-btn').disabled = true;
    
    try {
        const response = await fetch('/analyze-repo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                repo_url: repoUrl,
                max_files: maxFiles,
                selected_files: selectedFiles.length > 0 ? selectedFiles : null
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Analysis failed');
        }
        
        // Check for error in response
        if (data.error) {
            throw new Error(data.error);
        }
        
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('analyze-btn').disabled = false;
    }
}

function displayResults(data) {
    // Show results section
    document.getElementById('results').classList.remove('hidden');
    
    // Repository Info
    document.getElementById('repo-name').textContent = `${data.owner}/${data.repo_name}`;
    document.getElementById('files-count').textContent = data.files_analyzed;
    document.getElementById('languages').textContent = data.languages.join(', ');
    
    // Summary Cards
    const stats = data.aggregated_stats;
    document.getElementById('total-issues').textContent = stats.total_issues;
    document.getElementById('total-lines').textContent = stats.total_lines.toLocaleString();
    document.getElementById('issues-per-1k').textContent = stats.issues_per_1000_lines;
    document.getElementById('security-count').textContent = stats.breakdown.security;
    
    // Issue Breakdown Chart
    displayBreakdownChart(stats);
    
    // Most Problematic Files
    displayProblematicFiles(stats.most_problematic_files);
    
    // File Comparison Table
    displayFileComparison(data.file_comparison);
    
    // Detailed Findings by File
    displayFileDetails(data.file_results);
}

function displayBreakdownChart(stats) {
    const ctx = document.getElementById('breakdown-chart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (breakdownChart) {
        breakdownChart.destroy();
    }
    
    breakdownChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Dead Code', 'Security Issues', 'Optimizations'],
            datasets: [{
                label: 'Number of Issues',
                data: [
                    stats.breakdown.dead_code,
                    stats.breakdown.security,
                    stats.breakdown.optimization
                ],
                backgroundColor: [
                    'rgba(59, 130, 246, 0.5)',
                    'rgba(239, 68, 68, 0.5)',
                    'rgba(251, 191, 36, 0.5)'
                ],
                borderColor: [
                    'rgb(59, 130, 246)',
                    'rgb(239, 68, 68)',
                    'rgb(251, 191, 36)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

function displayProblematicFiles(files) {
    const container = document.getElementById('problematic-files');
    container.innerHTML = '';
    
    if (files.length === 0) {
        container.innerHTML = '<p class="text-gray-500">No problematic files found!</p>';
        return;
    }
    
    files.forEach((file, index) => {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'flex items-center justify-between p-4 bg-gray-50 rounded-lg';
        fileDiv.innerHTML = `
            <div class="flex-1">
                <div class="font-medium text-gray-800">${index + 1}. ${file.path}</div>
                <div class="text-sm text-gray-600 mt-1">
                    Dead Code: ${file.breakdown.dead_code} | 
                    Security: ${file.breakdown.security} | 
                    Optimization: ${file.breakdown.optimization}
                </div>
            </div>
            <div class="ml-4">
                <span class="px-3 py-1 bg-red-100 text-red-700 rounded-full font-semibold">
                    ${file.issues} issues
                </span>
            </div>
        `;
        container.appendChild(fileDiv);
    });
}

function displayFileComparison(comparison) {
    const tbody = document.getElementById('file-table');
    tbody.innerHTML = '';
    
    comparison.forEach(file => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50';
        
        // Color code based on issue density
        let densityColor = 'text-green-600';
        if (file.issues_per_100_lines > 5) densityColor = 'text-red-600';
        else if (file.issues_per_100_lines > 2) densityColor = 'text-yellow-600';
        
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${file.path}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${file.language}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${file.lines}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">${file.total_issues}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold ${densityColor}">${file.issues_per_100_lines}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm">
                <span class="text-blue-600">${file.dead_code}</span> / 
                <span class="text-red-600">${file.security}</span> / 
                <span class="text-yellow-600">${file.optimization}</span>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function displayFileDetails(fileResults) {
    const container = document.getElementById('file-details');
    container.innerHTML = '<h2 class="text-2xl font-bold text-gray-800 mb-4">Detailed Findings by File</h2>';
    
    fileResults.forEach(file => {
        const totalFindings = file.findings_count.dead_code + 
                            file.findings_count.security + 
                            file.findings_count.optimization;
        
        if (totalFindings === 0) return; // Skip files with no issues
        
        const fileDiv = document.createElement('div');
        fileDiv.className = 'bg-white rounded-lg shadow-md p-6';
        
        let findingsHtml = '';
        
        // Dead Code Findings
        if (file.findings.dead_code.length > 0) {
            findingsHtml += '<div class="mb-4"><h4 class="font-semibold text-blue-700 mb-2">Dead Code</h4><ul class="space-y-2">';
            file.findings.dead_code.forEach(finding => {
                findingsHtml += `
                    <li class="text-sm">
                        <span class="font-medium">${finding.category}:</span> ${finding.message}
                        ${finding.line ? ` (Line ${finding.line})` : ''}
                    </li>
                `;
            });
            findingsHtml += '</ul></div>';
        }
        
        // Security Findings
        if (file.findings.security_issues.length > 0) {
            findingsHtml += '<div class="mb-4"><h4 class="font-semibold text-red-700 mb-2">Security Issues</h4><ul class="space-y-2">';
            file.findings.security_issues.forEach(finding => {
                findingsHtml += `
                    <li class="text-sm">
                        <span class="font-medium">${finding.category}:</span> ${finding.message}
                        ${finding.line ? ` (Line ${finding.line})` : ''}
                    </li>
                `;
            });
            findingsHtml += '</ul></div>';
        }
        
        // Optimization Findings
        if (file.findings.optimizations.length > 0) {
            findingsHtml += '<div class="mb-4"><h4 class="font-semibold text-yellow-700 mb-2">Optimizations</h4><ul class="space-y-2">';
            file.findings.optimizations.forEach(finding => {
                findingsHtml += `
                    <li class="text-sm">
                        <span class="font-medium">${finding.category}:</span> ${finding.message}
                        ${finding.line ? ` (Line ${finding.line})` : ''}
                    </li>
                `;
            });
            findingsHtml += '</ul></div>';
        }
        
        fileDiv.innerHTML = `
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold text-gray-800">${file.path}</h3>
                <div class="flex gap-2">
                    <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs">${file.language}</span>
                    <span class="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">${file.lines} lines</span>
                    <span class="px-2 py-1 bg-red-100 text-red-700 rounded text-xs">${totalFindings} issues</span>
                </div>
            </div>
            ${findingsHtml}
        `;
        
        container.appendChild(fileDiv);
    });
}

function showError(message) {
    document.getElementById('error').classList.remove('hidden');
    document.getElementById('error-message').textContent = message;
    document.getElementById('results').classList.add('hidden');
}

// Made with Bob