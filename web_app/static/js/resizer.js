// resizer.js
// 让左右两侧面板可上下拖动调整高度，并记住到 localStorage
// 关键：只在需要时触发图谱 chart.resize()，避免左侧拖动误伤导致图谱错位

(function () {
  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function safeResizeChart() {
    if (window.__kgChart && typeof window.__kgChart.resize === 'function') {
      window.__kgChart.resize();
      // 某些浏览器布局重排有延迟，补一刀更稳
      setTimeout(() => {
        try { window.__kgChart.resize(); } catch (e) {}
      }, 50);
    }
  }

  function initVerticalSplit(opts) {
    const {
      key,
      containerEl,
      topEl,
      bottomEl,
      resizerEl,
      minTop = 140,
      minBottom = 160,
      padding = 60,
      onResize = null,
    } = opts;

    if (!containerEl || !topEl || !bottomEl || !resizerEl) return;

    function read() {
      try {
        const v = localStorage.getItem(key);
        if (!v) return null;
        const n = parseInt(v, 10);
        return Number.isFinite(n) ? n : null;
      } catch (_) {
        return null;
      }
    }

    function write(v) {
      try {
        localStorage.setItem(key, String(v));
      } catch (_) {}
    }

    // 恢复高度（只影响 top，高度剩余给 bottom）
    const saved = read();
    if (saved && saved > 0) {
      topEl.style.flex = '0 0 auto';
      topEl.style.height = `${saved}px`;
      bottomEl.style.flex = '1 1 auto';

      if (typeof onResize === 'function') onResize();
    }

    let dragging = false;
    let startY = 0;
    let startH = 0;

    resizerEl.addEventListener('mousedown', (e) => {
      e.preventDefault();
      dragging = true;
      startY = e.clientY;
      startH = topEl.getBoundingClientRect().height;
      resizerEl.classList.add('dragging');

      topEl.style.flex = '0 0 auto';
      bottomEl.style.flex = '1 1 auto';

      document.body.style.cursor = 'row-resize';
    });

    window.addEventListener('mousemove', (e) => {
      if (!dragging) return;

      const dy = e.clientY - startY;
      const containerH = containerEl.getBoundingClientRect().height;
      const maxTop = containerH - minBottom - padding;

      const newH = clamp(startH + dy, minTop, maxTop);
      topEl.style.height = `${newH}px`;

      if (typeof onResize === 'function') onResize();
    });

    window.addEventListener('mouseup', () => {
      if (!dragging) return;
      dragging = false;
      resizerEl.classList.remove('dragging');
      document.body.style.cursor = '';

      const h = Math.round(topEl.getBoundingClientRect().height);
      write(h);

      if (typeof onResize === 'function') onResize();
    });
  }

  window.addEventListener('load', () => {
    // 左侧：chat(上) + trace(下)
    // 左侧拖动不需要 resize 图谱，避免误伤
    initVerticalSplit({
      key: 'left_split_v1',
      containerEl: document.querySelector('.left'),
      topEl: document.getElementById('chat'),
      bottomEl: document.getElementById('trace'),
      resizerEl: document.getElementById('left-resizer'),
      minTop: 140,
      minBottom: 160,
      padding: 90,
      onResize: null,
    });

    // 右侧：graph(上) + detail(下)
    // 只有右侧拖动才 resize 图谱
    initVerticalSplit({
      key: 'right_split_v1',
      containerEl: document.querySelector('.right'),
      topEl: document.getElementById('graph'),
      bottomEl: document.getElementById('detail-panel'),
      resizerEl: document.getElementById('right-resizer'),
      minTop: 180,
      minBottom: 140,
      padding: 90,
      onResize: safeResizeChart,
    });
  });
})();
