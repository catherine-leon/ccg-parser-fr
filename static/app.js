// Frontend léger 
// Il envoie la phrase au backend Python, puis affiche les dérivations retournées.

const COLORS = {
  'App>': '#c8f060', 'App<': '#c8f060',
  'Comp>B': '#60c8f0', 'Comp<B': '#60c8f0',
  '<*>': '#f0a060', 'TypeR': '#c060f0', error: '#f06060'
};

const RULE_LABELS = {
  'App>': '>', 'App<': '<',
  'Comp>B': '>B', 'Comp<B': '<B',
  '<*>': '<*>', TypeR: 'T'
};

let BASE_LEXIQUE = {};
let EXTRA_LEXIQUE = {};
let EXAMPLES = [];

function mergedLexique() {
  return { ...BASE_LEXIQUE, ...EXTRA_LEXIQUE };
}

function escapeHtml(str) {
  return String(str).replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
}

function renderExamples() {
  const exEl = document.getElementById('examples');
  exEl.innerHTML = '';
  for (const ex of EXAMPLES) {
    const btn = document.createElement('button');
    btn.className = 'example-chip';
    btn.textContent = ex;
    btn.onclick = () => {
      document.getElementById('phrase-input').value = ex;
      doParseAndRender();
    };
    exEl.appendChild(btn);
  }
}

function renderLex() {
  const el = document.getElementById('lex-list');
  el.innerHTML = '';
  for (const [word, cats] of Object.entries(mergedLexique())) {
    const item = document.createElement('div');
    item.className = 'lex-item';
    const isExtra = Object.prototype.hasOwnProperty.call(EXTRA_LEXIQUE, word);
    item.innerHTML = `
      <span class="word">${escapeHtml(word)}</span>
      <span class="cats">${escapeHtml(cats.join(' | '))}</span>
      ${isExtra ? `<button class="del-btn" data-word="${escapeHtml(word)}">×</button>` : `<span class="del-btn" style="opacity:.25">·</span>`}
    `;
    const del = item.querySelector('.del-btn[data-word]');
    if (del) {
      del.onclick = (e) => {
        delete EXTRA_LEXIQUE[e.target.dataset.word];
        renderLex();
      };
    }
    el.appendChild(item);
  }
}

function svgText(x, y, str, opts = {}) {
  const ns = 'http://www.w3.org/2000/svg';
  const el = document.createElementNS(ns, 'text');
  el.setAttribute('x', x);
  el.setAttribute('y', y);
  el.setAttribute('fill', opts.fill || '#e8e8ec');
  el.setAttribute('font-family', opts.mono ? 'JetBrains Mono, monospace' : 'Instrument Serif, serif');
  el.setAttribute('font-size', opts.size || 13);
  el.setAttribute('font-style', opts.italic ? 'italic' : 'normal');
  el.setAttribute('font-weight', opts.bold ? '700' : '400');
  el.setAttribute('text-anchor', opts.anchor || 'middle');
  el.textContent = str;
  return el;
}

function svgLine(x1, y1, x2, y2, color, dashed = false) {
  const ns = 'http://www.w3.org/2000/svg';
  const el = document.createElementNS(ns, 'line');
  el.setAttribute('x1', x1); el.setAttribute('y1', y1);
  el.setAttribute('x2', x2); el.setAttribute('y2', y2);
  el.setAttribute('stroke', color);
  el.setAttribute('stroke-width', 1.5);
  if (dashed) el.setAttribute('stroke-dasharray', '4,3');
  return el;
}

function svgArrow(x, y, dir, color) {
  const ns = 'http://www.w3.org/2000/svg';
  const el = document.createElementNS(ns, 'polygon');
  const size = 5;
  if (dir === 'R') el.setAttribute('points', `${x},${y} ${x-size},${y-3} ${x-size},${y+3}`);
  else el.setAttribute('points', `${x},${y} ${x+size},${y-3} ${x+size},${y+3}`);
  el.setAttribute('fill', color);
  return el;
}

function getFallbackCat(word) {
  const cats = mergedLexique()[word] || mergedLexique()[word.toLowerCase()];
  return cats && cats.length ? cats[0] : null;
}

