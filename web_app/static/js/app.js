const chatEl = document.getElementById('chat');
const qEl = document.getElementById('q');
const sendBtn = document.getElementById('send');
const traceEl = document.getElementById('trace');
const detailPanel = document.getElementById('detail-panel');

const graphDom = document.getElementById('graph');
const chart = echarts.init(graphDom);
// 暴露给 resizer.js 用于在拖动时 resize，避免画布溢出到下方详情区域
window.__kgChart = chart;

const ROLE_LABELS = {
  user: '提问',
  ai: '回答'
};

function addMsg(role, text) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerHTML = `<span class="role">${ROLE_LABELS[role] || role}</span><span class="text"></span>`;
  div.querySelector('.text').innerText = text;
  chatEl.appendChild(div);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function sanitizeAnswer(text) {
  if (!text) return '';
  return text.replace(/\*\*/g, '').replace(/\*/g, '').replace(/^\s*[-•]\s+/gm, '').replace(/^\s*#+\s*/gm, '').trim();
}

// -------------------------
// Trace 勾选版：工具函数
// -------------------------
function toggleAllTriples(checked) {
  document.querySelectorAll('#trace .triple-cb').forEach(cb => { cb.checked = !!checked; });
}

function getSelectedTriples() {
  const src = window.__lastExtractedTriples || { entities: [], relations: [] };
  const selected = { entities: [], relations: [] };

  document.querySelectorAll('#trace .triple-cb').forEach(cb => {
    if (!cb.checked) return;
    const kind = cb.getAttribute('data-kind');
    const idx = parseInt(cb.getAttribute('data-index') || '-1', 10);
    if (Number.isNaN(idx) || idx < 0) return;

    if (kind === 'entity' && src.entities && src.entities[idx]) {
      selected.entities.push(src.entities[idx]);
    }
    if (kind === 'relation' && src.relations && src.relations[idx]) {
      selected.relations.push(src.relations[idx]);
    }
  });

  return selected;
}

async function confirmSelectedTriples() {
  const triples = getSelectedTriples();
  if ((!triples.entities || triples.entities.length === 0) && (!triples.relations || triples.relations.length === 0)) {
    alert('你还没有勾选任何三元组。');
    return;
  }

  try {
    const resp = await fetch('/api/chat/confirm_triples', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ triples })
    });
    const data = await resp.json();

    if (!data || !data.ok) {
      alert('保存失败：' + (data?.error || '未知错误'));
      return;
    }

    const msg = `已入库！新增：实体 ${data.added?.entities ?? '?'} 个，关系 ${data.added?.relations ?? '?'} 条。\n已存在跳过：实体 ${data.skipped?.entities ?? '?'} 个，关系 ${data.skipped?.relations ?? '?'} 条。`;
    alert(msg);

    // 入库成功后：立刻展示“新增子图”
    if (Array.isArray(data.touched_nodes) && data.touched_nodes.length > 0) {
      await showSubgraphBySeeds(data.touched_nodes);
    } else {
      await loadOverviewGraph();
    }
  } catch (e) {
    alert('保存失败：' + e.message);
  }
}

function renderTrace(trace) {
  let traceHtml = '';
  if (trace && trace.length > 0) {
    trace.forEach((item) => {
      if (item.step === 'extracted_triples') {
        // 把当前候选三元组放到 window，供确认按钮读取
        window.__lastExtractedTriples = item.triples || { entities: [], relations: [] };

        traceHtml += `<div class="trace-item"><div><strong>${item.message}</strong></div>`;

        traceHtml += `
          <div class="trace-actions">
            <button class="btn small-btn" onclick="toggleAllTriples(true)">全选</button>
            <button class="btn small-btn danger" onclick="toggleAllTriples(false)">全不选</button>
            <button class="btn small-btn" onclick="confirmSelectedTriples()">确认勾选并入库</button>
          </div>
        `;

        if (item.triples.entities && item.triples.entities.length > 0) {
          traceHtml += `<div class="trace-section"><div class="trace-section-title">实体</div>`;
          item.triples.entities.forEach((entity, i) => {
            const label = entity.label || '未知类型';
            const name = entity.name || '未命名';
            const desc = entity.description ? (': ' + entity.description) : '';
            traceHtml += `
              <label class="trace-check">
                <input type="checkbox" class="triple-cb" data-kind="entity" data-index="${i}" checked />
                <span>[${label}] ${name}${desc}</span>
              </label>
            `;
          });
          traceHtml += `</div>`;
        }

        if (item.triples.relations && item.triples.relations.length > 0) {
          traceHtml += `<div class="trace-section"><div class="trace-section-title">关系</div>`;
          item.triples.relations.forEach((rel, i) => {
            const s = rel.start_name || '未知';
            const t = rel.rel_type || '关系';
            const o = rel.end_name || '未知';
            traceHtml += `
              <label class="trace-check">
                <input type="checkbox" class="triple-cb" data-kind="relation" data-index="${i}" checked />
                <span>${s} --[${t}]--> ${o}</span>
              </label>
            `;
          });
          traceHtml += `</div>`;
        }

        traceHtml += `</div>`;
      }
    });
  }
  traceEl.innerHTML = traceHtml;
}

