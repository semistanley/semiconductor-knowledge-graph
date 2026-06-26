let allArchives = [];
let currentFilter = 'all';

function formatTime(iso) {
  if (!iso) return '';
  try {
    return new Date(iso).toLocaleString('zh-CN');
  } catch {
    return iso;
  }
}

function typeLabel(t) {
  const map = {
    chat: '问答归档',
    document_extract: '文档抽取',
    kg_update: '图谱更新',
  };
  return map[t] || t;
}

function renderUpdates(updates) {
  const el = document.getElementById('kg-updates');
  if (!updates.length) {
    el.innerHTML = '<p class="muted">暂无图谱更新记录</p>';
    return;
  }
  el.innerHTML = updates.map(u => `
    <div class="archive-item">
      <div class="archive-head">
        <span class="badge">${typeLabel(u.type)}</span>
        <span class="archive-time">${formatTime(u.created_at)}</span>
      </div>
      <div class="archive-body">
        新增实体 <b>${u.entities_added}</b> 个，关系 <b>${u.relations_added}</b> 条
        <span class="status-${u.status}">${u.status}</span>
      </div>
    </div>
  `).join('');
}

function renderArchives() {
  const el = document.getElementById('archives');
  const filtered = currentFilter === 'all'
    ? allArchives
    : allArchives.filter(a => a.type === currentFilter);

  if (!filtered.length) {
    el.innerHTML = '<p class="muted">暂无归档记录</p>';
    return;
  }

  el.innerHTML = filtered.map(a => {
    let preview = '';
    if (a.type === 'chat') {
      preview = `<div>问：${(a.content.question || '').slice(0, 80)}</div>
                 <div>答：${(a.content.answer || '').slice(0, 120)}...</div>`;
    } else if (a.type === 'document_extract') {
      preview = `文档：${a.content.source_doc || ''}，实体 ${(a.content.entities || []).length} 个`;
    } else if (a.type === 'kg_update') {
      preview = `来源：${a.content.source_doc || ''}，实体 ${(a.content.entities || []).length} 个`;
    } else {
      preview = JSON.stringify(a.content).slice(0, 100);
    }
    return `
      <div class="archive-item">
        <div class="archive-head">
          <span class="badge">${typeLabel(a.type)}</span>
          <span class="archive-time">${formatTime(a.created_at)}</span>
        </div>
        <div class="archive-title">${a.title || ''}</div>
        <div class="archive-body">${preview}</div>
      </div>
    `;
  }).join('');
}

document.addEventListener('DOMContentLoaded', async () => {
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.type;
      renderArchives();
    });
  });

  try {
    const [archResp, updResp] = await Promise.all([
      fetch('/api/archives'),
      fetch('/api/graph/updates'),
    ]);
    const archData = await archResp.json();
    const updData = await updResp.json();
    allArchives = archData.archives || [];
    renderUpdates(updData.updates || []);
    renderArchives();
  } catch (e) {
    document.getElementById('archives').innerHTML = `<p class="auth-error">加载失败：${e.message}</p>`;
  }
});