function partialErrorMessage(analysis) {
  if (!analysis.partial || !analysis.path || analysis.path.length === 0) return null;
  for (let i = 0; i < analysis.path.length; i++) {
    if (!analysis.path[i].cat) return `catégorie inconnue sur [${analysis.path[i].i}-${analysis.path[i].j}]`;
  }
  if (analysis.path.length >= 2) {
    const a = analysis.path[analysis.path.length - 2];
    const b = analysis.path[analysis.path.length - 1];
    return `${a.cat} + ${b.cat}`;
  }
  return `${analysis.path[0].cat} ne donne pas S`;
}

function renderDerivation(mots, analysis) {
  const charW = 7.5;
  const minW = 80;
  const ROW_H = 38;
  const n = mots.length;
  const steps = analysis.steps || [];
  const wordCats = analysis.wordCats || {};
  const allCats = Object.values(wordCats);
  const maxLen = Math.max(4, ...allCats.map(s => s.length), ...mots.map(m => m.length));
  const W = Math.max(minW, Math.ceil(maxLen * charW) + 16);
  const svgH = (steps.length + 3) * ROW_H + 60;
  const svgW = n * W + 20;

  const ns = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('width', svgW);
  svg.setAttribute('height', svgH);
  svg.setAttribute('viewBox', `0 0 ${svgW} ${svgH}`);

  let curY = 28;
  for (let i = 0; i < n; i++) {
    const cx = i * W + W/2 + 10;
    svg.appendChild(svgText(cx, curY, mots[i], { bold: true, size: 14, mono: true }));
  }
  curY += ROW_H;

  for (let i = 0; i < n; i++) {
    const cx = i * W + W/2 + 10;
    const cat = wordCats[String(i)] || getFallbackCat(mots[i]) || '???';
    svg.appendChild(svgText(cx, curY, cat, { fill: '#9090a0', size: 11, mono: true }));
  }
  curY += ROW_H;

  for (const step of steps) {
    const color = COLORS[step.rule] || '#888';
    const label = RULE_LABELS[step.rule] || step.rule;
    const x1 = step.d * W + 10;
    const x2 = (step.f + 1) * W + 10;
    const mx = (x1 + x2) / 2;

    if (step.rule === 'App>' || step.rule === 'Comp>B') {
      svg.appendChild(svgLine(x1, curY - 6, x2 - 8, curY - 6, color));
      svg.appendChild(svgArrow(x2 - 8, curY - 6, 'R', color));
    } else if (step.rule === 'App<' || step.rule === 'Comp<B') {
      svg.appendChild(svgLine(x1 + 8, curY - 6, x2, curY - 6, color));
      svg.appendChild(svgArrow(x1 + 8, curY - 6, 'L', color));
    } else if (step.rule === 'TypeR') {
      svg.appendChild(svgLine(x1, curY - 6, x2, curY - 6, color, true));
    } else {
      svg.appendChild(svgLine(x1, curY - 6, x2, curY - 6, color));
    }

    svg.appendChild(svgText(x1 + 3, curY - 8, label, { fill: color, size: 9, mono: true, anchor: 'start' }));
    svg.appendChild(svgText(mx, curY + 6, step.cat, { fill: '#c0c0d0', size: 11, mono: true }));
    curY += ROW_H;
  }

  const err = partialErrorMessage(analysis);
  if (err) {
    svg.appendChild(svgLine(10, curY - 10, n * W + 10, curY - 10, COLORS.error, true));
    svg.appendChild(svgText(15, curY + 6, `✗ ${err}`, { fill: COLORS.error, size: 10, mono: true, anchor: 'start' }));
    curY += ROW_H;
  }

  svg.setAttribute('height', curY + 10);
  return svg;
}

async function callParseAPI(phrase) {
  const response = await fetch('/api/parse', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      phrase,
      typeRaise: document.getElementById('opt-typer').checked,
      maxTrees: 999,
      extraLexique: EXTRA_LEXIQUE
    })
  });
  if (!response.ok) throw new Error(`Erreur serveur: ${response.status}`);
  return response.json();
}

