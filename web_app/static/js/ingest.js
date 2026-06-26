const fileInput = document.getElementById('file');
const versionEl = document.getElementById('version');
const extractBtn = document.getElementById('extract');
const applyBtn = document.getElementById('apply');
const pendingEl = document.getElementById('pending');
const statusEl = document.getElementById('status');
const dropZone = document.getElementById('drop-zone');
const fileBtn = document.getElementById('file-btn');

let pendingData = null;
let selectedFile = null;

function setStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.style.color = isError ? 'var(--danger)' : 'var(--muted)';
}

function card(title, bodyHtml) {
  const div = document.createElement('div');
  div.className = 'card';
  div.innerHTML = `<h4>${title}</h4>${bodyHtml}`;
  return div;
}

function renderPending(p) {
  pendingEl.innerHTML = '';

  const entities = p.entities || [];
  const relations = p.relations || [];
  const measurements = p.measurements || [];

  pendingEl.appendChild(card('基本信息', `<div class="small">source_doc: ${p.source_doc} | version: ${p.source_version} | extracted_at: ${p.extracted_at}</div>`));

  const entWrap = document.createElement('div');
  entWrap.appendChild(card(`实体 Entities（${entities.length}）`, ''));
  entities.forEach((e, idx) => {
    const id = `ent_${idx}`;
    const el = document.createElement('div');
    el.className = 'row';
    el.innerHTML = `
      <input type="checkbox" id="${id}" />
      <label for="${id}" class="row" style="cursor:pointer; flex:1;">
        <span class="tag">${e.label}</span>
        <span>${e.name}</span>
        <span class="small">${(e.properties?.evidence || '').slice(0, 80)}...</span>
      </label>
    `;
    el.querySelector('input').addEventListener('change', (ev) => { e.confirmed = ev.target.checked; });
    entWrap.appendChild(el);
  });
  pendingEl.appendChild(entWrap);

  const relWrap = document.createElement('div');
  relWrap.appendChild(card(`关系 Relations（${relations.length}）`, ''));
  relations.forEach((r, idx) => {
    const id = `rel_${idx}`;
    const el = document.createElement('div');
    el.className = 'row';
    el.innerHTML = `
      <input type="checkbox" id="${id}" />
      <label for="${id}" class="row" style="cursor:pointer; flex:1;">
        <span class="tag">${r.rel_type}</span>
        <span>${r.start_name} → ${r.end_name}</span>
        <span class="small">${(r.properties?.evidence || '').slice(0, 80)}...</span>
      </label>
    `;
    el.querySelector('input').addEventListener('change', (ev) => { r.confirmed = ev.target.checked; });
    relWrap.appendChild(el);
  });
  pendingEl.appendChild(relWrap);

  const mWrap = document.createElement('div');
  mWrap.appendChild(card(`量化信息 Measurements（${measurements.length}）`, '<div class="small">建议只勾选证据充分的数值数据</div>'));
  measurements.forEach((m, idx) => {
    const id = `m_${idx}`;
    const el = document.createElement('div');
    el.className = 'row';
    el.innerHTML = `
      <input type="checkbox" id="${id}" />
      <label for="${id}" class="row" style="cursor:pointer; flex:1;">
        <span class="tag">${m.metric || 'metric'}</span>
        <span>${m.subject_name || ''}</span>
        <span class="small">${(m.evidence || '').slice(0, 80)}...</span>
      </label>
    `;
    el.querySelector('input').addEventListener('change', (ev) => { m.confirmed = ev.target.checked; });
    mWrap.appendChild(el);
  });
  pendingEl.appendChild(mWrap);
}

function handleFileSelect(file) {
  if (!file) return;
  selectedFile = file;
  dropZone.querySelector('.drop-zone-text').innerHTML = `<p>已选择文件：<b>${file.name}</b></p><p class="small">点击或拖拽可更换</p>`;
}

// --- Event Listeners ---

// 点击按钮触发文件选择
fileBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', () => handleFileSelect(fileInput.files?.[0]));

// 拖拽区域事件
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropZone.classList.add('drag-over');
});
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  const file = e.dataTransfer.files?.[0];
  handleFileSelect(file);
});

// 抽取按钮
extractBtn.addEventListener('click', async () => {
  if (!selectedFile) {
    setStatus('请先选择或拖拽一个文件', true);
    return;
  }

  setStatus('抽取中...（文档越大耗时越长，请耐心等待）');
  extractBtn.disabled = true;

  const form = new FormData();
  form.append('file', selectedFile);
  form.append('source_version', versionEl.value || 'v1');

  try {
    const resp = await fetch('/api/ingest/extract', { method: 'POST', body: form });
    const data = await resp.json();
    if (data.error) {
      throw new Error(data.error);
    }
    pendingData = data;
    renderPending(pendingData);
    setStatus('抽取完成：请勾选需要导入的条目，然后点击“确认并导入”');
  } catch (err) {
    setStatus(`抽取失败：${err.message}`, true);
  } finally {
    extractBtn.disabled = false;
  }
});

// 导入按钮
applyBtn.addEventListener('click', async () => {
  if (!pendingData) {
    setStatus('请先抽取三元组', true);
    return;
  }

  setStatus('导入中...');
  applyBtn.disabled = true;

  try {
    const resp = await fetch('/api/ingest/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(pendingData),
    });
    const data = await resp.json();
    if (data.error) {
      throw new Error(data.error);
    }
    setStatus(`导入成功！新增实体 ${data.added?.entities ?? '?'} 个，关系 ${data.added?.relations ?? '?'} 条。已自动归档并更新知识图谱。`);
  } catch (err) {
    setStatus(`导入失败：${err.message}`, true);
  } finally {
    applyBtn.disabled = false;
  }
});
