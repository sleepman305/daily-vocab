/**
 * Daily vocab by SirV — app học từ vựng Anh–Việt và Trung–Việt (HSK).
 *
 * Kiến trúc: một trang tĩnh (GitHub Pages), dữ liệu JSON tách theo cấp trong
 * thư mục data/, tiến độ lưu localStorage, service worker (sw.js) cho chạy
 * offline. Không phụ thuộc thư viện ngoài.
 *
 * Lặp lại ngắt quãng (SRS) kiểu hộp Leitner: mỗi từ có "hộp" b. Bấm "Đã nhớ"
 * thì lên hộp, hẹn ôn sau INTERVALS[b] ngày; bấm "Chưa nhớ" thì về hộp 0 và
 * được xếp lại ngay trong lượt đang học. Căn cứ: hệ Leitner (S. Leitner, "So
 * lernt man lernen", 1972) — khoảng ôn tăng gần gấp đôi sau mỗi lần nhớ đúng.
 */
'use strict';

/* ======================= Hằng số & tiện ích ======================= */

const $ = (id) => document.getElementById(id);
const STORE_KEY = 'dv-state-v1';
const TR_KEY = 'dv-tr-v1';
/** Số ngày chờ đến lần ôn kế tiếp theo hộp Leitner (chỉ số = hộp sau khi lên). */
const INTERVALS = [0, 1, 3, 7, 14, 30, 60, 120];
/** Hộp từ đây trở lên coi là "Đã thuộc" (đã nhớ ≥ 3 lần, khoảng ôn ≥ 7 ngày). */
const KNOWN_BOX = 3;

const LEVELS = {
  en: { 1: 'Cơ bản', 2: 'Thông dụng', 3: 'Nâng cao', 4: 'Chuyên sâu' },
  zh: { 1: 'HSK 1', 2: 'HSK 2', 3: 'HSK 3', 4: 'HSK 4', 5: 'HSK 5', 6: 'HSK 6', 7: 'HSK 7–9' },
};
const LEVEL_NOTE = {
  en: { 1: '~2.300 từ hay gặp nhất', 2: 'Giao tiếp, đọc báo', 3: 'Học thuật, chuyên môn', 4: 'Hiếm gặp, thuật ngữ' },
  zh: {},
};
/** Nhãn từ loại tiếng Trung theo mã gắn thẻ ICTCLAS/jieba dùng trong complete-hsk-vocabulary. */
const ZH_POS = {
  n: 'danh từ', v: 'động từ', a: 'tính từ', d: 'phó từ', r: 'đại từ', m: 'số từ', q: 'lượng từ',
  p: 'giới từ', c: 'liên từ', u: 'trợ từ', y: 'trợ từ ngữ khí', e: 'thán từ', vn: 'động từ / danh từ',
  an: 'tính từ / danh từ', ad: 'tính từ / phó từ', t: 'từ thời gian', f: 'phương vị từ', s: 'từ nơi chốn',
  l: 'quán ngữ', i: 'thành ngữ', b: 'từ khu biệt', z: 'từ trạng thái', nr: 'tên người', ns: 'địa danh',
  nt: 'tên tổ chức', nz: 'danh từ riêng', mq: 'số lượng từ', qv: 'lượng từ',
};

/** Số thứ tự ngày theo giờ địa phương (để so hạn ôn không lệch múi giờ). */
function today() {
  return Math.floor((Date.now() - new Date().getTimezoneOffset() * 60000) / 864e5);
}
function dayLabel(n) {
  const d = new Date(n * 864e5);
  return `${d.getUTCDate()}/${d.getUTCMonth() + 1}`;
}
function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
/** Bỏ dấu, chữ thường — dùng cho tìm kiếm và so đáp án không phân biệt dấu. */
function fold(s) {
  return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd');
}
function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
/** Khoảng cách Levenshtein, dừng sớm khi > 2 (chỉ cần biết "sai 1 chữ"). */
function editDistance(a, b) {
  if (Math.abs(a.length - b.length) > 2) return 3;
  let prev = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    for (let j = 1; j <= b.length; j++) {
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    }
    prev = cur;
  }
  return prev[b.length];
}

/* ======================= Trạng thái lưu trữ ======================= */

const DEFAULTS = {
  v: 1,
  lang: 'en',
  mode: 'new',
  f: { en: { lv: '1', topic: 'all' }, zh: { lv: '1' } },
  set: { dur: 15, autoNext: 0, size: 20, goal: 20, autoSpeak: false, accent: 'en-US', rate: 0.9, theme: 'auto', haptic: true },
  srs: {},   // id -> {b: hộp, d: ngày đến hạn, n: số lần ôn, l: số lần quên, v: cấp của từ}
  days: {},  // số ngày -> số lượt chấm trong ngày
  best: 0,   // chuỗi ngày dài nhất
};

/**
 * Đọc trạng thái từ localStorage, trộn với mặc định để bản cũ thiếu khoá vẫn chạy.
 * @returns {object} trạng thái; lỗi đọc/parse thì trả bản mặc định.
 */
function loadState() {
  try {
    const raw = JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
    return {
      ...structuredClone(DEFAULTS), ...raw,
      f: { en: { ...DEFAULTS.f.en, ...(raw.f?.en || {}) }, zh: { ...DEFAULTS.f.zh, ...(raw.f?.zh || {}) } },
      set: { ...DEFAULTS.set, ...(raw.set || {}) },
      srs: raw.srs || {}, days: raw.days || {},
    };
  } catch (e) {
    return structuredClone(DEFAULTS);
  }
}
const S = loadState();
let saveTimer = null;
function save() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(S)); }
    catch (e) { toast('Không lưu được tiến độ (bộ nhớ trình duyệt đầy hoặc bị chặn).'); }
  }, 150);
}

/* ======================= Dữ liệu ======================= */

const DB = { meta: null, files: {} };

/**
 * Tải một tệp dữ liệu (có bộ nhớ đệm trong phiên).
 * @param {string} name tên tệp không đuôi: 'meta', 'en-1'…'en-4', 'zh'.
 * @returns {Promise<Array|object>} dữ liệu đã chuyển thành đối tượng mục từ.
 * @throws Error khi mất mạng lần đầu và chưa có trong cache service worker.
 */
async function loadFile(name) {
  if (DB.files[name]) return DB.files[name];
  const r = await fetch(`data/${name}.json`);
  if (!r.ok) throw new Error('HTTP ' + r.status);
  const raw = await r.json();
  let items;
  if (name.startsWith('en-')) {
    items = raw.map(([t, m, p, ipa, ex, l, c]) => ({ id: 'e:' + t, lang: 'en', t, m, p, ipa, ex, l, c }));
  } else {
    items = raw.map(([t, py, m, g, l, p]) => ({ id: 'z:' + t, lang: 'zh', t, py, m, g, l, p: ZH_POS[p] || '' }));
  }
  DB.files[name] = items;
  return items;
}
async function loadMeta() {
  if (!DB.meta) {
    const r = await fetch('data/meta.json');
    DB.meta = await r.json();
    DB.meta.en.topics.sort((a, b) => a.localeCompare(b, 'vi'));
  }
  return DB.meta;
}
/** Danh sách tệp cần cho một ngôn ngữ và bộ lọc cấp ('all' = mọi cấp). */
function filesFor(lang, lv) {
  if (lang === 'zh') return ['zh'];
  return lv === 'all' ? ['en-1', 'en-2', 'en-3', 'en-4'] : ['en-' + lv];
}
async function loadItems(lang, lv) {
  const parts = await Promise.all(filesFor(lang, lv).map(loadFile));
  let items = parts.flat();
  if (lang === 'zh' && lv !== 'all') items = items.filter((w) => String(w.l) === String(lv));
  return items;
}
/** Tìm mục từ theo id trong mọi tệp đã tải (dùng khi ôn tập). */
async function itemsByIds(ids) {
  // Bản ghi SRS nhớ cấp (v) nên chỉ tải đúng tệp của cấp đó; thiếu v thì tải cả 4.
  const names = new Set();
  for (const id of ids) {
    if (id.startsWith('z:')) names.add('zh');
    else if (S.srs[id]?.v) names.add('en-' + S.srs[id].v);
    else ['en-1', 'en-2', 'en-3', 'en-4'].forEach((n) => names.add(n));
  }
  const all = (await Promise.all([...names].map(loadFile))).flat();
  const map = new Map(all.map((w) => [w.id, w]));
  return ids.map((id) => map.get(id)).filter(Boolean);
}

