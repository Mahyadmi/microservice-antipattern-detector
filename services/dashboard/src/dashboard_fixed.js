// ... (keep all the existing code until the displayResults function)

function displayResults(results) {
    const container = document.getElementById('results-content');
    const summary = document.getElementById('results-summary');
    
    // IMPORTANT: Clear previous results first
    container.innerHTML = '';
    
    // Create summary
    summary.innerHTML = `
        <h3>Analysis Complete</h3>
        <p>Detected ${results.anti_patterns.length} anti-patterns across ${Object.keys(results.metrics.tool_distribution).length} analysis tools.</p>
    `;
    
    // Create detailed results - only once, no duplicates
    results.anti_patterns.forEach((pattern, index) => {
        setTimeout(() => {
            const item = document.createElement('div');
            item.className = `anti-pattern-item severity-${pattern.severity}`;
            item.innerHTML = `
                <div class="pattern-header">
                    <span class="pattern-type">${pattern.type.replace(/_/g, ' ')}</span>
                    <span class="pattern-severity">${pattern.severity}</span>
                </div>
                <div style="color: #64748b; margin: 10px 0;">
                    <strong>Tool:</strong> ${pattern.tool} | 
                    <strong>Location:</strong> ${pattern.file}:${pattern.line}
                </div>
                <div style="margin: 10px 0;">${pattern.description}</div>
                <div style="color: #10b981; font-style: italic;">
                    💡 ${pattern.recommendation}
                </div>
            `;
            container.appendChild(item);
        }, index * 100);
    });
}

// ... (rest of the code remains the same)
