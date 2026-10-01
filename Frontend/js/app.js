const passwordInput = document.getElementById('password-input');
const togglePwBtn = document.getElementById('toggle-pw');
const scoreVal = document.getElementById('score-val');
const classificationBadge = document.getElementById('classification-badge');
const progressFill = document.getElementById('progress-fill');
const findingsList = document.getElementById('findings-list');
const suggestionsList = document.getElementById('suggestions-list');
const generateBtn = document.getElementById('generate-btn');
const generatedOutput = document.getElementById('generated-output');

const mLength = document.getElementById('m-length');
const mRatio = document.getElementById('m-ratio');
const mEntropy = document.getElementById('m-entropy');

const statTotal = document.getElementById('stat-total');
const statAvg = document.getElementById('stat-avg');

const ctxName = document.getElementById('ctx-name');
const ctxYear = document.getElementById('ctx-year');

togglePwBtn.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        togglePwBtn.textContent = 'Hide';
    } else {
        passwordInput.type = 'password';
        togglePwBtn.textContent = 'Show';
    }
});

async function analyzePassword() {
    const password = passwordInput.value;
    const context = {
        name: ctxName.value,
        year: ctxYear.value
    };

    try {
        const response = await fetch('http://localhost:5000/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password, context })
        });
        const data = await response.json();
        updateUI(data);
        fetchStats();
    } catch (err) {
        console.error("Backend offline or error:", err);
    }
}

function updateUI(data) {
    scoreVal.textContent = data.score;
    classificationBadge.textContent = data.classification;
    progressFill.style.width = `${data.score}%`;

    // Color coding progress bar
    if (data.score <= 40) progressFill.style.background = '#ef4444';
    else if (data.score <= 60) progressFill.style.background = '#f59e0b';
    else progressFill.style.background = '#10b981';

    mLength.textContent = data.metrics.length;
    mRatio.textContent = data.metrics.unique_character_ratio;
    mEntropy.textContent = data.metrics.entropy_bits;

    findingsList.innerHTML = data.findings.length ? data.findings.map(f => `<li>${f}</li>`).join('') : '<li>No major weaknesses detected.</li>';
    suggestionsList.innerHTML = data.suggestions.length ? data.suggestions.map(s => `<li>${s}</li>`).join('') : '<li>Password looks solid!</li>';
}

passwordInput.addEventListener('input', analyzePassword);
ctxName.addEventListener('input', analyzePassword);
ctxYear.addEventListener('input', analyzePassword);

generateBtn.addEventListener('click', async () => {
    const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ length: 20 })
    });
    const data = await response.json();
    generatedOutput.value = data.generated_password;
});

async function fetchStats() {
    try {
        const res = await fetch('http://localhost:5000/api/dashboard/stats');
        const stats = await res.json();
        statTotal.textContent = stats.total_analyses;
        statAvg.textContent = stats.average_score;
    } catch (err) {
        console.error("Failed to fetch dashboard stats");
    }
}

fetchStats();