/* ======================= SRS & thống kê ======================= */

function dueIds(lang) {
  const t = today(), pre = lang === 'zh' ? 'z:' : 'e:';
  return Object.entries(S.srs)
    .filter(([id, r]) => id.startsWith(pre) && r.d <= t)
    .sort((a, b) => a[1].d - b[1].d)
    .map(([id]) => id);
}
function countToday() { return S.days[today()] || 0; }
function bump() {
  const t = today();
  S.days[t] = (S.days[t] || 0) + 1;
  // Chỉ giữ 400 ngày gần nhất cho gọn bộ nhớ.
  const keys = Object.keys(S.days);
  if (keys.length > 400) keys.sort((a, b) => a - b).slice(0, keys.length - 400).forEach((k) => delete S.days[k]);
  S.best = Math.max(S.best || 0, streak());
}
/** Chuỗi ngày học liên tiếp; hôm nay chưa học thì tính đến hôm qua. */
function streak() {
  let d = today(), n = 0;
  if (!S.days[d]) d--;
  while (S.days[d]) { n++; d--; }
  return n;
}
/**
 * Chấm một từ và hẹn ngày ôn.
 * @param {string} id mã mục từ.
 * @param {boolean} good true = "Đã nhớ".
 * @param {number} gain số hộp được lên (2 nếu tự gõ đúng không cần gợi ý).
 * @param {number} lv cấp của từ, lưu kèm để lần ôn chỉ tải đúng tệp dữ liệu.
 * @returns {number} số ngày tới lần ôn kế tiếp.
 */
function grade(id, good, gain = 1, lv = 0) {
  const r = S.srs[id] || { b: 0, d: today(), n: 0, l: 0 };
  if (lv) r.v = lv;
  if (good) r.b = Math.min(INTERVALS.length - 1, r.b + gain);
  else { r.b = 0; r.l++; }
  r.n++;
  r.d = today() + INTERVALS[r.b];
  S.srs[id] = r;
  return INTERVALS[r.b];
}
function nextInterval(id, gain) {
  const b = Math.min(INTERVALS.length - 1, (S.srs[id]?.b || 0) + gain);
  return INTERVALS[b];
}
function daysText(n) { return n <= 0 ? 'hôm nay' : n === 1 ? '1 ngày' : n < 30 ? `${n} ngày` : `${Math.round(n / 30)} tháng`; }

/* ======================= Phát âm ======================= */

let voices = [];
function refreshVoices() { try { voices = speechSynthesis.getVoices(); } catch (e) { voices = []; } }
if ('speechSynthesis' in window) {
  refreshVoices();
  speechSynthesis.onvoiceschanged = refreshVoices;
}
/**
 * Đọc to một chuỗi bằng Web Speech API.
 * @param {string} text nội dung đọc.
 * @param {'en'|'zh'} lang ngôn ngữ; tiếng Anh dùng giọng Mỹ/Anh theo cài đặt.
 * @param {HTMLElement} [btn] nút phát để hiện hiệu ứng đang đọc.
 */
function speak(text, lang, btn) {
  if (!('speechSynthesis' in window)) { toast('Trình duyệt này không hỗ trợ đọc từ.'); return; }
  const code = lang === 'zh' ? 'zh-CN' : S.set.accent;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = code;
  u.rate = Number(S.set.rate) || 0.9;
  if (!voices.length) refreshVoices();
  const v = voices.find((x) => x.lang.replace('_', '-') === code) ||
    voices.find((x) => x.lang.toLowerCase().startsWith(code.slice(0, 2)));
  if (v) u.voice = v;
  else if (voices.length && lang === 'zh') toast('Máy chưa có giọng tiếng Trung. iPhone: Cài đặt › Trợ năng › Nội dung được đọc › Giọng nói.');
  if (btn) {
    btn.classList.add('playing');
    u.onend = u.onerror = () => btn.classList.remove('playing');
  }
  speechSynthesis.speak(u);
}

/* ======================= Dịch câu ví dụ ======================= */

let trCache = {};
try { trCache = JSON.parse(localStorage.getItem(TR_KEY) || '{}'); } catch (e) { /* bỏ qua */ }
/**
 * Dịch câu ví dụ Anh → Việt qua Google Dịch (không bắt buộc, cần mạng).
 * @returns {Promise<string>} bản dịch; '' nếu lỗi/quá 6 giây.
 */
async function translate(text) {
  if (trCache[text]) return trCache[text];
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), 6000);
  try {
    const r = await fetch('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=vi&dt=t&q=' + encodeURIComponent(text), { signal: ctl.signal });
    const data = await r.json();
    const vi = (data[0] || []).map((x) => x[0]).join('').trim();
    if (vi) {
      trCache[text] = vi;
      const keys = Object.keys(trCache);
      if (keys.length > 800) delete trCache[keys[0]];
      try { localStorage.setItem(TR_KEY, JSON.stringify(trCache)); } catch (e) { /* đầy bộ nhớ thì thôi */ }
    }
    return vi;
  } catch (e) {
    return '';
  } finally {
    clearTimeout(t);
  }
}

/* ======================= Giao diện chung ======================= */

let toastTimer = null;
function toast(msg, ms = 2600) {
  const el = $('toast');
  el.textContent = msg;
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.hidden = true; }, ms);
}
function haptic(p) { if (S.set.haptic && navigator.vibrate) try { navigator.vibrate(p); } catch (e) { /* iOS không hỗ trợ */ } }

function applyTheme() {
  const th = S.set.theme;
  if (th === 'auto') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', th);
}

/** Đặt trạng thái chọn cho một nhóm nút segmented (role=radio). */
function setChecked(container, attr, value) {
  container.querySelectorAll(`[${attr}]`).forEach((b) => b.setAttribute('aria-checked', String(b.getAttribute(attr) === String(value))));
}

/* ---------- Bottom sheet ---------- */
let sheetOnClose = null;
/**
 * Mở bảng trượt từ dưới lên.
 * @param {string} title tiêu đề.
 * @param {HTMLElement|string} body nội dung.
 * @param {Function} [onClose] gọi khi đóng.
 */
