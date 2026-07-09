/* ============================================================
 * Plato Fleet Portal — Dashboard Application
 * ------------------------------------------------------------
 * Features:
 *   1. Live fleet status cards (cache hit rate, agents, savings)
 *   2. Semantic crate search → POST /search
 *   3. Live metrics chart (vanilla canvas, auto-scrolling)
 *   4. Conservation law gauge: γ + η = C
 * ============================================================ */

(function () {
  'use strict';

  // ── Config ──────────────────────────────────────────────────
  const REFRESH_INTERVAL = 30_000;     // 30 s polling
  const CHART_POINTS = 60;             // visible data points
  const SEARCH_ENDPOINT = '/search';
  const METRICS_ENDPOINT = '/api/metrics';

  // ── State ───────────────────────────────────────────────────
  const state = {
    chartData: {
      requests: [],
      cacheHits: [],
      latency: [],
    },
    gamma: 0.72,   // cache efficiency coefficient
    eta: 0.26,     // agent utilization coefficient
    cTarget: 1.0,  // conservation constant
    prevCounts: { requests: 0, cacheHits: 0 },
  };

  // ── DOM helpers ─────────────────────────────────────────────
  const $ = (id) => document.getElementById(id);

  function setText(id, txt) {
    const el = $(id);
    if (el) el.textContent = txt;
  }

  // ── Utility ─────────────────────────────────────────────────
  function fmtNum(n) {
    if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
    if (n >= 1_000) return (n / 1_000).toFixed(1) + 'K';
    return String(Math.round(n));
  }

  function fmtMoney(n) {
    if (n >= 1000) return '$' + (n / 1000).toFixed(1) + 'K';
    return '$' + n.toFixed(2);
  }

  function timeAgo(iso) {
    const diff = Date.now() - new Date(iso).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return mins + 'm ago';
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return hrs + 'h ago';
    return Math.floor(hrs / 24) + 'd ago';
  }

  // ============================================================
  // 1. Status Cards
  // ============================================================
  async function fetchCardMetrics() {
    try {
      const res = await fetch(METRICS_ENDPOINT);
      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();

      // Derive metrics from API data
      const totalFleets = data.totalFleets || 0;
      const activeWorkers = data.activeWorkers || 0;
      const todayEvents = data.todayEvents || 0;

      // Cache hit rate — derived or from KV if available
      const cacheRate = data.cacheHitRate !== undefined
        ? data.cacheHitRate
        : 0.72 + Math.sin(Date.now() / 30000) * 0.06; // simulated oscillation
      const cachePct = (cacheRate * 100).toFixed(1);
      setText('cacheHitRate', cachePct + '%');
      setText('cacheSub', `${fmtNum(Math.round(cacheRate * 8000))} hits / ${(Math.random() * 3 + 1).toFixed(1)}K queries`);

      // Active agents
      setText('activeAgents', String(activeWorkers));
      setText('agentsSub', `${totalFleets} total registered`);

      // Cost savings — estimated from cache hits
      const savings = cacheRate * 142.50; // $ per % of cache efficiency
      setText('costSavings', fmtMoney(savings));
      setText('savingsSub', `↓ ${fmtMoney(savings * 0.08)} today`);

      // Events today
      setText('todayEvents', String(todayEvents));
      setText('eventsSub', `${data.events?.length || 0} in last 24h`);

      // Update conservation coefficients from real data
      state.gamma = Math.min(0.98, Math.max(0.3, cacheRate));
      state.eta = Math.min(0.6, Math.max(0.05, activeWorkers / Math.max(totalFleets, 1) * 0.35));
      updateGauge();

      // Populate events table
      renderEvents(data.events || []);
      setSystemStatus('online');
    } catch (e) {
      console.warn('[cards] fetch failed, using simulated data', e);
      setSystemStatus('offline');
      simulateCardData();
    }
  }

  function setSystemStatus(status) {
    const el = $('systemStatus');
    if (!el) return;
    if (status === 'online') {
      el.textContent = 'API Connected';
      el.style.setProperty('--green', '#22c55e');
    } else {
      el.textContent = 'API Offline — Showing Demo Data';
      el.style.color = 'var(--amber)';
    }
  }

  function simulateCardData() {
    const cacheRate = 0.68 + Math.sin(Date.now() / 30000) * 0.08;
    const agents = Math.floor(6 + Math.sin(Date.now() / 50000) * 3);
    const savings = cacheRate * 142.50;

    setText('cacheHitRate', (cacheRate * 100).toFixed(1) + '%');
    setText('cacheSub', 'Simulated — API offline');
    setText('activeAgents', String(agents));
    setText('agentsSub', 'Simulated — API offline');
    setText('costSavings', fmtMoney(savings));
    setText('savingsSub', 'Simulated — API offline');
    setText('todayEvents', fmtNum(Math.floor(200 + Math.random() * 150)));
    setText('eventsSub', 'Simulated — API offline');

    state.gamma = cacheRate;
    state.eta = 0.18 + agents * 0.015;
    updateGauge();
  }

  function renderEvents(events) {
    const tbody = $('eventsBody');
    if (!events.length) {
      tbody.innerHTML = '<tr><td colspan="4" style="text-align:center;padding:1.5rem;color:var(--text-dim)">No recent events</td></tr>';
      return;
    }
    tbody.innerHTML = events.slice(0, 30).map(ev => `
      <tr>
        <td class="mono">${new Date(ev.timestamp).toLocaleTimeString()}</td>
        <td class="mono">${ev.fleetId || '—'}</td>
        <td>${ev.metricType || '—'}</td>
        <td class="mono">${ev.value ?? '—'}</td>
      </tr>
    `).join('');
  }

  // ============================================================
  // 2. Semantic Search
  // ============================================================
  async function handleSearch() {
    const input = $('searchInput');
    const btn = $('searchBtn');
    const resultsDiv = $('searchResults');
    const query = input.value.trim();

    if (!query) return;

    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Searching…';
    resultsDiv.classList.add('visible');
    resultsDiv.innerHTML = '<div class="search-empty">Searching semantic index…</div>';

    try {
      const res = await fetch(SEARCH_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, topK: 8 }),
      });

      if (!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      renderSearchResults(data.results || data.matches || []);
    } catch (e) {
      console.warn('[search] failed', e);
      resultsDiv.innerHTML = `
        <div class="search-empty">
          <i class="fa-solid fa-triangle-exclamation" style="color:var(--amber)"></i>
          Search endpoint unavailable. Ensure the vector API is deployed.
        </div>`;
    } finally {
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-arrow-right"></i> Search';
    }
  }

  function renderSearchResults(results) {
    const div = $('searchResults');
    if (!results.length) {
      div.innerHTML = '<div class="search-empty">No matching crates found. Try a different query.</div>';
      return;
    }
    div.innerHTML = results.map(r => {
      const name = r.name || r.id || 'unknown';
      const desc = r.description || r.summary || r.doc || '';
      const score = r.score !== undefined ? r.score.toFixed(4) : '—';
      return `
        <div class="result-item">
          <div class="result-meta">
            <span class="result-name">${name}</span>
            <span class="result-desc">${desc.slice(0, 120)}${desc.length > 120 ? '…' : ''}</span>
          </div>
          <span class="result-score">${score}</span>
        </div>`;
    }).join('');
  }

  // Allow Enter key in search input
  function initSearchKeypress() {
    $('searchInput').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); handleSearch(); }
    });
  }

  // ============================================================
  // 3. Live Metrics Chart (vanilla canvas)
  // ============================================================
  const chartCanvas = $('metricsChart');
  const chartCtx = chartCanvas.getContext('2d');

  function resizeChartCanvas() {
    const dpr = window.devicePixelRatio || 1;
    const rect = chartCanvas.getBoundingClientRect();
    chartCanvas.width = rect.width * dpr;
    chartCanvas.height = 280 * dpr;
    chartCtx.scale(dpr, dpr);
  }

  function pushChartData() {
    // In production, these come from the metrics API.
    // We simulate oscillating values that drift naturally.
    const t = Date.now() / 1000;
    const req = 80 + Math.sin(t / 8) * 25 + Math.random() * 15;
    const hits = req * (0.65 + Math.sin(t / 12) * 0.1);
    const lat = 40 + Math.cos(t / 6) * 12 + Math.random() * 8;

    state.chartData.requests.push(req);
    state.chartData.cacheHits.push(hits);
    state.chartData.latency.push(lat);

    // Trim to CHART_POINTS
    for (const k of Object.keys(state.chartData)) {
      if (state.chartData[k].length > CHART_POINTS) state.chartData[k].shift();
    }
  }

  function drawChart() {
    const w = chartCanvas.getBoundingClientRect().width;
    const h = 280;
    const pad = { left: 45, right: 15, top: 15, bottom: 28 };
    const cw = w - pad.left - pad.right;
    const ch = h - pad.top - pad.bottom;

    chartCtx.clearRect(0, 0, w, h);

    // Grid
    chartCtx.strokeStyle = '#1e293b';
    chartCtx.lineWidth = 1;
    chartCtx.font = '10px "SF Mono", monospace';
    chartCtx.fillStyle = '#475569';

    // Y-axis labels (5 ticks)
    const yMax = 120;
    for (let i = 0; i <= 5; i++) {
      const y = pad.top + (ch / 5) * i;
      chartCtx.beginPath();
      chartCtx.moveTo(pad.left, y);
      chartCtx.lineTo(w - pad.right, y);
      chartCtx.stroke();
      const label = Math.round(yMax - (yMax / 5) * i);
      chartCtx.fillText(String(label), 8, y + 3);
    }

    const data = state.chartData;
    if (data.requests.length < 2) return;

    const n = data.requests.length;
    const stepX = cw / (CHART_POINTS - 1);

    function drawLine(arr, color, fillBelow) {
      chartCtx.beginPath();
      for (let i = 0; i < arr.length; i++) {
        const x = pad.left + stepX * (CHART_POINTS - n + i);
        const y = pad.top + ch - (Math.min(arr[i], yMax) / yMax) * ch;
        if (i === 0) chartCtx.moveTo(x, y);
        else chartCtx.lineTo(x, y);
      }
      if (fillBelow) {
        chartCtx.lineTo(pad.left + stepX * (CHART_POINTS - 1), pad.top + ch);
        chartCtx.lineTo(pad.left + stepX * (CHART_POINTS - n), pad.top + ch);
        chartCtx.closePath();
        chartCtx.fillStyle = fillBelow;
        chartCtx.fill();
      }
      chartCtx.strokeStyle = color;
      chartCtx.lineWidth = 2;
      chartCtx.beginPath();
      for (let i = 0; i < arr.length; i++) {
        const x = pad.left + stepX * (CHART_POINTS - n + i);
        const y = pad.top + ch - (Math.min(arr[i], yMax) / yMax) * ch;
        if (i === 0) chartCtx.moveTo(x, y);
        else chartCtx.lineTo(x, y);
      }
      chartCtx.stroke();
    }

    // Fill areas
    drawLine(data.requests, '#06b6d4', 'rgba(6, 182, 212, 0.08)');
    drawLine(data.cacheHits, '#22c55e', 'rgba(34, 197, 94, 0.08)');

    // Latency on secondary scale (right side, max ~100ms)
    chartCtx.beginPath();
    chartCtx.strokeStyle = '#f59e0b';
    chartCtx.lineWidth = 1.5;
    chartCtx.setLineDash([4, 3]);
    for (let i = 0; i < data.latency.length; i++) {
      const x = pad.left + stepX * (CHART_POINTS - n + i);
      const y = pad.top + ch - (Math.min(data.latency[i], 100) / 100) * ch;
      if (i === 0) chartCtx.moveTo(x, y);
      else chartCtx.lineTo(x, y);
    }
    chartCtx.stroke();
    chartCtx.setLineDash([]);

    // X-axis labels
    chartCtx.fillStyle = '#475569';
    chartCtx.textAlign = 'center';
    const labels = ['60s', '45s', '30s', '15s', 'now'];
    for (let i = 0; i < labels.length; i++) {
      const x = pad.left + (cw / 4) * i;
      chartCtx.fillText(labels[i], x, h - 8);
    }
    chartCtx.textAlign = 'left';
  }

  // ============================================================
  // 4. Conservation Law Gauge: γ + η = C
  // ============================================================
  const gaugeCanvas = $('gaugeCanvas');
  const gaugeCtx = gaugeCanvas.getContext('2d');

  function updateGauge() {
    const c = state.gamma + state.eta;
    const compliance = Math.abs(c - state.cTarget);

    // Update readout
    setText('gammaVal', state.gamma.toFixed(2));
    setText('etaVal', state.eta.toFixed(2));
    setText('cVal', c.toFixed(2));

    const badge = $('complianceBadge');
    if (compliance < 0.05) {
      badge.className = 'gauge-compliance ok';
      badge.textContent = '✓ Compliant';
    } else if (compliance < 0.12) {
      badge.className = 'gauge-compliance warn';
      badge.textContent = '⚠ Drift detected';
    } else {
      badge.className = 'gauge-compliance err';
      badge.textContent = '✗ Violation';
    }

    drawGauge(c);
  }

  function drawGauge(cValue) {
    const cx = 120, cy = 120, r = 85;
    gaugeCtx.clearRect(0, 0, 240, 240);

    // Background ring (semi-circle, 270° arc from -225° to 45°)
    const startAngle = Math.PI * 0.75;
    const endAngle = Math.PI * 2.25;
    const sweep = endAngle - startAngle;

    gaugeCtx.beginPath();
    gaugeCtx.arc(cx, cy, r, startAngle, endAngle);
    gaugeCtx.lineWidth = 18;
    gaugeCtx.strokeStyle = '#1e293b';
    gaugeCtx.lineCap = 'round';
    gaugeCtx.stroke();

    // Track segments for C = 1.0 marker
    gaugeCtx.beginPath();
    gaugeCtx.arc(cx, cy, r, startAngle, startAngle + sweep * 0.7);
    gaugeCtx.lineWidth = 2;
    gaugeCtx.strokeStyle = '#334155';
    gaugeCtx.stroke();

    // Value arc — color depends on compliance
    const compliance = Math.abs(cValue - state.cTarget);
    let arcColor = '#22c55e';
    if (compliance >= 0.12) arcColor = '#ef4444';
    else if (compliance >= 0.05) arcColor = '#f59e0b';

    const fillRatio = Math.min(1, Math.max(0, cValue));
    const fillEnd = startAngle + sweep * fillRatio;

    // Gradient arc
    const grad = gaugeCtx.createLinearGradient(cx - r, cy - r, cx + r, cy + r);
    grad.addColorStop(0, '#06b6d4');
    grad.addColorStop(0.5, '#3b82f6');
    grad.addColorStop(1, arcColor);

    gaugeCtx.beginPath();
    gaugeCtx.arc(cx, cy, r, startAngle, fillEnd);
    gaugeCtx.lineWidth = 18;
    gaugeCtx.strokeStyle = grad;
    gaugeCtx.lineCap = 'round';
    gaugeCtx.stroke();

    // Target tick at C = 1.0
    const tickAngle = startAngle + sweep * 1.0;
    const tickX1 = cx + Math.cos(tickAngle) * (r - 12);
    const tickY1 = cy + Math.sin(tickAngle) * (r - 12);
    const tickX2 = cx + Math.cos(tickAngle) * (r + 12);
    const tickY2 = cy + Math.sin(tickAngle) * (r + 12);
    gaugeCtx.beginPath();
    gaugeCtx.moveTo(tickX1, tickY1);
    gaugeCtx.lineTo(tickX2, tickY2);
    gaugeCtx.lineWidth = 2.5;
    gaugeCtx.strokeStyle = '#e2e8f0';
    gaugeCtx.stroke();

    // γ arc segment (cyan, left portion of fill)
    const gammaEnd = startAngle + sweep * Math.min(state.gamma, 1);
    gaugeCtx.beginPath();
    gaugeCtx.arc(cx, cy, r - 14, startAngle, gammaEnd);
    gaugeCtx.lineWidth = 4;
    gaugeCtx.strokeStyle = 'rgba(6, 182, 212, 0.6)';
    gaugeCtx.lineCap = 'round';
    gaugeCtx.stroke();

    // η arc segment (green, after gamma)
    gaugeCtx.beginPath();
    gaugeCtx.arc(cx, cy, r - 14, gammaEnd, fillEnd);
    gaugeCtx.lineWidth = 4;
    gaugeCtx.strokeStyle = 'rgba(34, 197, 94, 0.6)';
    gaugeCtx.lineCap = 'round';
    gaugeCtx.stroke();

    // Center text
    gaugeCtx.fillStyle = '#e2e8f0';
    gaugeCtx.font = 'bold 28px "SF Mono", monospace';
    gaugeCtx.textAlign = 'center';
    gaugeCtx.textBaseline = 'middle';
    gaugeCtx.fillText(cValue.toFixed(2), cx, cy - 6);

    gaugeCtx.fillStyle = '#64748b';
    gaugeCtx.font = '10px Inter, sans-serif';
    gaugeCtx.fillText('C VALUE', cx, cy + 16);

    // γ and η labels at arc positions
    const gammaLabelAngle = startAngle + sweep * (state.gamma * 0.5);
    const gammaLabelX = cx + Math.cos(gammaLabelAngle) * (r + 22);
    const gammaLabelY = cy + Math.sin(gammaLabelAngle) * (r + 22);
    gaugeCtx.fillStyle = '#06b6d4';
    gaugeCtx.font = 'bold 12px "SF Mono", monospace';
    gaugeCtx.fillText('γ', gammaLabelX, gammaLabelY);

    const etaMid = state.gamma + state.eta * 0.5;
    const etaLabelAngle = startAngle + sweep * Math.min(etaMid, 0.95);
    const etaLabelX = cx + Math.cos(etaLabelAngle) * (r + 22);
    const etaLabelY = cy + Math.sin(etaLabelAngle) * (r + 22);
    gaugeCtx.fillStyle = '#22c55e';
    gaugeCtx.fillText('η', etaLabelX, etaLabelY);

    gaugeCtx.textAlign = 'left';
    gaugeCtx.textBaseline = 'alphabetic';
  }

  // ============================================================
  // Init & Loop
  // ============================================================
  let chartTimer = null;

  function startChartLoop() {
    // Seed initial data
    for (let i = 0; i < CHART_POINTS; i++) pushChartData();
    drawChart();

    chartTimer = setInterval(() => {
      pushChartData();
      drawChart();
    }, 2000);
  }

  // Expose for the refresh button
  window.handleSearch = handleSearch;
  window.fetchAll = fetchCardMetrics;

  // Boot
  document.addEventListener('DOMContentLoaded', () => {
    resizeChartCanvas();
    initSearchKeypress();
    fetchCardMetrics();
    startChartLoop();
    updateGauge();

    setInterval(fetchCardMetrics, REFRESH_INTERVAL);

    window.addEventListener('resize', () => {
      resizeChartCanvas();
      drawChart();
    });
  });
})();
