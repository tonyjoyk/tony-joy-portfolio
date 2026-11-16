/* Dev mode colour picker. Loaded only when the URL has ?dev (see the loader at the end of index.html).
   Changes two CSS tokens live: --bg (page background) and --brand (titles, icons, links, focus, footer).
   All other tints derive from them in style.css, so nothing else needs setting.
   A choice is remembered in this browser, in dev mode only. Normal visits always use the CSS defaults. */
(function () {
  var BG = [
    ['White', '#FFFFFF'], ['Monsoon mist', '#F3F5EF'], ['Warm paper', '#F7F5EF'], ['Rain-washed', '#EEF2EC'], ['Sage paper', '#F1F3EA'],
    ['Coconut husk', '#F6F2EA'], ['Cool fog', '#F1F3F2'], ['Laterite dust', '#F6EFE9']
  ];
  var BRAND = [
    ['Link blue', '#4394E2'], ['Deep blue', '#2A76C0'], ['Monsoon green', '#3D6B4F'], ['Paddy field', '#2F5D3A'], ['Backwater teal', '#2E6668'], ['Pepper vine', '#4A5D3A'],
    ['Rain forest', '#25483A'], ['Cardamom', '#557346'], ['Laterite', '#A4553A'], ['Kerala ink', '#2B2A28']
  ];
  var KEY = 'tj-dev-palette', root = document.documentElement;
  var css = getComputedStyle(root);
  var DEFAULT = { bg: css.getPropertyValue('--bg').trim(), brand: css.getPropertyValue('--brand').trim() };
  var state = { bg: DEFAULT.bg, brand: DEFAULT.brand, open: true };
  try { var saved = JSON.parse(localStorage.getItem(KEY) || 'null'); if (saved) state = Object.assign(state, saved); } catch (e) {}

  // WCAG contrast ratio between two hex colours
  function lum(h) {
    var c = [1, 3, 5].map(function (i) { var x = parseInt(h.slice(i, i + 2), 16) / 255; return x <= 0.04045 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }
  function ratio(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }

  var style = document.createElement('style');
  style.textContent = [
    '.devpal{position:fixed;right:16px;bottom:16px;z-index:9999;width:268px;max-width:calc(100vw - 32px);background:#fff;color:#1F1D1A;',
    'border:1px solid rgba(0,0,0,.08);border-radius:10px;box-shadow:0 8px 28px rgba(0,0,0,.14);font:13px/1.4 var(--font-sans);padding:14px}',
    '.devpal h3{margin:0 0 2px;font:500 11px/1.4 var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:#6E6A63}',
    '.devpal__row{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 12px;align-items:center}',
    '.devpal__sw{width:26px;height:26px;border-radius:50%;border:1px solid rgba(0,0,0,.15);cursor:pointer;padding:0}',
    '.devpal__sw[aria-pressed=true]{outline:2px solid #1F1D1A;outline-offset:2px}',
    '.devpal input[type=color]{width:30px;height:26px;border:0;padding:0;background:none;cursor:pointer}',
    '.devpal__name{color:#6E6A63;font-size:12px;min-height:1.4em;margin:-4px 0 14px}',
    '.devpal__cr{font:500 12px/1.4 var(--font-mono);margin:4px 0 10px}',
    '.devpal__cr.bad{color:#B3261E}',
    '.devpal__btns{display:flex;gap:8px}',
    '.devpal__btns button,.devpal__pill{font:inherit;font-size:12px;border:1px solid rgba(0,0,0,.15);background:#fff;border-radius:999px;padding:4px 12px;cursor:pointer}',
    '.devpal__pill{position:fixed;right:16px;bottom:16px;z-index:9999;box-shadow:0 4px 14px rgba(0,0,0,.12)}',
    '.devpal__close{position:absolute;top:8px;right:10px;border:0;background:none;font-size:18px;line-height:1;cursor:pointer;color:#6E6A63}'
  ].join('');
  document.head.appendChild(style);

  var panel = document.createElement('div'); panel.className = 'devpal'; panel.setAttribute('role', 'region'); panel.setAttribute('aria-label', 'Colour picker (dev mode)');
  var pill = document.createElement('button'); pill.className = 'devpal__pill'; pill.type = 'button'; pill.textContent = 'Colours';
  document.body.appendChild(panel); document.body.appendChild(pill);

  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
  function apply(keepPanel) {
    root.style.setProperty('--bg', state.bg); root.style.setProperty('--brand', state.brand);
    var m = document.querySelector('meta[name=theme-color]'); if (m) m.content = state.bg;
    panel.hidden = !state.open; pill.hidden = state.open;
    if (!keepPanel) render();
    save();
  }

  function group(title, list, key) {
    var name = function (hex) { var f = list.filter(function (x) { return x[1].toLowerCase() === hex.toLowerCase(); })[0]; return f ? f[0] : 'Custom'; };
    var h = '<h3>' + title + '</h3><div class="devpal__row">';
    list.forEach(function (c) {
      h += '<button type="button" class="devpal__sw" data-k="' + key + '" data-v="' + c[1] + '" title="' + c[0] + ' ' + c[1] + '" aria-label="' + c[0] +
        '" aria-pressed="' + (c[1].toLowerCase() === state[key].toLowerCase()) + '" style="background:' + c[1] + '"></button>';
    });
    h += '<input type="color" data-k="' + key + '" value="' + state[key] + '" aria-label="Custom ' + title.toLowerCase() + ' colour"></div>';
    h += '<div class="devpal__name">' + name(state[key]) + ' · ' + state[key].toUpperCase() + '</div>';
    return h;
  }

  function render() {
    var r = ratio(state.brand, state.bg), ok = r >= 4.5;
    panel.innerHTML = '<button type="button" class="devpal__close" aria-label="Collapse">×</button>' +
      group('Background', BG, 'bg') + group('Brand: titles and icons', BRAND, 'brand') +
      '<div class="devpal__cr' + (ok ? '' : ' bad') + '">Contrast ' + r.toFixed(1) + ':1 ' + (ok ? '✓ readable' : '✗ below 4.5:1, too light for small titles') + '</div>' +
      '<div class="devpal__btns"><button type="button" data-a="copy">Copy choice</button><button type="button" data-a="reset">Reset</button></div>';
  }

  panel.addEventListener('click', function (e) {
    var t = e.target.closest('button'); if (!t) return;
    if (t.classList.contains('devpal__close')) { state.open = false; return apply(); }
    if (t.dataset.k) { state[t.dataset.k] = t.dataset.v; return apply(); }
    if (t.dataset.a === 'reset') { state.bg = DEFAULT.bg; state.brand = DEFAULT.brand; return apply(); }
    if (t.dataset.a === 'copy') {
      var txt = '--bg: ' + state.bg.toUpperCase() + '; --brand: ' + state.brand.toUpperCase() + ';';
      var done = function () { t.textContent = 'Copied'; setTimeout(function () { t.textContent = 'Copy choice'; }, 1500); };
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(done, function () { prompt('Copy this:', txt); }); else prompt('Copy this:', txt);
    }
  });
  panel.addEventListener('input', function (e) {
    if (e.target.type === 'color') { state[e.target.dataset.k] = e.target.value; apply(true); }   // live, without closing the picker
  });
  panel.addEventListener('change', function (e) {
    if (e.target.type === 'color') { state[e.target.dataset.k] = e.target.value; apply(); }
  });
  pill.addEventListener('click', function () { state.open = true; apply(); });

  apply();
})();