function openSheet(title, body, onClose) {
  pauseTimer();
  $('sheetTitle').textContent = title;
  const b = $('sheetBody');
  b.replaceChildren();
  if (typeof body === 'string') b.innerHTML = body; else b.append(body);
  $('sheet').hidden = false;
  $('sheetBackdrop').hidden = false;
  sheetOnClose = onClose || null;
  const first = b.querySelector('[aria-checked="true"]') || b.querySelector('button');
  first?.focus({ preventScroll: true });
  first?.scrollIntoView?.({ block: 'nearest' });
}
function closeSheet() {
  if ($('sheet').hidden) return;
  $('sheet').hidden = true;
  $('sheetBackdrop').hidden = true;
  const cb = sheetOnClose;
  sheetOnClose = null;
  cb?.();
  resumeTimer();
}
$('sheetBackdrop').onclick = closeSheet;
/* Vuốt xuống để đóng */
(() => {
  let y0 = null;
  const sh = $('sheet');
  sh.addEventListener('touchstart', (e) => { if ($('sheetBody').scrollTop <= 0) y0 = e.touches[0].clientY; }, { passive: true });
  sh.addEventListener('touchmove', (e) => {
    if (y0 == null) return;
    const dy = e.touches[0].clientY - y0;
    if (dy > 0) sh.style.transform = `translateY(${dy}px)`;
  }, { passive: true });
  sh.addEventListener('touchend', (e) => {
    if (y0 == null) return;
    const dy = e.changedTouches[0].clientY - y0;
    sh.style.transform = '';
    y0 = null;
    if (dy > 90) closeSheet();
  });
})();

/**
 * Dựng danh sách lựa chọn cho sheet.
 * @param {Array<{v:string,label:string,note?:string}>} opts
 * @param {string} cur giá trị đang chọn.
 * @param {Function} onPick gọi với giá trị được chọn.
 */
function optionList(opts, cur, onPick) {
  const wrap = document.createElement('div');
  wrap.setAttribute('role', 'radiogroup');
  for (const o of opts) {
    const b = document.createElement('button');
    b.className = 'opt';
    b.setAttribute('role', 'radio');
    b.setAttribute('aria-checked', String(String(o.v) === String(cur)));
    b.innerHTML = `<span>${esc(o.label)}${o.note ? `<br><small>${esc(o.note)}</small>` : ''}</span>`;
    b.onclick = () => { closeSheet(); onPick(o.v); };
    wrap.append(b);
  }
  return wrap;
}

/* ======================= Điều hướng tab ======================= */

let currentTab = 'study';
function go(tab) {
  if (tab !== 'study') pauseTimer();
  currentTab = tab;
  for (const s of ['study', 'library', 'progress', 'settings']) $('screen-' + s).hidden = s !== tab;
  document.querySelectorAll('.tabbar button').forEach((b) => {
    if (b.dataset.tab === tab) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
  });
  window.scrollTo({ top: 0 });
  if (tab === 'library') renderLibrary(true);
  if (tab === 'progress') renderProgress();
  if (tab === 'study') {
    if (studyDirty) startSession(); else resumeTimer();
    refreshDue();
  }
}
document.querySelectorAll('.tabbar button').forEach((b) => { b.onclick = () => go(b.dataset.tab); });
$('streakChip').onclick = () => go('progress');

/* ======================= Ngôn ngữ ======================= */

function setLang(lang) {
  if (S.lang === lang) return;
  S.lang = lang;
  save();
  setChecked(document.querySelector('.lang-seg'), 'data-lang', lang);
  libQuery.lv = 'all';
  if (currentTab === 'study') startSession();
  else { studyDirty = true; if (currentTab === 'library') renderLibrary(true); if (currentTab === 'progress') renderProgress(); }
  renderStudyChrome();
}
document.querySelectorAll('.lang-seg button').forEach((b) => { b.onclick = () => setLang(b.dataset.lang); });

/* ======================= Màn HỌC ======================= */

const session = { queue: [], i: 0, good: 0, again: 0, seen: new Set(), total: 0, retries: new Map() };
let studyDirty = false;
let card = null;        // mục từ đang hiện
let revealed = false;
let hints = 0;
let typedRight = false;
const timer = { left: 0, total: 0, id: null, paused: false, last: 0 };

/** Vẽ phần khung (chip lọc, placeholder, nhãn) theo ngôn ngữ và chế độ hiện tại. */
function renderStudyChrome() {
  const lang = S.lang, f = S.f[lang];
  setChecked(document.querySelector('.mode-seg'), 'data-mode', S.mode);
  $('levelChipVal').textContent = f.lv === 'all' ? 'Tất cả' : LEVELS[lang][f.lv];
  $('topicChip').hidden = lang !== 'en' || S.mode === 'review';
  $('levelChip').hidden = S.mode === 'review';
  $('topicChipVal').textContent = f.topic && f.topic !== 'all' ? f.topic : 'Tất cả';
  $('timerChipVal').textContent = S.set.dur ? S.set.dur + ' giây' : 'Không giới hạn';
  $('autoChipVal').textContent = S.set.autoNext ? `Tự chuyển ${S.set.autoNext}s` : 'Tự chuyển: Tắt';
  $('autoChip').setAttribute('aria-checked', String(!!S.set.autoNext));
  $('answerInput').placeholder = lang === 'zh' ? 'Gõ pinyin hoặc chữ Hán…' : 'Gõ từ tiếng Anh…';
  $('answerInput').setAttribute('aria-label', lang === 'zh' ? 'Nhập pinyin hoặc chữ Hán' : 'Nhập từ tiếng Anh');
  $('streakNum').textContent = streak();
  refreshDue();
}
function refreshDue() {
  const n = dueIds(S.lang).length;
  $('dueBadge').hidden = !n;
  $('dueBadge').textContent = n > 99 ? '99+' : n;
}

function showPanel(which) {
  // which: 'card' | 'summary' | 'empty' | 'loading'
  const isCard = which === 'card';
  for (const id of ['card', 'dock']) $(id).hidden = !isCard;
  $('answerForm').hidden = !isCard || revealed;
  $('actionsAsk').hidden = !isCard || revealed;
  $('actionsRate').hidden = !isCard || !revealed;
  $('summary').hidden = which !== 'summary';
  $('empty').hidden = which !== 'empty';
  $('loading').hidden = which !== 'loading';
  $('filterChips').hidden = which === 'loading';
}

/**
 * Bắt đầu lượt học mới theo chế độ và bộ lọc hiện tại.
 * Từ mới: lấy các từ chưa có trong SRS, ưu tiên từ hay gặp (dữ liệu đã sắp
 * theo tần suất), trộn nhẹ trong 5 lần cỡ lượt để mỗi lượt không y hệt nhau.
 * Ôn tập: lấy các từ đến hạn, hạn cũ trước.
 */
async function startSession() {
  studyDirty = false;
  stopTimer();
  renderStudyChrome();
  showPanel('loading');
  const lang = S.lang, f = S.f[lang], size = Number(S.set.size) || 20;
  let queue = [];
  try {
    if (S.mode === 'review') {
      queue = await itemsByIds(dueIds(lang).slice(0, size));
    } else {
      $('loadingText').textContent = (f.lv === 'all' || (lang === 'en' && f.topic !== 'all')) ? 'Đang tải toàn bộ kho từ (lần đầu hơi lâu)…' : 'Đang tải kho từ…';
      const lvForLoad = lang === 'en' && f.topic !== 'all' ? 'all' : f.lv;
      let items = await loadItems(lang, lvForLoad);
      if (lang === 'en' && f.topic !== 'all') {
        items = items.filter((w) => w.c === f.topic && (f.lv === 'all' || String(w.l) === String(f.lv)));
      }
      const fresh = items.filter((w) => !S.srs[w.id]);
      queue = shuffle(fresh.slice(0, size * 5)).slice(0, size);
    }
  } catch (e) {
    $('emptyTitle').textContent = 'Không tải được kho từ';
    $('emptyText').textContent = 'Lần đầu mở app cần có mạng để tải dữ liệu. Kiểm tra kết nối rồi thử lại.';
    $('emptyBtn').textContent = 'Thử lại';
    $('emptyBtn').onclick = startSession;
    showPanel('empty');
    return;
  }
  if (!queue.length) {
    if (S.mode === 'review') {
      $('emptyTitle').textContent = 'Chưa có từ nào đến hạn ôn';
      $('emptyText').textContent = 'Học thêm từ mới, app sẽ tự nhắc ôn đúng lúc bạn sắp quên.';
      $('emptyBtn').textContent = 'Học từ mới';
      $('emptyBtn').onclick = () => setMode('new');
    } else {
      $('emptyTitle').textContent = 'Bạn đã học hết nhóm này 👏';
      $('emptyText').textContent = 'Chọn cấp hoặc chủ đề khác để học tiếp, hoặc sang Ôn tập.';
      $('emptyBtn').textContent = 'Đổi cấp độ';
      $('emptyBtn').onclick = openLevelSheet;
    }
    showPanel('empty');
    return;
  }
  Object.assign(session, { queue, i: 0, good: 0, again: 0, seen: new Set(), total: queue.length, retries: new Map() });
  showCard();
}

