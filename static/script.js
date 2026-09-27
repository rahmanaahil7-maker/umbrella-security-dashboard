let searchChart = null;
let latestAnalysis = null;
let latestBench = null;
let authMode = 'login';

document.addEventListener("DOMContentLoaded", () => {
    checkAuthStatus();
    initChart();
});

async function checkAuthStatus() {
    try {
        const res = await fetch('/api/auth/status');
        const data = await res.json();
        const badge = document.getElementById('userBadge');
        const btn = document.getElementById('loginModalBtn');
        if (data.authenticated) {
            badge.innerText = `SYS.STATUS: ${data.role.toUpperCase()} (${data.username})`;
            badge.className = "status-badge admin";
            btn.innerText = "TERMINATE SESSION";
            btn.onclick = logout;
        } else {
            badge.innerText = "SYS.STATUS: GUEST";
            badge.className = "status-badge guest";
            btn.innerText = "AUTHENTICATE";
            btn.onclick = toggleAuthModal;
        }
    } catch (e) {
        console.error("Auth status error", e);
    }
}

function toggleAuthModal() {
    document.getElementById('authModal').classList.toggle('hidden');
}

function switchAuthTab(mode) {
    authMode = mode;
    document.getElementById('tabLogin').classList.toggle('active', mode === 'login');
    document.getElementById('tabRegister').classList.toggle('active', mode === 'register');
    document.getElementById('authTitle').innerText = mode === 'login' ? "SECURE LOGIN" : "ISSUE CLEARANCE";
}

async function submitAuth() {
    const username = document.getElementById('modalUser').value.trim();
    const password = document.getElementById('modalPass').value.trim();
    if (!username || !password) {
        alert("Credentials required.");
        return;
    }
    const endpoint = authMode === 'login' ? '/api/auth/login' : '/api/auth/register';
    const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok && data.success) {
        toggleAuthModal();
        checkAuthStatus();
    } else {
        alert(data.message || "Authentication rejected by Red Queen.");
    }
}

async function logout() {
    await fetch('/api/auth/logout', { method: 'POST' });
    checkAuthStatus();
}

function initChart() {
    const ctx = document.getElementById('searchSpaceChart').getContext('2d');
    Chart.defaults.color = '#666666';
    Chart.defaults.font.family = "'JetBrains Mono', monospace";
    
    searchChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            datasets: [{
                label: 'Combinatorial Expansion',
                data: [62, 3844, 238328, 14776336, 916132832, 5.68e10, 3.52e12, 2.18e14, 1.35e16, 8.39e17],
                borderColor: '#e60000',
                backgroundColor: 'rgba(230, 0, 0, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.2,
                pointBackgroundColor: '#030303',
                pointBorderColor: '#e60000'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { type: 'logarithmic', grid: { color: '#222222' } },
                x: { grid: { color: '#222222' } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

async function runCompletePipeline() {
    const password = document.getElementById('targetPassword').value.trim();
    const algorithm = document.getElementById('algoSelect').value;
    if (!password) { alert("Payload required."); return; }

    const runBtn = document.getElementById('runPipelineBtn');
    runBtn.disabled = true;

    // Red Queen Interface Output
    document.getElementById('aiConsole').innerText = "> Initializing Red Queen heuristics...\n> Establishing secure link to generative core...";
    document.getElementById('attackConsole').innerText = "> Allocating Hive multithreaded worker nodes...\n> Bypassing thermal limits...";
    const verdictEl = document.getElementById('kpiVerdict');
    verdictEl.innerText = "PROCESSING";
    verdictEl.className = "value";

    try {
        // 1. Static & Markov
        const analyzeRes = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password, algorithm })
        });
        latestAnalysis = await analyzeRes.json();

        document.getElementById('kpiEntropy').innerText = `${latestAnalysis.entropy} bits`;
        document.getElementById('kpiPerplexity').innerText = `${latestAnalysis.ml.perplexity}`;

        searchChart.data.labels = latestAnalysis.curve.map(c => `L-${c.length}`);
        searchChart.data.datasets[0].data = latestAnalysis.curve.map(c => c.space);
        searchChart.update();

        // 2. Parallel Attack
        const attackRes = await fetch('/api/attack_parallel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password, algorithm, max_length: 3 })
        });
        latestBench = await attackRes.json();
        latestBench.entropy = latestAnalysis.entropy;

        document.getElementById('kpiHashRate').innerText = `${latestBench.hash_rate.toLocaleString()} h/s`;
        
        if (latestBench.cracked) {
            verdictEl.innerText = "COMPROMISED";
            verdictEl.className = "value verdict-compromised";
        } else {
            verdictEl.innerText = "SECURE";
            verdictEl.className = "value verdict-secure";
        }

        document.getElementById('attackConsole').innerText = 
            `> TARGET HASH: ${latestAnalysis.hash}\n` +
            `> PROTOCOL: ${latestBench.algorithm.toUpperCase()}\n` +
            `> VECTORS EXPLORED: ${latestBench.attempts.toLocaleString()}\n` +
            `> CYCLE TIME: ${latestBench.time}s\n` +
            `> NODE THROUGHPUT: ${latestBench.hash_rate.toLocaleString()} hashes/sec\n\n` +
            `> RESULT: ${latestBench.cracked ? 'BREACH SUCCESSFUL (' + latestBench.found_password + ')' : 'BRUTE FORCE INEFFECTIVE IN GIVEN PARAMETERS'}`;

        document.getElementById('liveAlgo').innerText = latestBench.algorithm.toUpperCase();
        document.getElementById('liveRate').innerText = `${latestBench.hash_rate.toLocaleString()} h/s`;
        const exhaustSecs = (latestAnalysis.charset_pool ** 8) / Math.max(latestBench.hash_rate, 1);
        document.getElementById('liveExhaust').innerText = exhaustSecs > 31536000 ? `~${(exhaustSecs / 31536000).toFixed(1)} Years` : `~${(exhaustSecs / 60).toFixed(1)} Mins`;

        // 3. AI Heuristics
        const aiRes = await fetch('/api/ai_analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password })
        });
        const aiData = await aiRes.json();
        
        document.getElementById('aiConsole').innerText = 
            `> RED QUEEN ADVISORY (Mode: ${aiData.engine_mode})\n` +
            `> VULNERABILITY THREAT LEVEL: ${aiData.vulnerability_score}/10\n\n` +
            `> IDENTIFIED WEAKNESSES:\n` + aiData.identified_weaknesses.map(w => `  - ${w}`).join('\n') + `\n\n` +
            `> DIRECTIVE: ${aiData.expert_recommendation}`;

    } catch (err) {
        console.error(err);
        document.getElementById('attackConsole').innerText = "> FATAL SYSTEM EXCEPTION. CHECK CONSOLE.";
    } finally {
        runBtn.disabled = false;
    }
}

async function requestPdfReport() {
    if (!latestAnalysis || !latestBench) {
        alert("Execute audit before exporting intel.");
        return;
    }

    try {
        const res = await fetch('/api/generate_report', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                password: document.getElementById('targetPassword').value,
                bench_data: latestBench,
                ml_data: latestAnalysis.ml
            })
        });

        if (!res.ok) {
            alert("Report generation failed.");
            return;
        }

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "Umbrella_Security_Intel.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (e) {
        console.error("Export error", e);
    }
}