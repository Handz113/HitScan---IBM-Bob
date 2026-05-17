// Repository Analysis JavaScript

let breakdownChart;
let currentRepoRemediationPrompt = '';

let repositoryFiles = [];
let currentRepoUrl = '';

// Security: HTML escaping function to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

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
    
    // Clear existing content safely
    fileList.textContent = '';
    
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
            
            // Create elements safely without innerHTML
            fileDiv.appendChild(checkbox);
            
            const span = document.createElement('span');
            span.className = 'flex-1';
            
            const fileNameSpan = document.createElement('span');
            fileNameSpan.className = 'text-gray-800';
            fileNameSpan.textContent = fileName;
            span.appendChild(fileNameSpan);
            
            if (file.language) {
                const langBadge = document.createElement('span');
                langBadge.className = 'ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs';
                langBadge.textContent = file.language;
                span.appendChild(langBadge);
            }
            
            const sizeBadge = document.createElement('span');
            sizeBadge.className = 'ml-2 text-xs text-gray-500';
            sizeBadge.textContent = formatFileSize(file.size);
            span.appendChild(sizeBadge);
            
            fileDiv.appendChild(span);
            
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
    
    // Display AI fix prompt
    currentRepoRemediationPrompt = data.remediation_prompt;
    document.getElementById('repo-fix-prompt').textContent = data.remediation_prompt;
    
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
    container.textContent = '';
    
    if (files.length === 0) {
        const p = document.createElement('p');
        p.className = 'text-gray-500';
        p.textContent = 'No problematic files found!';
        container.appendChild(p);
        return;
    }
    
    files.forEach((file, index) => {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'flex items-center justify-between p-4 bg-gray-50 rounded-lg';
        
        const leftDiv = document.createElement('div');
        leftDiv.className = 'flex-1';
        
        const pathDiv = document.createElement('div');
        pathDiv.className = 'font-medium text-gray-800';
        pathDiv.textContent = `${index + 1}. ${file.path}`;
        leftDiv.appendChild(pathDiv);
        
        const statsDiv = document.createElement('div');
        statsDiv.className = 'text-sm text-gray-600 mt-1';
        statsDiv.textContent = `Dead Code: ${file.breakdown.dead_code} | Security: ${file.breakdown.security} | Optimization: ${file.breakdown.optimization}`;
        leftDiv.appendChild(statsDiv);
        
        const rightDiv = document.createElement('div');
        rightDiv.className = 'ml-4';
        
        const badge = document.createElement('span');
        badge.className = 'px-3 py-1 bg-red-100 text-red-700 rounded-full font-semibold';
        badge.textContent = `${file.issues} issues`;
        rightDiv.appendChild(badge);
        
        fileDiv.appendChild(leftDiv);
        fileDiv.appendChild(rightDiv);
        container.appendChild(fileDiv);
    });
}

function displayFileComparison(comparison) {
    const tbody = document.getElementById('file-table');
    tbody.textContent = '';
    
    comparison.forEach(file => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-50';
        
        // Color code based on issue density
        let densityColor = 'text-green-600';
        if (file.issues_per_100_lines > 5) densityColor = 'text-red-600';
        else if (file.issues_per_100_lines > 2) densityColor = 'text-yellow-600';
        
        // Create cells safely
        const cells = [
            { text: file.path, className: 'px-6 py-4 whitespace-nowrap text-sm text-gray-900' },
            { text: file.language, className: 'px-6 py-4 whitespace-nowrap text-sm text-gray-500' },
            { text: file.lines, className: 'px-6 py-4 whitespace-nowrap text-sm text-gray-500' },
            { text: file.total_issues, className: 'px-6 py-4 whitespace-nowrap text-sm text-gray-900' },
            { text: file.issues_per_100_lines, className: `px-6 py-4 whitespace-nowrap text-sm font-semibold ${densityColor}` }
        ];
        
        cells.forEach(cellData => {
            const td = document.createElement('td');
            td.className = cellData.className;
            td.textContent = cellData.text;
            row.appendChild(td);
        });
        
        // Breakdown cell with colored spans
        const breakdownTd = document.createElement('td');
        breakdownTd.className = 'px-6 py-4 whitespace-nowrap text-sm';
        
        const deadSpan = document.createElement('span');
        deadSpan.className = 'text-blue-600';
        deadSpan.textContent = file.dead_code;
        breakdownTd.appendChild(deadSpan);
        breakdownTd.appendChild(document.createTextNode(' / '));
        
        const secSpan = document.createElement('span');
        secSpan.className = 'text-red-600';
        secSpan.textContent = file.security;
        breakdownTd.appendChild(secSpan);
        breakdownTd.appendChild(document.createTextNode(' / '));
        
        const optSpan = document.createElement('span');
        optSpan.className = 'text-yellow-600';
        optSpan.textContent = file.optimization;
        breakdownTd.appendChild(optSpan);
        
        row.appendChild(breakdownTd);
        tbody.appendChild(row);
    });
}