function setMode(mode) {
  S.mode = mode;
  save();
  startSession();
}
document.querySelectorAll('.mode-seg button').forEach((b) => { b.onclick = () => setMode(b.dataset.mode); });

/** Hiện thẻ ở vị trí session.i, hoặc tổng kết nếu hết hàng đợi. */
function showCard() {
  stopTimer();
  card = session.queue[session.i];
  if (!card) { showSummary(); return; }
  revealed = false;
  hints = 0;
  typedRight = false;
  const zh = card.lang === 'zh';
  const cardEl = $('card');
  cardEl.classList.remove('correct', 'wrong');

  $('sessionBar').style.width = (session.seen.size / session.total * 100) + '%';
  $('cardCount').textContent = `${Math.min(session.seen.size + 1, session.total)}/${session.total}`;
  $('cardLevel').textContent = LEVELS[card.lang][card.l] || '';
  $('promptLabel').textContent = zh ? 'Nghĩa tiếng Việt → chữ Hán' : 'Nghĩa tiếng Việt → tiếng Anh';
  const meaning = zh ? card.m.split('; ').slice(0, 2).join('; ') : card.m;
  $('prompt').textContent = meaning;
  $('prompt').classList.toggle('long', meaning.length > 60);
  $('promptPos').textContent = [card.p, card.c].filter(Boolean).join(' · ');
  $('answer').hidden = true;
  $('tiles').hidden = false;
  renderTiles();

  const inp = $('answerInput');
  inp.value = '';
  $('feedback').textContent = '';
  $('feedback').className = 'feedback';
  $('hintBtn').disabled = false;
  showPanel('card');
  // Chỉ tự đặt con trỏ trên máy có chuột; trên điện thoại bàn phím bật lên che mất thẻ.
  if (matchMedia('(pointer:fine)').matches) inp.focus({ preventScroll: true });
  startTimer();
}

/** Vẽ ô chữ gợi ý: tiếng Anh hiện chữ cái đầu + số ô; tiếng Trung hiện số chữ Hán và pinyin theo mức gợi ý. */
function renderTiles() {
  const box = $('tiles');
  box.replaceChildren();
  const zh = card.lang === 'zh';
  box.className = 'tiles' + (zh ? ' zh' : '');
  if (zh) {
    const chars = [...card.t];
    const syl = card.py.split(/\s+/);
    const aligned = syl.length === chars.length;
    chars.forEach((ch, k) => {
      const t = document.createElement('div');
      t.className = 'tile' + (hints >= 3 && k === 0 ? ' on' : '');
      const top = hints >= 3 && k === 0 ? ch : '？';
      let sub = '';
      if (aligned && hints >= 1) sub = hints >= 2 ? fold(syl[k]) : fold(syl[k])[0];
      t.innerHTML = `<span>${esc(top)}</span>${sub ? `<small>${esc(sub)}</small>` : ''}`;
      box.append(t);
    });
    $('tilesNote').textContent = !aligned && hints >= 1 ? 'Pinyin: ' + (hints >= 2 ? fold(card.py) : fold(card.py).split(/\s+/).map((s) => s[0]).join(' ')) : `${chars.length} chữ Hán`;
    return;
  }
  const letters = [...card.t];
  const count = letters.filter((c) => /[a-z]/i.test(c)).length;
  // Co ô theo từ dài nhất để một từ luôn nằm gọn một dòng (vd "responsibility" 14 chữ trên màn 320px).
  const longest = Math.max(...card.t.split(' ').map((x) => x.length));
  const avail = (box.parentElement.clientWidth || 320) - 36;
  const tw = Math.max(10, Math.min(30, Math.floor(avail / (longest * 1.2))));
  box.style.setProperty('--tw', tw + 'px');
  // Mỗi từ là một nhóm ô không bị ngắt giữa chừng khi xuống dòng.
  let n = 0;
  let group = null;
  for (const c of letters) {
    if (c === ' ' || !group) {
      group = document.createElement('span');
      group.className = 'tile-word';
      box.append(group);
      if (c === ' ') continue;
    }
    const t = document.createElement('div');
    if (/[a-z]/i.test(c)) {
      n++;
      const show = n <= hints + 1;
      t.className = 'tile' + (show ? ' on' : '');
      t.textContent = show ? c : '';
    } else {
      t.className = 'tile sym';
      t.textContent = c;
    }
    group.append(t);
  }
  const words = card.t.split(' ').length;
  $('tilesNote').textContent = `${count} chữ cái` + (words > 1 ? ` · ${words} từ` : '');
}

/* ---------- Đồng hồ ---------- */
function startTimer() {
  stopTimer();
  const dur = Number(S.set.dur) || 0;
  const ring = $('timerRing');
  ring.classList.toggle('off', !dur);
  if (!dur || revealed) return;
  Object.assign(timer, { left: dur * 1000, total: dur * 1000, paused: false, last: performance.now() });
  drawRing();
  timer.id = setInterval(tick, 100);
}
function tick() {
  const now = performance.now();
  if (!timer.paused) timer.left -= now - timer.last;
  timer.last = now;
  drawRing();
  if (timer.left <= 0) { stopTimer(); reveal('timeout'); }
}
function drawRing() {
  const p = Math.max(0, timer.left / timer.total);
  $('ringFg').style.strokeDashoffset = String(97.4 * (1 - p));
  const ring = $('timerRing');
  ring.classList.toggle('low', p < 0.3);
  ring.classList.toggle('paused', timer.paused);
  $('ringText').textContent = timer.paused ? '❚❚' : Math.ceil(Math.max(0, timer.left) / 1000);
}
function stopTimer() { clearInterval(timer.id); timer.id = null; }
function pauseTimer() { cancelAutoNext(); if (timer.id) { timer.paused = true; drawRing(); } }
function resumeTimer() {
  if (timer.id && timer.paused && currentTab === 'study' && $('sheet').hidden) {
    timer.paused = false;
    timer.last = performance.now();
    drawRing();
  }
}
$('timerRing').onclick = () => {
  if (!timer.id) return;
  if (timer.paused) resumeTimer(); else pauseTimer();
};
document.addEventListener('visibilitychange', () => {
  if (document.hidden) pauseTimer();
  else { refreshDue(); $('streakNum').textContent = streak(); }
});