function buildOption(nodes, links) {
  const categories = Array.from(new Set(nodes.map(n => n.category))).map(c => ({ name: c }));
  return {
    backgroundColor: 'transparent',
    tooltip: { show: false },
    legend: [{ data: categories.map(c => c.name), textStyle: { color: '#1b2430' } }],
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      animation: true,
      animationDurationUpdate: 800,
      label: { show: true, color: '#1b2430' },
      edgeLabel: { show: true, fontSize: 11, color: "#18a999", fontWeight: 600 },
      edgeSymbol: ["none", "arrow"],
      edgeSymbolSize: 8,
      categories,
      data: nodes,
      links,
      force: { repulsion: 300, edgeLength: 120, friction: 0.2 },
      lineStyle: { width: 3, opacity: 0.9, curveness: 0.2, color: "#4a67ff" },
      emphasis: { focus: 'adjacency', lineStyle: { width: 4 } },
    }]
  };
}

function renderGraph(graph) {
  const nodes = (graph?.nodes || []).map(n => ({
    id: n.id,
    name: n.name,
    category: n.category,
    description: n.description || '',
    evidence: n.evidence || '',
    source: n.source || '',
    symbolSize: n.symbolSize || 30,
    itemStyle: n.itemStyle || undefined,
    label: n.label || undefined,
  }));

  const links = (graph?.links || []).map(l => ({
    source: l.source,
    target: l.target,
    label: l.label,
    rel_type: l.rel_type || l.original_label || '',
    description: l.description || '',
    sourceStage: l.sourceStage || '',
  }));

  chart.setOption(buildOption(nodes, links), true);
}

function mergeGraphs(g1, g2) {
  const nodes = [...(g1?.nodes || [])];
  const links = [...(g1?.links || [])];
  const nodeIds = new Set(nodes.map(n => n.id));

  (g2?.nodes || []).forEach(n => {
    if (!nodeIds.has(n.id)) {
      nodeIds.add(n.id);
      nodes.push(n);
    }
  });

  const linkKey = (l) => `${l.source}__${l.label}__${l.target}`;
  const linkIds = new Set(links.map(linkKey));
  (g2?.links || []).forEach(l => {
    const k = linkKey(l);
    if (!linkIds.has(k)) {
      linkIds.add(k);
      links.push(l);
    }
  });

  return { nodes, links };
}

function getAdjacencyStats(graph, nodeName) {
  const links = graph?.links || [];
  const related = new Set();
  let inDegree = 0;
  let outDegree = 0;

  links.forEach(l => {
    if (l.source === nodeName) {
      outDegree += 1;
      related.add(l.target);
    }
    if (l.target === nodeName) {
      inDegree += 1;
      related.add(l.source);
    }
  });

  return {
    inDegree,
    outDegree,
    degree: inDegree + outDegree,
    relatedCount: related.size,
  };
}