function displayFileDetails(fileResults) {
    const container = document.getElementById('file-details');
    container.textContent = '';
    
    const title = document.createElement('h2');
    title.className = 'text-2xl font-bold text-gray-800 mb-4';
    title.textContent = 'Detailed Findings by File';
    container.appendChild(title);
    
    fileResults.forEach(file => {
        const totalFindings = file.findings_count.dead_code +
                            file.findings_count.security +
                            file.findings_count.optimization;
        
        if (totalFindings === 0) return; // Skip files with no issues
        
        const fileDiv = document.createElement('div');
        fileDiv.className = 'bg-white rounded-lg shadow-md p-6';
        
        // Header section
        const headerDiv = document.createElement('div');
        headerDiv.className = 'flex items-center justify-between mb-4';
        
        const h3 = document.createElement('h3');
        h3.className = 'text-lg font-semibold text-gray-800';
        h3.textContent = file.path;
        headerDiv.appendChild(h3);
        
        const badgesDiv = document.createElement('div');
        badgesDiv.className = 'flex gap-2';
        
        const langBadge = document.createElement('span');
        langBadge.className = 'px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs';
        langBadge.textContent = file.language;
        badgesDiv.appendChild(langBadge);
        
        const linesBadge = document.createElement('span');
        linesBadge.className = 'px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs';
        linesBadge.textContent = `${file.lines} lines`;
        badgesDiv.appendChild(linesBadge);
        
        const issuesBadge = document.createElement('span');
        issuesBadge.className = 'px-2 py-1 bg-red-100 text-red-700 rounded text-xs';
        issuesBadge.textContent = `${totalFindings} issues`;
        badgesDiv.appendChild(issuesBadge);
        
        headerDiv.appendChild(badgesDiv);
        fileDiv.appendChild(headerDiv);
        
        // Helper function to create findings section
        function createFindingsSection(findings, title, colorClass) {
            if (findings.length === 0) return null;
            
            const sectionDiv = document.createElement('div');
            sectionDiv.className = 'mb-4';
            
            const h4 = document.createElement('h4');
            h4.className = `font-semibold ${colorClass} mb-2`;
            h4.textContent = title;
            sectionDiv.appendChild(h4);
            
            const ul = document.createElement('ul');
            ul.className = 'space-y-2';
            
            findings.forEach(finding => {
                const li = document.createElement('li');
                li.className = 'text-sm';
                
                const categorySpan = document.createElement('span');
                categorySpan.className = 'font-medium';
                categorySpan.textContent = `${finding.category}:`;
                li.appendChild(categorySpan);
                
                li.appendChild(document.createTextNode(` ${finding.message}`));
                
                if (finding.line) {
                    li.appendChild(document.createTextNode(` (Line ${finding.line})`));
                }
                
                ul.appendChild(li);
            });
            
            sectionDiv.appendChild(ul);
            return sectionDiv;
        }
        
        // Add findings sections
        const deadCodeSection = createFindingsSection(file.findings.dead_code, 'Dead Code', 'text-blue-700');
        if (deadCodeSection) fileDiv.appendChild(deadCodeSection);
        
        const securitySection = createFindingsSection(file.findings.security_issues, 'Security Issues', 'text-red-700');
        if (securitySection) fileDiv.appendChild(securitySection);
        
        const optimizationSection = createFindingsSection(file.findings.optimizations, 'Optimizations', 'text-yellow-700');
        if (optimizationSection) fileDiv.appendChild(optimizationSection);
        
        container.appendChild(fileDiv);
    });
}

function showError(message) {
    document.getElementById('error').classList.remove('hidden');
    document.getElementById('error-message').textContent = message;
    document.getElementById('results').classList.add('hidden');
}

// Made with Bob