/* ---------- Kiểm tra đáp án ---------- */
function normEn(s) {
  return s.toLowerCase().replace(/[’‘`]/g, "'").replace(/[.!?,;:]+$/g, '').replace(/\s+/g, ' ').trim();
}
function normPinyin(s) {
  return fold(s).replace(/ü|v/g, 'u').replace(/[^a-z]/g, '');
}
/**
 * So câu trả lời với đáp án.
 * Tiếng Anh: không phân biệt hoa/thường, gạch nối coi như dấu cách.
 * Tiếng Trung: nhận chữ Hán, hoặc pinyin có/không dấu thanh, có/không số thanh,
 * có/không dấu cách (vd "nǐ hǎo", "ni3 hao3", "nihao" đều đúng với 你好).
 * @returns {'right'|'close'|'wrong'}
 */
function judge(input) {
  if (card.lang === 'zh') {
    if (/[㐀-鿿]/.test(input)) return input.replace(/\s/g, '') === card.t ? 'right' : 'wrong';
    const a = normPinyin(input), b = normPinyin(card.py);
    return a === b ? 'right' : (b.length > 4 && editDistance(a, b) === 1 ? 'close' : 'wrong');
  }
  const a = normEn(input).replace(/-/g, ' '), b = normEn(card.t).replace(/-/g, ' ');
  if (a === b || a.replace(/ /g, '') === b.replace(/ /g, '')) return 'right';
  return b.length >= 5 && editDistance(a, b) === 1 ? 'close' : 'wrong';
}
$('answerForm').addEventListener('submit', (e) => {
  e.preventDefault();
  if (!card) return;
  if (revealed) { rate(true); return; }
  const v = $('answerInput').value.trim();
  const fb = $('feedback');
  if (!v) {
    fb.textContent = 'Gõ đáp án bạn đoán, hoặc bấm “Xem đáp án”.';
    fb.className = 'feedback';
    return;
  }
  const res = judge(v);
  if (res === 'right') {
    typedRight = true;
    reveal('right');
  } else if (res === 'close') {
    fb.textContent = 'Gần đúng rồi — sai một chữ, thử lại nhé!';
    fb.className = 'feedback warn';
    haptic(30);
  } else {
    fb.textContent = 'Chưa đúng. Thử lại, bấm 💡 Gợi ý, hoặc xem đáp án.';
    fb.className = 'feedback bad';
    const c = $('card');
    c.classList.remove('wrong');
    void c.offsetWidth;
    c.classList.add('wrong');
    haptic([20, 40, 20]);
  }
});

$('hintBtn').onclick = () => {
  if (!card || revealed) return;
  const max = card.lang === 'zh' ? 3 : Math.max(0, card.t.replace(/[^a-z]/gi, '').length - 2);
  if (hints >= max) {
    $('feedback').textContent = 'Đã gợi ý tối đa — đoán thử hoặc xem đáp án.';
    $('feedback').className = 'feedback';
    return;
  }
  hints++;
  renderTiles();
};
$('revealBtn').onclick = () => reveal('manual');
$('skipBtn').onclick = () => {
  if (!card) return;
  session.queue.splice(session.i, 1);
  session.total = Math.max(session.seen.size, session.total - 1);
  showCard();
};

/**
 * Mở đáp án.
 * @param {'right'|'manual'|'timeout'} why lý do mở, quyết định lời nhắn và gợi ý chấm.
 */
function reveal(why) {
  if (!card || revealed) return;
  stopTimer();
  revealed = true;
  const zh = card.lang === 'zh';
  $('tiles').hidden = true;
  $('tilesNote').textContent = '';
  $('answer').hidden = false;
  const w = $('answerWord');
  w.textContent = card.t;
  w.className = 'answer-word' + (zh ? ' zh' : '');
  $('answerSub').textContent = zh ? card.py : [card.ipa, card.p].filter(Boolean).join(' · ');
  $('answerGloss').hidden = !zh;
  $('answerGloss').textContent = zh ? 'EN: ' + card.g : '';
  if (zh && card.m.split('; ').length > 2) $('answerGloss').textContent = 'Nghĩa khác: ' + card.m.split('; ').slice(2).join('; ') + ' · EN: ' + card.g;
  renderExample();

  $('answerInput').blur();
  $('answerForm').hidden = true;
  $('actionsAsk').hidden = true;
  $('actionsRate').hidden = false;
  const gain = typedRight && hints === 0 ? 2 : 1;
  $('goodHint').textContent = 'ôn sau ' + daysText(nextInterval(card.id, gain));
  $('againHint').textContent = 'ôn lại trong lượt này';

  const fb = $('feedback');
  if (why === 'right') {
    fb.textContent = gain === 2 ? 'Chính xác! 🎉 Tự nhớ không cần gợi ý — giãn lịch ôn.' : 'Chính xác! 🎉';
    fb.className = 'feedback good';
    const c = $('card');
    c.classList.remove('correct');
    void c.offsetWidth;
    c.classList.add('correct');
    haptic(25);
    $('goodBtn').focus({ preventScroll: true });
  } else if (why === 'timeout') {
    fb.textContent = 'Hết giờ — xem đáp án rồi tự chấm nhé.';
    fb.className = 'feedback warn';
  } else {
    fb.textContent = 'Bạn nhớ từ này chưa? Tự chấm để app hẹn lịch ôn.';
    fb.className = 'feedback';
  }
  requestAnimationFrame(() => $('answer').scrollIntoView({ block: 'nearest', behavior: 'smooth' }));
  if (S.set.autoSpeak) setTimeout(() => { if (revealed) speak(card.t, card.lang, $('speakBtn')); }, 150);
  scheduleAutoNext(why === 'right');
}

/* ---------- Tự chuyển từ ---------- */
let autoNextId = null;
/**
 * Hẹn tự chấm và sang từ tiếp sau S.set.autoNext giây (0 = tắt).
 * Gõ đúng → tự chấm "Đã nhớ"; hết giờ hoặc bấm xem đáp án → "Chưa nhớ"
 * (không tự nhớ ra được thì cần ôn lại). Nút sẽ được chọn có vạch chạy làm
 * đồng hồ; bật "Tự đọc" thì cộng thêm 1 giây để kịp nghe hết phát âm.
 * @param {boolean} good kết quả sẽ tự chấm.
 */
function scheduleAutoNext(good) {
  cancelAutoNext();
  const sec = Number(S.set.autoNext) || 0;
  if (!sec || !revealed) return;
  const ms = sec * 1000 + (S.set.autoSpeak ? 1000 : 0);
  const btn = good ? $('goodBtn') : $('againBtn');
  btn.style.setProperty('--auto-dur', ms + 'ms');
  btn.classList.add('auto');
  const stop = document.createElement('button');
  stop.className = 'link-btn';
  stop.id = 'autoStop';
  stop.textContent = 'Dừng tự chuyển';
  stop.onclick = () => { cancelAutoNext(); toast('Đã dừng tự chuyển cho từ này — tự chấm nhé.'); };
  $('feedback').append(stop);
  autoNextId = setTimeout(() => { autoNextId = null; rate(good); }, ms);
}
function cancelAutoNext() {
  clearTimeout(autoNextId);
  autoNextId = null;
  $('goodBtn').classList.remove('auto');
  $('againBtn').classList.remove('auto');
  $('autoStop')?.remove();
}

/** Hiện câu ví dụ (chỉ tiếng Anh), tô đậm từ đang học. */
function renderExample() {
  const ex = card.lang === 'en' ? card.ex : '';
  $('example').hidden = !ex;
  if (!ex) return;
  const re = new RegExp(`(${card.t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\w*)`, 'i');
  $('exEn').innerHTML = esc(ex).replace(re, '<mark>$1</mark>');
  const cached = trCache[ex];
  $('exVi').hidden = !cached;
  $('exVi').textContent = cached || '';
  $('exTranslate').hidden = !!cached;
  $('exTranslate').disabled = false;
  $('exTranslate').textContent = 'Dịch câu ví dụ';
}
$('exTranslate').onclick = async () => {
  const shown = card, btn = $('exTranslate');
  btn.disabled = true;
  btn.textContent = 'Đang dịch…';
  const vi = await translate(shown.ex);
  if (card !== shown) return;
  if (vi) {
    $('exVi').textContent = vi;
    $('exVi').hidden = false;
    btn.hidden = true;
  } else {
    btn.disabled = false;
    btn.textContent = 'Không dịch được (cần mạng) — thử lại';
  }
};
$('speakBtn').onclick = () => { if (card) speak(card.t, card.lang, $('speakBtn')); };

/**
 * Tự chấm sau khi mở đáp án.
 * "Chưa nhớ" chèn lại từ vào sau 3 thẻ (tối đa 2 lần/lượt) để ôn ngay khi còn nóng.
 * @param {boolean} good true = "Đã nhớ".
 */
function rate(good) {
  if (!card || !revealed) return;
  cancelAutoNext();
  const gain = typedRight && hints === 0 ? 2 : 1;
  const firstTime = !session.seen.has(card.id);
  grade(card.id, good, gain, card.l);
  if (firstTime) {
    session.seen.add(card.id);
    bump();
    if (good) session.good++; else session.again++;
  }
  if (!good) {
    const n = session.retries.get(card.id) || 0;
    if (n < 2) {
      session.retries.set(card.id, n + 1);
      session.queue.splice(Math.min(session.queue.length, session.i + 4), 0, card);
    }
  }
  haptic(10);
  save();
  $('streakNum').textContent = streak();
  session.i++;
  showCard();
}
$('goodBtn').onclick = () => rate(true);
$('againBtn').onclick = () => rate(false);

function showSummary() {
  stopTimer();
  card = null;
  $('sessionBar').style.width = '100%';
  const total = session.good + session.again;
  const pct = total ? Math.round(session.good / total * 100) : 0;
  $('sumEmoji').textContent = pct >= 80 ? '🏆' : pct >= 50 ? '🎉' : '💪';
  $('sumTitle').textContent = S.mode === 'review' ? 'Xong lượt ôn!' : 'Xong lượt học!';
  const goal = Number(S.set.goal), t = countToday();
  $('sumText').textContent = t >= goal ? `Bạn đã đạt mục tiêu ${goal} từ hôm nay. Tuyệt vời!` : `Còn ${goal - t} từ nữa là đạt mục tiêu hôm nay.`;
  $('sumGood').textContent = session.good;
  $('sumAgain').textContent = session.again;
  $('sumToday').textContent = t;
  const due = dueIds(S.lang).length;
  $('sumReview').hidden = !due || S.mode === 'review';
  $('sumReview').textContent = `Ôn ${due} từ đến hạn`;
  $('sumNext').textContent = S.mode === 'review' && due ? 'Ôn tiếp' : 'Học lượt mới';
  showPanel('summary');
  refreshDue();
}
$('sumNext').onclick = () => startSession();
$('sumReview').onclick = () => setMode('review');

/* ---------- Chip bộ lọc ---------- */
function openLevelSheet() {
  const lang = S.lang, counts = DB.meta?.[lang]?.levels || {};
  const opts = [{ v: 'all', label: 'Tất cả các cấp', note: lang === 'en' ? 'Tải toàn bộ ~85.000 từ' : '' }]
    .concat(Object.entries(LEVELS[lang]).map(([v, label]) => ({
      v, label, note: [counts[v] ? counts[v].toLocaleString('vi-VN') + ' từ' : '', LEVEL_NOTE[lang][v] || ''].filter(Boolean).join(' · '),
    })));
  openSheet(lang === 'zh' ? 'Chọn cấp HSK' : 'Chọn cấp độ', optionList(opts, S.f[lang].lv, (v) => {
    S.f[lang].lv = v;
    save();
    startSession();
  }));
}
$('levelChip').onclick = openLevelSheet;
$('topicChip').onclick = async () => {
  const meta = await loadMeta();
  const opts = [{ v: 'all', label: 'Tất cả chủ đề' }].concat(meta.en.topics.map((t) => ({ v: t, label: t })));
  openSheet('Chọn chủ đề', optionList(opts, S.f.en.topic, (v) => {
    S.f.en.topic = v;
    if (v !== 'all') S.f.en.lv = 'all';
    save();
    startSession();
  }));
};
const DURATIONS = [[0, 'Không giới hạn'], [10, '10 giây'], [15, '15 giây'], [20, '20 giây'], [30, '30 giây'], [60, '60 giây']];
$('timerChip').onclick = () => {
  openSheet('Thời gian đoán mỗi từ', optionList(DURATIONS.map(([v, label]) => ({ v, label })), S.set.dur, (v) => {
    S.set.dur = Number(v);
    save();
    renderStudyChrome();
    renderSettings();
    if (card && !revealed) startTimer();
  }));
};

const AUTO_NEXT = [[0, 'Tắt', 'Tự bấm “Đã nhớ / Chưa nhớ” để sang từ'], [2, 'Sau 2 giây'], [3, 'Sau 3 giây'], [5, 'Sau 5 giây'], [8, 'Sau 8 giây']];
$('autoChip').onclick = () => {
  openSheet('Tự chuyển sang từ tiếp theo', optionList(
    AUTO_NEXT.map(([v, label, note]) => ({ v, label, note: note || 'Gõ đúng → Đã nhớ · Không nhớ ra → Chưa nhớ' })),
    S.set.autoNext, (v) => {
      S.set.autoNext = Number(v);
      save();
      renderStudyChrome();
      renderSettings();
      if (card && revealed) scheduleAutoNext(typedRight);
    }));
};

/* ---------- Phím tắt (máy tính) ---------- */
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') { closeSheet(); return; }
  if (currentTab !== 'study' || !$('sheet').hidden || !card) return;
  const typing = e.target === $('answerInput');
  if (revealed) {
    if (e.key === '1') { e.preventDefault(); rate(false); }
    else if (e.key === '2' || (e.key === 'Enter' && !typing && e.target.tagName !== 'BUTTON')) { e.preventDefault(); rate(true); }
    else if (e.key.toLowerCase() === 'p' && !typing) speak(card.t, card.lang, $('speakBtn'));
  } else if (!typing && e.key === ' ') { e.preventDefault(); reveal('manual'); }
});

/* ======================= Màn KHO TỪ ======================= */

const libQuery = { q: '', lv: 'all', rows: [], shown: 0 };
let libToken = 0;
function renderLibLevels() {
  const box = $('libLevels'), lang = S.lang;
  box.replaceChildren();
  const add = (v, label) => {
    const b = document.createElement('button');
    b.className = 'chip';
    b.setAttribute('role', 'radio');
    b.setAttribute('aria-checked', String(libQuery.lv === v));
    b.textContent = label;
    b.onclick = () => { libQuery.lv = v; renderLibrary(true); };
    box.append(b);
  };
  add('all', 'Tất cả');
  Object.entries(LEVELS[lang]).forEach(([v, l]) => add(v, l));
}
function wordState(id) {
  const r = S.srs[id];
  return !r ? '' : r.b >= KNOWN_BOX ? 'known' : 'learning';
}
/**
 * Lọc và xếp hạng kho từ: khớp nguyên từ > bắt đầu bằng > nghĩa chứa > từ chứa.
 * Tìm không dấu ("hoc" khớp "học"); tiếng Trung khớp cả pinyin không dấu.
 */
async function renderLibrary(reset) {
  const token = ++libToken, lang = S.lang;
  renderLibLevels();
  $('search').placeholder = lang === 'zh' ? 'Tìm chữ Hán, pinyin hoặc nghĩa…' : 'Tìm từ tiếng Anh hoặc nghĩa tiếng Việt…';
  if (reset) { $('wordList').replaceChildren(); $('libCount').textContent = 'Đang tải…'; }
  let items;
  try { items = await loadItems(lang, libQuery.lv); }
  catch (e) { $('libCount').textContent = 'Không tải được kho từ — cần mạng ở lần mở đầu.'; return; }
  if (token !== libToken) return;
  const q = fold(libQuery.q.trim());
  let rows;
  if (!q) rows = items;
  else {
    const qz = q.replace(/\s+/g, '');
    const scored = [];
    for (const w of items) {
      w._k ??= fold(w.t);
      w._m ??= fold(w.m);
      if (lang === 'zh') w._p ??= fold(w.py).replace(/\s+/g, '');
      let s = -1;
      if (w._k === q || (lang === 'zh' && w._p === qz)) s = 0;
      else if (w._k.startsWith(q) || (lang === 'zh' && w._p.startsWith(qz))) s = 1;
      else if (w._m.startsWith(q) || w._m.includes('; ' + q) || w._m.includes(', ' + q)) s = 2;
      else if (w._m.includes(q)) s = 3;
      else if (w._k.includes(q)) s = 4;
      if (s >= 0) scored.push([s, w]);
    }
    scored.sort((a, b) => a[0] - b[0]);
    rows = scored.map((x) => x[1]);
  }
  libQuery.rows = rows;
  libQuery.shown = 0;
  $('wordList').replaceChildren();
  $('libCount').textContent = rows.length ? `${rows.length.toLocaleString('vi-VN')} từ` : 'Không tìm thấy từ nào.';
  moreLibrary();
}
function moreLibrary() {
  const list = $('wordList'), end = Math.min(libQuery.rows.length, libQuery.shown + 60);
  const frag = document.createDocumentFragment();
  for (let k = libQuery.shown; k < end; k++) {
    const w = libQuery.rows[k];
    const li = document.createElement('li');
    li.className = 'word-row';
    li.tabIndex = 0;
    const st = wordState(w.id);
    const meta = w.lang === 'zh' ? w.py : (w.ipa || w.p || '');
    li.innerHTML = `<span class="wr-state ${st}" title="${st === 'known' ? 'Đã thuộc' : st ? 'Đang học' : ''}"></span>
      <div class="wr-main"><div class="wr-top"><span class="wr-word ${w.lang === 'zh' ? 'zh' : ''}">${esc(w.t)}</span><span class="wr-meta">${esc(meta)}</span></div>
      <div class="wr-mean">${esc(w.m)}</div></div>
      <button class="icon-btn" aria-label="Nghe ${esc(w.t)}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/></svg></button>`;
    li.querySelector('button').onclick = (e) => { e.stopPropagation(); speak(w.t, w.lang, e.currentTarget); };
    li.onclick = () => openDetail(w);
    li.onkeydown = (e) => { if (e.key === 'Enter') openDetail(w); };
    frag.append(li);
  }
  list.append(frag);
  libQuery.shown = end;
}
new IntersectionObserver((ents) => {
  if (ents[0].isIntersecting && currentTab === 'library' && libQuery.shown < libQuery.rows.length) moreLibrary();
}, { rootMargin: '400px' }).observe($('libSentinel'));
let searchTimer = null;
$('search').addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => { libQuery.q = $('search').value; renderLibrary(false); }, 180);
});