async function doParseAndRender() {
  const phrase = document.getElementById('phrase-input').value.trim();
  if (!phrase) return;
  const content = document.getElementById('content');
  content.innerHTML = '<div style="color:var(--muted);font-size:0.8rem">Analyse en cours…</div>';

  let result;
  try {
    result = await callParseAPI(phrase);
  } catch (err) {
    content.innerHTML = `<div class="status-err">${escapeHtml(err.message)}</div>`;
    return;
  }

  const mots = result.mots || [];
  const metrics = result.metrics || {};
  const complete = result.complete || [];
  const showPartial = document.getElementById('opt-partial').checked;
  const partials = showPartial ? (result.partials || []) : [];
  const failedPairs = metrics.failedPairs || [];
  const allAnalyses = [...complete, ...partials];
  const totalChemins = (metrics.successes || 0) + (metrics.impasses || 0);

  content.innerHTML = '';
  const status = document.createElement('div');
  status.className = 'status-bar';
  const metaInfo = `<span style="color:var(--muted);margin-left:auto">${mots.length} mots · ${result.elapsedMs}ms · <span style="color:var(--accent)">${metrics.successes || 0}</span> succès · <span style="color:var(--rule-err)">${metrics.impasses || 0}</span> impasse(s) sur ${totalChemins} chemins explorés</span>`;
  if (complete.length > 0) {
    status.innerHTML = `<span class="status-ok">✓ ${complete.length} analyse(s) complète(s)</span>${partials.length ? `<span class="status-partial">+ ${partials.length} blocage(s) affiché(s)</span>` : ''}${metaInfo}`;
  } else {
    status.innerHTML = `<span class="status-err">✗ Aucune analyse complète</span>${partials.length ? `<span class="status-partial">${partials.length} blocage(s) affiché(s)</span>` : ''}${metaInfo}`;
  }
  content.appendChild(status);

  if (allAnalyses.length === 0) {
    content.insertAdjacentHTML('beforeend', '<div style="color:var(--muted);font-size:0.8rem;padding:1rem 0;">Aucun résultat à afficher.</div>');
    return;
  }

  const navWrap = document.createElement('div');
  navWrap.style.cssText = 'display:flex;flex-direction:column;gap:0.4rem';
  const navComplete = document.createElement('div');
  navComplete.className = 'analyses-nav';
  const navPartial = document.createElement('div');
  navPartial.className = 'analyses-nav';
  if (complete.length) navComplete.innerHTML = '<span style="font-size:0.62rem;color:var(--muted);letter-spacing:0.08em;text-transform:uppercase;margin-right:0.2rem">Complètes</span>';
  if (partials.length) navPartial.innerHTML = '<span style="font-size:0.62rem;color:var(--muted);letter-spacing:0.08em;text-transform:uppercase;margin-right:0.2rem">Blocages</span>';
  navWrap.appendChild(navComplete);
  if (partials.length) navWrap.appendChild(navPartial);

  const displayArea = document.createElement('div');
  displayArea.className = 'derivation-wrap';

  function showAnalysis(idx) {
    navWrap.querySelectorAll('.nav-btn').forEach((b, i) => b.classList.toggle('active', i === idx));
    displayArea.innerHTML = '';
    displayArea.appendChild(renderDerivation(mots, allAnalyses[idx]));

    if (document.getElementById('opt-failures').checked && failedPairs.length > 0) {
      const failBlock = document.createElement('div');
      failBlock.style.cssText = 'margin-top:1rem;padding-top:0.75rem;border-top:1px solid var(--border)';
      const title = document.createElement('div');
      title.style.cssText = 'font-size:0.65rem;letter-spacing:0.08em;text-transform:uppercase;color:var(--muted);margin-bottom:0.5rem';
      title.textContent = `${metrics.rulesFailed || 0} paire(s) bloquée(s) sur ${metrics.rulesAttempted || 0} essais CYK`;
      failBlock.appendChild(title);
      const seen = new Map();
      failedPairs.forEach(p => {
        const k = p.left + ' + ' + p.right;
        seen.set(k, (seen.get(k) || 0) + 1);
      });
      const grid = document.createElement('div');
      grid.style.cssText = 'display:grid;grid-template-columns:1fr auto;gap:0.15rem 1rem;font-size:0.7rem;font-family:JetBrains Mono,monospace;max-height:150px;overflow-y:auto';
      [...seen.entries()].sort((a,b) => b[1]-a[1]).forEach(([pair, count]) => {
        grid.insertAdjacentHTML('beforeend', `<span style="color:var(--rule-err)">✗ ${escapeHtml(pair)}</span><span style="color:var(--muted);text-align:right">${count}×</span>`);
      });
      failBlock.appendChild(grid);
      displayArea.appendChild(failBlock);
    }
  }

  allAnalyses.forEach((a, i) => {
    const btn = document.createElement('button');
    btn.className = 'nav-btn' + (a.partial ? ' partial' : '');
    btn.textContent = a.label;
    btn.onclick = () => showAnalysis(i);
    if (a.partial) navPartial.appendChild(btn);
    else navComplete.appendChild(btn);
  });

  content.appendChild(navWrap);
  content.appendChild(displayArea);
  showAnalysis(0);
}

