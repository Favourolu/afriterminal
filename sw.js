const CACHE = 'afriterminal-v2';
const SHELL = [
  'dashboard.html',
  'privacy.html',
  'manifest.json',
  'ngx_live_prices.csv',
  'african_exchanges.csv',
  'commodities_data.csv',
  'macro_data.csv',
  'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',
  'https://unpkg.com/lightweight-charts@3.8.0/dist/lightweight-charts.standalone.production.js'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const url = e.request.url;
  if (
    url.includes('open.er-api.com') ||
    url.includes('coingecko.com') ||
    url.includes('worldbank.org') ||
    url.includes('allorigins.win') ||
    url.includes('african-markets.com')
  ) {
    e.respondWith(fetch(e.request).catch(() => new Response('{}', {headers:{'Content-Type':'application/json'}})));
    return;
  }
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