/** Bảng chi tiết một từ trong kho: nghĩa, ví dụ, trạng thái ôn và nút thêm/bỏ khỏi ôn tập. */
function openDetail(w) {
  const d = document.createElement('div');
  d.className = 'detail';
  const r = S.srs[w.id];
  const status = !r ? 'Chưa học' : r.b >= KNOWN_BOX ? `Đã thuộc · ôn lại ${dayLabel(r.d)}` : `Đang học · ôn ${r.d <= today() ? 'hôm nay' : dayLabel(r.d)}`;
  d.innerHTML = `
    <div class="answer-main"><span class="answer-word ${w.lang === 'zh' ? 'zh' : ''}">${esc(w.t)}</span>
      <button class="icon-btn" id="dSpeak" aria-label="Nghe phát âm"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/></svg></button></div>
    <p class="answer-sub">${esc(w.lang === 'zh' ? w.py : [w.ipa, w.p].filter(Boolean).join(' · '))}</p>
    <p class="meaning">${esc(w.m)}</p>
    ${w.lang === 'zh' ? `<p class="answer-gloss">EN: ${esc(w.g)}${w.p ? ' · ' + esc(w.p) : ''}</p>` : ''}
    ${w.ex ? `<div class="example"><p class="ex-en">${esc(w.ex)}</p></div>` : ''}
    <p class="pill" style="align-self:flex-start">${esc(LEVELS[w.lang][w.l] || '')} · ${esc(status)}</p>
    <div class="actions"><button class="btn ${r ? 'ghost' : 'primary'}" id="dToggle">${r ? 'Bỏ khỏi danh sách ôn' : '＋ Thêm vào ôn tập hôm nay'}</button></div>`;
  openSheet(w.lang === 'zh' ? 'Chi tiết chữ Hán' : 'Chi tiết từ', d);
  d.querySelector('#dSpeak').onclick = (e) => speak(w.t, w.lang, e.currentTarget);
  d.querySelector('#dToggle').onclick = () => {
    if (S.srs[w.id]) { delete S.srs[w.id]; toast('Đã bỏ khỏi danh sách ôn.'); }
    else { S.srs[w.id] = { b: 0, d: today(), n: 0, l: 0, v: w.l }; toast('Đã thêm — vào Học › Ôn tập để ôn ngay.'); }
    save();
    refreshDue();
    closeSheet();
    const row = [...$('wordList').children].find((li) => li.querySelector('.wr-word')?.textContent === w.t);
    if (row) row.querySelector('.wr-state').className = 'wr-state ' + wordState(w.id);
  };
}