function estimateCommercialValue(category, degree) {
  // 投资人视角：设备/工艺/技术 > 材料 > 能力 > 参数
  const base = {
    Equipment: 4,
    Technology: 4,
    Method: 3,
    Material: 3,
    Capability: 2,
    Parameter: 1,
    Entity: 2,
    Node: 2,
  };
  const b = base[category] ?? 2;
  const score = b + Math.min(2, Math.floor(degree / 3));

  if (score >= 5) return { level: '高', hint: '可直接映射到客户预算/交付场景，适合做 PoC→试点→规模化' };
  if (score >= 3) return { level: '中', hint: '可作为解决方案模块，建议补齐上下游节点以形成可复用交付包' };
  return { level: '低', hint: '偏基础概念/参数，建议绑定具体设备/工艺场景提升商业可解释性' };
}

function estimateTRL(category) {
  // 展示用估计：用于讲清楚“可落地程度”
  const map = {
    Equipment: 7,
    Technology: 6,
    Method: 6,
    Material: 5,
    Capability: 4,
    Parameter: 3,
    Entity: 4,
    Node: 4,
  };
  return map[category] ?? 4;
}

function businessTemplate(category) {
  // 不编造具体公司/型号，只给“商业模型结构化模板”
  if (category === 'Equipment') {
    return {
      scenario: ['晶圆厂设备选型与替代', '工艺导入/量产爬坡', '设备维护与良率提升'],
      buyer: ['工艺/设备负责人（技术评审）', '采购（商务/交付条款）', '厂务/质量（合规与验收）'],
      roi: ['良率提升（ppm/缺陷密度下降）', '吞吐提升（UPH）', '成本下降（耗材/维护/折旧）'],
      model: ['设备销售 + 安装调试', '维保/备件订阅', '工艺recipe/参数包交付（增值）'],
      moat: ['工艺know-how沉淀（recipe库）', '数据闭环（故障/缺陷→优化）', '客户现场验证壁垒'],
    };
  }
  if (category === 'Technology' || category === 'Method') {
    return {
      scenario: ['工艺路线设计与优化', '新材料/新结构导入', '良率与一致性提升'],
      buyer: ['工艺整合/研发（定义目标）', '产线工程（实施与验证）', '质量/可靠性（评估与验收）'],
      roi: ['窗口扩大（Process Window）', '良率提升', '缩短导入周期（TTV）'],
      model: ['咨询/交付（工艺路线+验证报告）', '软件订阅（知识库/决策支持）', '数据服务（工艺/设备参数对标）'],
      moat: ['结构化知识图谱资产', '行业数据积累与迭代', '可解释推理链路（可信）'],
    };
  }
  if (category === 'Material') {
    return {
      scenario: ['材料选型与替代', '可靠性/一致性提升', '成本与供应链优化'],
      buyer: ['工艺/材料工程（性能评估）', '质量/可靠性（验证）', '采购（成本与供货）'],
      roi: ['缺陷降低与一致性提升', '降低返工/报废', '供应链风险下降'],
      model: ['材料供应 + 工艺适配服务', '联合开发（NRE + 量产供货）', '数据订阅（材料性能/对标）'],
      moat: ['配方/工艺适配能力', '验证数据积累', '供应链与认证门槛'],
    };
  }

  return {
    scenario: ['知识检索与问答', '工程决策辅助', '文档知识结构化沉淀'],
    buyer: ['研发/工程团队', '知识管理/信息化', '业务负责人'],
    roi: ['缩短检索时间', '减少试错成本', '知识复用率提升'],
    model: ['SaaS订阅', '私有化部署+实施', '行业知识库增值服务'],
    moat: ['领域知识图谱', '持续迭代的数据资产', '工作流闭环（抽取-确认-入库）'],
  };
}

