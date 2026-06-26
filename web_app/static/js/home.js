/* Home page - background graph anim + stats loader */

(function () {
  var heroDom = document.getElementById('hero-graph');
  if (!heroDom) return;

  var chart = echarts.init(heroDom);

  // Static demo nodes (semiconductor domain)
  var demoNodes = [
    { id: 'PVD',       name: 'PVD',       category: 'Technology',  symbolSize: 48 },
    { id: 'CVD',       name: 'CVD',       category: 'Technology',  symbolSize: 44 },
    { id: 'ALD',       name: 'ALD',       category: 'Technology',  symbolSize: 42 },
    { id: '溅射',       name: '溅射',       category: 'Method',      symbolSize: 32 },
    { id: 'PECVD',     name: 'PECVD',     category: 'Method',      symbolSize: 30 },
    { id: 'MOCVD',     name: 'MOCVD',     category: 'Method',      symbolSize: 28 },
    { id: 'TiN',       name: 'TiN',       category: 'Material',    symbolSize: 34 },
    { id: 'SiO2',      name: 'SiO2',      category: 'Material',    symbolSize: 30 },
    { id: 'Al2O3',     name: 'Al2O3',     category: 'Material',    symbolSize: 28 },
    { id: 'HfO2',      name: 'HfO2',      category: 'Material',    symbolSize: 26 },
    { id: 'Si3N4',     name: 'Si3N4',     category: 'Material',    symbolSize: 24 },
    { id: 'W',         name: 'W',         category: 'Material',    symbolSize: 22 },
    { id: 'Cu',        name: 'Cu',        category: 'Material',    symbolSize: 24 },
    { id: 'Al',        name: 'Al',        category: 'Material',    symbolSize: 22 },
    { id: 'LPCVD',     name: 'LPCVD',     category: 'Method',      symbolSize: 26 },
    { id: 'APCVD',     name: 'APCVD',     category: 'Method',      symbolSize: 22 },
    { id: '蒸镀',       name: '蒸镀',       category: 'Method',      symbolSize: 26 },
    { id: 'PLD',       name: 'PLD',       category: 'Method',      symbolSize: 22 },
    { id: '刻蚀',       name: '刻蚀',       category: 'Technology',  symbolSize: 40 },
    { id: '光刻',       name: '光刻',       category: 'Technology',  symbolSize: 42 },
    { id: '外延生长',   name: '外延生长',   category: 'Technology',  symbolSize: 30 },
    { id: '3D集成',    name: '3D集成',    category: 'Technology',  symbolSize: 34 },
    { id: 'TSV',       name: 'TSV',       category: 'ChipStructure', symbolSize: 26 },
    { id: '磁控溅射',   name: '磁控溅射',   category: 'Equipment',   symbolSize: 28 },
    { id: 'CMP',       name: 'CMP',       category: 'Technology',  symbolSize: 32 },
  ];

  var demoLinks = [
    { source: 'PVD',    target: '溅射',      label: '包含'},
    { source: 'PVD',    target: '蒸镀',      label: '包含'},
    { source: 'PVD',    target: 'PLD',       label: '包含'},
    { source: 'PVD',    target: 'TiN',       label: '沉积'},
    { source: 'PVD',    target: 'Al',        label: '沉积'},
    { source: 'PVD',    target: 'Cu',        label: '沉积'},
    { source: 'PVD',    target: 'W',         label: '沉积'},
    { source: 'CVD',    target: 'PECVD',     label: '包含'},
    { source: 'CVD',    target: 'MOCVD',     label: '包含'},
    { source: 'CVD',    target: 'LPCVD',     label: '包含'},
    { source: 'CVD',    target: 'APCVD',     label: '包含'},
    { source: 'CVD',    target: 'SiO2',      label: '沉积'},
    { source: 'CVD',    target: 'Si3N4',     label: '沉积'},
    { source: 'CVD',    target: 'TiN',       label: '沉积'},
    { source: 'ALD',    target: 'Al2O3',     label: '沉积'},
    { source: 'ALD',    target: 'HfO2',      label: '沉积'},
    { source: 'ALD',    target: 'TiN',       label: '沉积'},
    { source: '溅射',    target: '磁控溅射',  label: '使用设备'},
    { source: '3D集成', target: 'TSV',       label: '依赖'},
    { source: 'CVD',    target: '外延生长',   label: '相关'},
    { source: '刻蚀',    target: '光刻',      label: '配合'},
    { source: 'CMP',    target: 'SiO2',      label: '抛光'},
    { source: 'PVD',    target: 'CVD',       label: '互补'},
    { source: 'CVD',    target: 'ALD',       label: '互补'},
  ];

  var categories = [
    { name: 'Technology',  itemStyle: { color: '#4a67ff' } },
    { name: 'Method',      itemStyle: { color: '#18a999' } },
    { name: 'Material',    itemStyle: { color: '#ff8c42' } },
    { name: 'Equipment',   itemStyle: { color: '#9b5de5' } },
    { name: 'ChipStructure', itemStyle: { color: '#f15bb5' } },
  ];

  var option = {
    backgroundColor: 'transparent',
    animation: true,
    animationDuration: 2000,
    animationEasingUpdate: 'quinticInOut',
    series: [{
      type: 'graph',
      layout: 'force',
      roam: false,
      draggable: false,
      categories: categories,
      label: { show: true, fontSize: 12, color: 'rgba(27,36,48,0.7)', fontWeight: 500 },
      edgeLabel: { show: true, fontSize: 10, color: 'rgba(27,36,48,0.35)' },
      edgeSymbol: ['none', 'arrow'],
      edgeSymbolSize: 6,
      data: demoNodes,
      links: demoLinks,
      force: { repulsion: 280, edgeLength: [80, 200], gravity: 0.08, friction: 0.1 },
      lineStyle: { width: 1.5, opacity: 0.5, curveness: 0.15 },
      emphasis: { focus: 'adjacency', lineStyle: { width: 3 } },
    }]
  };

  chart.setOption(option);

  // Gentle auto-rotation
  var rot = 0;
  setInterval(function () {
    rot += 0.15;
    chart.setOption({
      series: [{
        force: {
          gravity: 0.08 + Math.sin(rot * 0.4) * 0.02,
        }
      }]
    });
  }, 2000);

  window.addEventListener('resize', function () { chart.resize(); });

  // Load public stats
  fetch('/api/public/stats')
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (d) {
      var stats = document.getElementById('hero-stats');
      if (!stats) return;
      stats.innerHTML =
        '<div class="stat-item"><span class="stat-num">' + (d.node_count || '120+') + '</span><span class="stat-label">技术节点</span></div>' +
        '<div class="stat-item"><span class="stat-num">' + (d.relation_count || '200+') + '</span><span class="stat-label">知识关系</span></div>' +
        '<div class="stat-item"><span class="stat-num">' + (d.label_count || '10') + '</span><span class="stat-label">实体类别</span></div>';
    })
    .catch(function () {});
})();
