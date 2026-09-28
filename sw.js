/**
 * Service worker của Daily vocab — cho app chạy offline.
 *
 * - Vỏ app (HTML/CSS/JS/icon): tải sẵn khi cài; khi mở thì trả bản trong cache
 *   ngay và cập nhật ngầm (stale-while-revalidate), nên lần mở sau có bản mới.
 * - Dữ liệu từ vựng (data/*.json): cache khi lần đầu dùng tới (cache-first),
 *   vì tệp lớn và chỉ đổi khi phát hành bản dữ liệu mới — khi đó tăng VERSION.
 * - Yêu cầu ra ngoài (Google Dịch) đi thẳng mạng, không cache ở đây.
 */
const VERSION = 'dv-2.2.0';
const SHELL = ['./', 'index.html', 'app.css', 'app.js', 'manifest.webmanifest', 'data/meta.json',
  'icons/icon-192.png', 'icons/apple-touch-icon.png', 'icons/favicon.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  const isData = url.pathname.includes('/data/') && !url.pathname.endsWith('meta.json');
  e.respondWith(caches.open(VERSION).then(async (cache) => {
    const hit = await cache.match(e.request, { ignoreSearch: true });
    if (isData && hit) return hit;
    const net = fetch(e.request).then((r) => {
      if (r.ok) cache.put(e.request, r.clone());
      return r;
    });
    if (hit) { e.waitUntil(net.catch(() => null)); return hit; }
    return net;
  }));
});