function renderNodeDetails(nodeData, graphSnapshot) {
  const name = nodeData?.name || '';
  const category = nodeData?.category || 'Entity';
  const desc = nodeData?.description || '暂无描述（建议后续补齐：定义/应用场景/关键参数范围）';
  const evidence = nodeData?.evidence || '';
  const source = nodeData?.source || '';

  const stats = getAdjacencyStats(graphSnapshot, name);
  const value = estimateCommercialValue(category, stats.degree);
  const trl = estimateTRL(category);
  const tpl = businessTemplate(category);

  let html = '';
  html += `<div class="detail-card">`;
  html += `  <div class="detail-header">`;
  html += `    <div class="detail-title">${name}</div>`;
  html += `    <div class="detail-sub">类型：<span class="badge">${category}</span> 来源：<span class="badge">${source || 'neo4j'}</span></div>`;
  html += `  </div>`;

  html += `  <div class="detail-grid">`;
  html += `    <div class="metric"><div class="metric-k">关联强度</div><div class="metric-v">${stats.degree}</div><div class="metric-s">连接 ${stats.relatedCount} 个节点</div></div>`;
  html += `    <div class="metric"><div class="metric-k">落地成熟度(TRL)</div><div class="metric-v">${trl}/9</div><div class="metric-s">用于演示“可落地程度”</div></div>`;
  html += `    <div class="metric"><div class="metric-k">商业价值</div><div class="metric-v">${value.level}</div><div class="metric-s">${value.hint}</div></div>`;
  html += `  </div>`;

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">一句话定位（Pitch）</div>`;
  html += `    <div class="detail-text"><b>${name}</b> 在当前知识网络中属于 <b>${category}</b> 类节点，可用于 <b>${tpl.scenario[0]}</b>，并通过 <b>${tpl.roi[0]}</b> 体现价值。</div>`;
  html += `  </div>`;

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">核心描述</div>`;
  html += `    <div class="detail-text">${desc}</div>`;
  html += `  </div>`;

  if (evidence) {
    html += `  <div class="detail-section">`;
    html += `    <div class="detail-section-title">证据 / 来源片段</div>`;
    html += `    <div class="detail-text mono">${evidence}</div>`;
    html += `  </div>`;
  }

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">应用场景（Where）</div>`;
  html += `    <ul class="detail-ul">${tpl.scenario.map(x => `<li>${x}</li>`).join('')}</ul>`;
  html += `  </div>`;

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">采购/决策链（Who）</div>`;
  html += `    <ul class="detail-ul">${tpl.buyer.map(x => `<li>${x}</li>`).join('')}</ul>`;
  html += `  </div>`;

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">ROI 杠杆（Value）</div>`;
  html += `    <ul class="detail-ul">${tpl.roi.map(x => `<li>${x}</li>`).join('')}</ul>`;
  html += `  </div>`;

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">商业模式（How to sell）</div>`;
  html += `    <ul class="detail-ul">${tpl.model.map(x => `<li>${x}</li>`).join('')}</ul>`;
  html += `  </div>`;

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">壁垒 / 护城河（Moat）</div>`;
  html += `    <ul class="detail-ul">${tpl.moat.map(x => `<li>${x}</li>`).join('')}</ul>`;
  html += `  </div>`;

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">落地路径（PoC → 试点 → 规模化）</div>`;
  html += `    <ul class="detail-ul">`;
  html += `      <li><b>PoC：</b>选择 1 个典型问题/工艺段，导入文档+图谱，验证可解释问答与连通子图</li>`;
  html += `      <li><b>试点：</b>固化工作流（抽取-确认-入库），覆盖 3~5 个高频场景，形成可交付报告</li>`;
  html += `      <li><b>规模化：</b>接入更多数据源/部门，形成知识资产闭环与持续迭代模型</li>`;
  html += `    </ul>`;
  html += `  </div>`;

  html += `</div>`;

  detailPanel.innerHTML = html;
}

function renderEdgeDetails(edgeData) {
  const s = edgeData?.source;
  const t = edgeData?.target;
  const label = edgeData?.label;
  const desc = edgeData?.description || '';

  let html = '';
  html += `<div class="detail-card">`;
  html += `  <div class="detail-header">`;
  html += `    <div class="detail-title">关系：${label || ''}</div>`;
  html += `    <div class="detail-sub">${s} → ${t}</div>`;
  html += `  </div>`;

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">关系含义（对业务的解释）</div>`;
  html += `    <div class="detail-text">${desc || '暂无描述。建议补齐：该关系为何成立、适用条件、对决策的影响（设备/工艺/成本/良率）。'}</div>`;
  html += `  </div>`;

  html += `  <div class="detail-section">`;
  html += `    <div class="detail-section-title">决策价值（投资人视角）</div>`;
  html += `    <ul class="detail-ul">`;
  html += `      <li>把“知识”变成“可解释的决策路径”，减少试错和沟通成本</li>`;
  html += `      <li>可沉淀为可复用的“推荐逻辑”，形成交付壁垒</li>`;
  html += `    </ul>`;
  html += `  </div>`;

  html += `</div>`;
  detailPanel.innerHTML = html;
}

