// triples_resizer.js
// 目标：只让左侧“三元组抽取”区域（#trace）支持上下拖拽调节高度。
// - 默认不改变原布局
// - 拖拽后记住到 localStorage

(function () {
  const KEY = 'trace_height_v1';
  const MIN = 120;
  const MAX_RATIO = 0.7; // 最大不超过左侧可用高度的 70%

  function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
  }

  function readHeight() {
    try {
      const v = parseInt(localStorage.getItem(KEY) || '', 10);
      return Number.isFinite(v) ? v : null;
    } catch (_) {
      return null;
    }
  }

  function writeHeight(h) {
    try {
      localStorage.setItem(KEY, String(Math.round(h)));
    } catch (_) {}
  }

  window.addEventListener('load', () => {
    const left = document.querySelector('.left');
    const trace = document.getElementById('trace');
    const handle = document.getElementById('trace-resizer');

    if (!left || !trace || !handle) return;

    // 恢复之前用户调过的高度
    const saved = readHeight();
    if (saved) {
      trace.style.height = `${saved}px`;
      trace.style.maxHeight = 'none';
    }

    handle.addEventListener('mousedown', (e) => {
      e.preventDefault();
      handle.classList.add('dragging');

      const startY = e.clientY;
      const startH = trace.getBoundingClientRect().height;
      const leftH = left.getBoundingClientRect().height;
      const maxH = Math.floor(leftH * MAX_RATIO);

      function onMove(ev) {
        const dy = ev.clientY - startY;
        const newH = clamp(startH + dy, MIN, maxH);
        trace.style.height = `${newH}px`;
        trace.style.maxHeight = 'none';
      }

      function onUp() {
        handle.classList.remove('dragging');
        window.removeEventListener('mousemove', onMove);
        window.removeEventListener('mouseup', onUp);
        const h = trace.getBoundingClientRect().height;
        writeHeight(h);
      }

      window.addEventListener('mousemove', onMove);
      window.addEventListener('mouseup', onUp);
    });
  });
})();
