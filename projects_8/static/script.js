const resultArea = document.getElementById('result-area');

function showLoading() {
    resultArea.innerHTML = '<div class="loading">⏳ Загрузка...</div>';
}

function showError(msg) {
    resultArea.innerHTML = `<div class="error">❌ Ошибка: ${msg}</div>`;
}

function displayStat(data) {
    const names = {
        mean: 'Средний балл',
        median: 'Медиана',
        total: 'Количество оценок',
        std: 'Стандартное отклонение',
        max: 'Максимальная оценка'
    };
    let val = data.metric === 'total' ? Math.round(data.value) : data.value.toFixed(2);
    resultArea.innerHTML = `
        <div class="stat-card">
            <div class="label">${names[data.metric]}</div>
            <div class="value">${val}</div>
        </div>
    `;
}

function displayChart(url) {
    resultArea.innerHTML = `<div class="chart-container"><img src="${url}?t=${Date.now()}" alt="График"></div>`;
}

async function fetchStat(metric) {
    showLoading();
    try {
        let res = await fetch(`/api/stat/${metric}`);
        let data = await res.json();
        if (data.status === 'error') throw new Error(data.message);
        displayStat(data);
    } catch (e) {
        showError(e.message);
    }
}

async function fetchChart(kind) {
    showLoading();
    try {
        let res = await fetch(`/api/chart/${kind}`, { method: 'HEAD' });
        if (!res.ok) throw new Error('График не доступен');
        displayChart(`/api/chart/${kind}`);
    } catch (e) {
        showError(e.message);
    }
}

document.querySelectorAll('[data-action="stat"]').forEach(btn => {
    btn.onclick = () => fetchStat(btn.dataset.metric);
});

document.querySelectorAll('[data-action="chart"]').forEach(btn => {
    btn.onclick = () => fetchChart(btn.dataset.kind);
});

document.getElementById('clear-btn').onclick = () => {
    resultArea.innerHTML = '<div class="placeholder">← Нажмите кнопку слева</div>';
};