async function ask() {
  const q = qEl.value.trim();
  if (!q) return;

  addMsg('user', q);
  qEl.value = '';
  addMsg('ai', '正在检索知识图谱并生成答案…');

  const resp = await fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: q }) });
  const data = await resp.json();

  const answer = sanitizeAnswer(data.response || JSON.stringify(data));
  const last = chatEl.lastChild;
  if (last && last.classList.contains('ai')) {
    last.querySelector('.text').innerText = answer;
  } else {
    addMsg('ai', answer);
  }

  renderTrace(data.trace);

  const mainGraph = data.graph?.main;
  const expansionGraph = data.graph?.expansion;

  if ((!mainGraph || !mainGraph.nodes || mainGraph.nodes.length === 0) && (!expansionGraph || !expansionGraph.nodes || expansionGraph.nodes.length === 0)) {
    await loadOverviewGraph();
  } else {
    renderGraph(mainGraph || { nodes: [], links: [] });
    setTimeout(() => {
      const merged = mergeGraphs(mainGraph, expansionGraph);
      renderGraph(merged);
    }, 300);
  }
}

// --- Event Listeners ---
sendBtn.addEventListener('click', ask);
qEl.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); ask(); } });
window.addEventListener('resize', () => chart.resize());

// 图谱交互：单击同时显示详情并展开
chart.on('click', async (params) => {
  const data = params.data || {};

  // 获取当前图谱快照，用于算“关联强度”等指标
  const opt = chart.getOption();
  const series = opt.series?.[0] || {};
  const graphSnapshot = { nodes: series.data || [], links: series.links || [] };

  // 1. 显示详情
  if (params.dataType === 'node') {
    renderNodeDetails(data, graphSnapshot);
  } else if (params.dataType === 'edge') {
    renderEdgeDetails(data);
  }

  // 2. 展开子图 (仅限节点)
  if (params.dataType !== 'node') return;
  const nodeName = data.name;
  if (!nodeName) return;

  try {
    const resp = await fetch('/api/graph/expand', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ node_name: nodeName }) });
    const expansionData = await resp.json();
    if (expansionData.error) { return; }

    const currentOption = chart.getOption();
    const currentGraph = { nodes: currentOption.series[0].data, links: currentOption.series[0].links };
    const mergedGraph = mergeGraphs(currentGraph, expansionData);
    renderGraph(mergedGraph);
  } catch (error) { console.error('Failed to expand graph:', error); }
});

// 初始图
async function loadOverviewGraph() {
  try {
    const resp = await fetch('/api/graph/overview');
    if (!resp.ok) { renderGraph({ nodes: [], links: [] }); return; }
    const data = await resp.json();
    if (data.error) { renderGraph({ nodes: [], links: [] }); return; }
    renderGraph(data);
  } catch (error) { renderGraph({ nodes: [], links: [] }); }
}

async function showSubgraphBySeeds(seedNames) {
  const seeds = (seedNames || []).filter(s => typeof s === 'string' && s.trim()).slice(0, 8);
  if (seeds.length === 0) {
    await loadOverviewGraph();
    return;
  }

  // 逐个 seed 调 expand，然后合并成一个子图
  let merged = { nodes: [], links: [] };
  for (const name of seeds) {
    try {
      const resp = await fetch('/api/graph/expand', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ node_name: name })
      });
      const g = await resp.json();
      if (g && !g.error) {
        merged = mergeGraphs(merged, g);
      }
    } catch (e) {
      // ignore single seed failure
    }
  }

  if (!merged.links || merged.links.length === 0) {
    await loadOverviewGraph();
    return;
  }

  renderGraph(merged);
}

loadOverviewGraph();

async function loadChatHistory() {
  try {
    const resp = await fetch('/api/chat/history');
    if (!resp.ok) return;
    const data = await resp.json();
    (data.messages || []).forEach(m => {
      if (m.role === 'user' || m.role === 'ai') {
        addMsg(m.role, m.content);
      }
    });
  } catch (e) {
    console.warn('加载历史对话失败', e);
  }
}

loadChatHistory();