/* ======================= Màn TIẾN ĐỘ ======================= */

async function renderProgress() {
  const goal = Number(S.set.goal), t = countToday();
  $('goalNum').textContent = t;
  $('goalOf').textContent = `/ ${goal} từ`;
  $('goalFg').style.strokeDashoffset = String(326.7 * (1 - Math.min(1, t / goal)));
  $('goalTitle').textContent = t >= goal ? 'Đạt mục tiêu hôm nay! 🎯' : 'Mục tiêu hôm nay';
  $('goalSub').textContent = t >= goal ? 'Học thêm để vượt mục tiêu, hoặc nghỉ ngơi — mai quay lại giữ chuỗi 🔥' : `Còn ${goal - t} từ nữa. Học hoặc ôn đều được tính.`;
  const due = dueIds(S.lang).length;
  $('goalGo').textContent = due ? `Ôn ${due} từ đến hạn` : 'Học tiếp';
  $('goalGo').onclick = () => { if (due) { S.mode = 'review'; save(); } studyDirty = true; go('study'); };
  $('stStreak').textContent = streak();
  $('stBest').textContent = Math.max(S.best || 0, streak());
  $('stDue').textContent = due;

  // Biểu đồ 7 ngày
  const wk = $('weekChart');
  wk.replaceChildren();
  const td = today();
  const vals = Array.from({ length: 7 }, (_, k) => S.days[td - 6 + k] || 0);
  const max = Math.max(goal, ...vals);
  const names = ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'];
  vals.forEach((v, k) => {
    const dn = td - 6 + k;
    const el = document.createElement('div');
    el.className = 'day' + (v >= goal ? ' hit' : '') + (k === 6 ? ' today' : '');
    el.innerHTML = `<b>${v || ''}</b><i style="height:${Math.max(4, v / max * 80)}px"></i><span>${k === 6 ? 'Nay' : names[new Date(dn * 864e5).getUTCDay()]}</span>`;
    wk.append(el);
  });

  // Tiến độ theo cấp: dùng meta.json để biết tổng mà không phải tải hết dữ liệu.
  const lang = S.lang;
  $('progLang').textContent = lang === 'zh' ? 'Tiếng Trung' : 'Tiếng Anh';
  const meta = await loadMeta().catch(() => null);
  const box = $('levelProgress');
  box.replaceChildren();
  const pre = lang === 'zh' ? 'z:' : 'e:';
  const byLevel = {};
  for (const [id, r] of Object.entries(S.srs)) {
    if (!id.startsWith(pre)) continue;
    const lv = r.v ?? '?';
    byLevel[lv] ??= { k: 0, l: 0 };
    if (r.b >= KNOWN_BOX) byLevel[lv].k++; else byLevel[lv].l++;
  }
  for (const [lv, label] of Object.entries(LEVELS[lang])) {
    const total = meta?.[lang]?.levels?.[lv] || 0;
    const s = byLevel[lv] || { k: 0, l: 0 };
    const row = document.createElement('div');
    row.innerHTML = `<div class="lv-top"><b>${label}</b><span>${s.k.toLocaleString('vi-VN')} thuộc · ${s.l.toLocaleString('vi-VN')} đang học / ${total.toLocaleString('vi-VN')}</span></div>
      <div class="lv-bar"><div class="k" style="width:${total ? s.k / total * 100 : 0}%"></div><div class="l" style="width:${total ? s.l / total * 100 : 0}%"></div></div>`;
    box.append(row);
  }
  if (byLevel['?']) {
    const p = document.createElement('p');
    p.className = 'note';
    p.style.margin = '0';
    p.textContent = `${byLevel['?'].k + byLevel['?'].l} từ khác đang trong danh sách ôn.`;
    box.append(p);
  }
}