async function runBenchmark() {
  const content = document.getElementById('content');
  content.innerHTML = '<div style="color:var(--muted);font-size:0.8rem">Benchmark en cours…</div>';
  const results = [];
  for (const phrase of EXAMPLES) {
    document.getElementById('phrase-input').value = phrase;
    const res = await callParseAPI(phrase);
    results.push({ phrase, n: res.mots.length, elapsed: res.elapsedMs, ...res.metrics });
  }
  content.innerHTML = '';
  content.insertAdjacentHTML('beforeend', '<div style="font-size:0.75rem;color:var(--muted);margin-bottom:1rem;letter-spacing:0.08em;text-transform:uppercase">Benchmark — toutes les phrases</div>');
  const table = document.createElement('table');
  table.style.cssText = 'width:100%;border-collapse:collapse;font-size:0.72rem;font-family:JetBrains Mono,monospace';
  table.innerHTML = `
    <thead><tr style="color:var(--muted);border-bottom:1px solid var(--border)">
      <th style="text-align:left;padding:0.4rem 0.6rem">Phrase</th><th>Tokens</th><th>Succès</th><th>Impasses</th><th>Temps</th>
    </tr></thead>
    <tbody>${results.map(r => `
      <tr style="border-bottom:1px solid var(--border);cursor:pointer" data-phrase="${escapeHtml(r.phrase)}">
        <td style="padding:0.4rem 0.6rem;color:var(--accent2)">${escapeHtml(r.phrase)}</td>
        <td style="text-align:center;padding:0.4rem 0.6rem">${r.n}</td>
        <td style="text-align:center;padding:0.4rem 0.6rem;color:${r.successes > 0 ? 'var(--accent)' : 'var(--rule-err)'}">${r.successes}</td>
        <td style="text-align:center;padding:0.4rem 0.6rem;color:var(--rule-err)">${r.impasses}</td>
        <td style="text-align:right;padding:0.4rem 0.6rem;color:var(--muted)">${r.elapsed}ms</td>
      </tr>`).join('')}</tbody>`;
  content.appendChild(table);
  table.querySelectorAll('tr[data-phrase]').forEach(row => {
    row.onclick = () => {
      document.getElementById('phrase-input').value = row.dataset.phrase;
      doParseAndRender();
    };
  });
  document.getElementById('bench-results').textContent = `${results.length} phrases · moy ${(results.reduce((s,r)=>s+r.elapsed,0)/results.length).toFixed(1)}ms`;
}

async function init() {
  const response = await fetch('/api/lexique');
  const data = await response.json();
  BASE_LEXIQUE = data.lexique || {};
  EXAMPLES = data.examples || [];
  renderExamples();
  renderLex();
}

document.getElementById('add-word-btn').onclick = () => {
  const w = document.getElementById('new-word').value.trim();
  const c = document.getElementById('new-cat').value.trim();
  if (!w || !c) return;
  EXTRA_LEXIQUE[w] = c.split(',').map(s => s.trim()).filter(Boolean);
  renderLex();
  document.getElementById('new-word').value = '';
  document.getElementById('new-cat').value = '';
};

document.getElementById('phrase-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') doParseAndRender();
});
document.getElementById('parse-btn').onclick = doParseAndRender;
document.getElementById('bench-btn').onclick = runBenchmark;
init();
