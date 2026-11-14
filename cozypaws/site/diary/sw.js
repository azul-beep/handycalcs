// Paw Diary (Cozy Paws): funciona sin internet. Versión 181f9f3392 (cambia sola cuando cambia la app).
const C='pawdiary-181f9f3392',PRE=["/diary/", "/diary/es/", "/diary/manifest.webmanifest", "/diary/es/manifest.webmanifest", "/img/logo-160.png", "/img/logo-ilustrado.png", "/img/icon.png", "/fonts/Yesteryear-Regular.woff2", "/fonts/AbrilFatface-Regular.woff2", "/fonts/Lora.woff2", "/diary/icons/icon-192.png", "/diary/icons/icon-512.png"];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(PRE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x.startsWith('pawdiary-')&&x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('notificationclick',e=>{e.notification.close();e.waitUntil(clients.openWindow('/diary/#rem'))});
self.addEventListener('fetch',e=>{const r=e.request,u=new URL(r.url);if(r.method!=='GET'||u.origin!==location.origin)return;
 if(r.mode==='navigate'){e.respondWith(fetch(r).then(x=>{const y=x.clone();caches.open(C).then(c=>c.put(u.pathname,y));return x}).catch(()=>caches.match(u.pathname).then(m=>m||caches.match('/diary/'))));return}
 e.respondWith(caches.match(r).then(m=>{const f=fetch(r).then(x=>{if(x.ok){const y=x.clone();caches.open(C).then(c=>c.put(r,y))}return x}).catch(()=>m);return m||f}));});
