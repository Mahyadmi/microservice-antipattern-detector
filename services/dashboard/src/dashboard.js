const API_URL = '/api';
let selectedProject = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initializing...');
    animateMetrics();
    setupDatasetSelection();
});

function animateMetrics() {
    // Your REAL validated metrics
    const metrics = [
        { element: document.querySelector('.metric-value[data-value="100"]'), value: 100 },    // Precision
        { element: document.querySelector('.metric-value[data-value="66.7"]'), value: 66.7 },  // Recall
        { element: document.querySelector('.metric-value[data-value="80"]'), value: 80 },      // F1-Score
        { element: document.querySelector('.metric-value[data-value="40"]'), value: 40 }       // Cost Reduction
    ];
    
    metrics.forEach(metric => {
        if (metric.element) {
            let current = 0;
            const increment = metric.value / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= metric.value) {
                    current = metric.value;
                    clearInterval(timer);
                }
                metric.element.textContent = current % 1 === 0 ? `${current}%` : `${current.toFixed(1)}%`;
            }, 30);
        }
    });
}

function setupDatasetSelection() {
    const options = document.querySelectorAll('.dataset-option');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    options.forEach(option => {
        option.style.cursor = 'pointer';
        option.addEventListener('click', function() {
            options.forEach(opt => opt.classList.remove('selected'));
            this.classList.add('selected');
            selectedProject = this.dataset.project;
            analyzeBtn.disabled = false;
            analyzeBtn.querySelector('.btn-text').textContent = `Analyze ${selectedProject}`;
        });
    });
}

async function startAnalysis() {
    if (!selectedProject) return;
    
    const btn = document.getElementById('analyzeBtn');
    btn.classList.add('loading');
    btn.disabled = true;
    
    document.getElementById('results-section').style.display = 'block';
    document.getElementById('results-loading').style.display = 'block';
    document.getElementById('results-content').style.display = 'none';
    
    try {
        const response = await fetch(`${API_URL}/analysis`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({project_name: selectedProject})
        });
        
        const data = await response.json();
        const analysisId = data.analysis_id;
        
        setTimeout(async () => {
            const resultsResponse = await fetch(`${API_URL}/analysis/${analysisId}/results`);
            const results = await resultsResponse.json();
            displayResults(results);
            btn.classList.remove('loading');
            btn.disabled = false;
        }, 5000);
        
    } catch (error) {
        console.error('Analysis failed:', error);
        btn.classList.remove('loading');
        btn.disabled = false;
    }
}

function displayResults(results) {
    const container = document.getElementById('results-content');
    container.innerHTML = '';
    
    if (results.anti_patterns && results.anti_patterns.length > 0) {
        results.anti_patterns.forEach(pattern => {
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
        });
    }
    
    document.getElementById('results-loading').style.display = 'none';
    document.getElementById('results-content').style.display = 'block';
}