/* ======================= Màn CÀI ĐẶT ======================= */

/**
 * Dựng một nhóm segmented cho cài đặt.
 * @param {string} id id phần tử chứa.
 * @param {Array<[any,string]>} opts cặp [giá trị, nhãn].
 * @param {string} key khoá trong S.set.
 * @param {Function} [after] gọi sau khi đổi.
 */
function segSetting(id, opts, key, after) {
  const box = $(id);
  box.setAttribute('role', 'radiogroup');
  box.replaceChildren();
  for (const [v, label] of opts) {
    const b = document.createElement('button');
    b.setAttribute('role', 'radio');
    b.dataset.v = String(v);
    b.setAttribute('aria-checked', String(String(S.set[key]) === String(v)));
    b.textContent = label;
    b.onclick = () => {
      S.set[key] = typeof v === 'number' ? Number(v) : v;
      save();
      setChecked(box, 'data-v', v);
      after?.();
    };
    box.append(b);
  }
}
function renderSettings() {
  segSetting('setDuration', [[0, 'Tắt'], [10, '10s'], [15, '15s'], [30, '30s']], 'dur', () => { renderStudyChrome(); if (card && !revealed) startTimer(); });
  segSetting('setAutoNext', [[0, 'Tắt'], [2, '2s'], [3, '3s'], [5, '5s']], 'autoNext', renderStudyChrome);
  segSetting('setSize', [[10, '10'], [20, '20'], [30, '30'], [50, '50']], 'size', () => { studyDirty = true; });
  segSetting('setGoal', [[10, '10'], [20, '20'], [30, '30'], [50, '50']], 'goal');
  segSetting('setAccent', [['en-US', 'Mỹ'], ['en-GB', 'Anh']], 'accent');
  segSetting('setRate', [[0.75, 'Chậm'], [0.9, 'Vừa'], [1, 'Nhanh']], 'rate');
  segSetting('setTheme', [['auto', 'Tự động'], ['light', 'Sáng'], ['dark', 'Tối']], 'theme', applyTheme);
  $('setAutoSpeak').checked = !!S.set.autoSpeak;
  $('setHaptic').checked = !!S.set.haptic;
}
$('setAutoSpeak').onchange = (e) => { S.set.autoSpeak = e.target.checked; save(); };
$('setHaptic').onchange = (e) => { S.set.haptic = e.target.checked; save(); };
$('testVoice').onclick = () => speak(S.lang === 'zh' ? '你好，欢迎学习中文' : 'Welcome to Daily vocab', S.lang);

$('exportBtn').onclick = () => {
  const d = new Date();
  const name = `daily-vocab-sao-luu-${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}.json`;
  const blob = new Blob([JSON.stringify({ app: 'daily-vocab', ...S }, null, 1)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
  toast('Đã tạo tệp sao lưu ' + name);
};
$('importFile').onchange = async (e) => {
  const f = e.target.files[0];
  e.target.value = '';
  if (!f) return;
  try {
    const data = JSON.parse(await f.text());
    if (data.app !== 'daily-vocab' || typeof data.srs !== 'object') throw new Error('sai định dạng');
    const n = Object.keys(data.srs).length;
    if (!confirm(`Khôi phục ${n} từ đã học từ tệp này? Tiến độ hiện tại trên máy sẽ bị thay thế.`)) return;
    delete data.app;
    Object.assign(S, loadStateFrom(data));
    save();
    applyTheme();
    renderSettings();
    renderStudyChrome();
    toast(`Đã khôi phục ${n} từ.`);
    studyDirty = true;
  } catch (err) {
    toast('Tệp không đúng định dạng sao lưu của Daily vocab.');
  }
};
function loadStateFrom(raw) {
  return {
    ...structuredClone(DEFAULTS), ...raw,
    f: { en: { ...DEFAULTS.f.en, ...(raw.f?.en || {}) }, zh: { ...DEFAULTS.f.zh, ...(raw.f?.zh || {}) } },
    set: { ...DEFAULTS.set, ...(raw.set || {}) },
  };
}
$('resetBtn').onclick = () => {
  const n = Object.keys(S.srs).length;
  if (!confirm(`Xoá toàn bộ tiến độ (${n} từ, chuỗi ${streak()} ngày)? Không hoàn tác được.`)) return;
  S.srs = {};
  S.days = {};
  S.best = 0;
  save();
  renderStudyChrome();
  studyDirty = true;
  toast('Đã xoá tiến độ.');
};

/* ---------- Cài như ứng dụng (PWA) ---------- */
let installEvt = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  installEvt = e;
  $('installBtn').hidden = false;
});
$('installBtn').onclick = async () => {
  if (!installEvt) return;
  installEvt.prompt();
  await installEvt.userChoice.catch(() => null);
  installEvt = null;
  $('installBtn').hidden = true;
};
if (matchMedia('(display-mode: standalone)').matches || navigator.standalone) {
  $('installNote').textContent = 'Đã cài trên máy này. App chạy được cả khi không có mạng.';
}
if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
  navigator.serviceWorker.register('sw.js').catch(() => { /* chạy được không cần SW */ });
}

/* ======================= Khởi động ======================= */

applyTheme();
setChecked(document.querySelector('.lang-seg'), 'data-lang', S.lang);
renderSettings();
loadMeta().catch(() => null);
startSession();
