// Run from the repository root: node --test _internal/pilot-checks.test.cjs
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const read=p=>fs.readFileSync(p,'utf8');
const pages=['index.html','consultation.html','booking.html','price-calculator.html','guides.html','hair-extension-cost-moreton-bay.html','weft-extension-maintenance.html','choosing-weft-hair-extensions.html','privacy.html','service-terms.html','accessibility.html'];
test('public preview headings, footer and noindex',()=>{for(const p of pages){const h=read(p);assert.equal((h.match(/<h1[\s>]/g)||[]).length,1,p);assert.match(h,/noindex/,p);assert.match(h,/\/privacy\.html/,p);assert.match(h,/\/service-terms\.html/,p);assert.match(h,/\/accessibility\.html/,p)}});
test('owner dashboard literal element references and navigation',()=>{const w=read('owner-cloud/worker.js'),h=JSON.parse(w.match(/const HTML=(.*?);\n/s)[1]);const ids=[...h.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]);assert.equal(new Set(ids).size,ids.length);const script=h.match(/<script>([\s\S]*?)<\/script>/)[1];new Function(script);const refs=[...new Set([...script.matchAll(/\$\("([^"]+)"\)/g)].map(m=>m[1]))];assert.deepEqual(refs.filter(id=>!ids.includes(id)&&!['hist-date','hist-time'].includes(id)),[]);for(const [,view] of h.matchAll(/data-view="([^"]+)"/g))assert.ok(ids.includes(view),view)});
test('published package prices match calculator and consultation',()=>{const price=h=>h.match(/const PRICE = Object.freeze\([\s\S]*?\}\);/)[0];assert.equal(price(read('consultation.html')),price(read('price-calculator.html')))});
test('sitemap excludes private and demo paths',()=>{const s=read('sitemap.xml');assert.doesNotMatch(s,/owner-cloud|availability-cloud|calendar-demo|_internal/);assert.equal((s.match(/<loc>/g)||[]).length,pages.length)});
test('security headers defined',()=>{const h=read('_headers');for(const name of ['X-Content-Type-Options','Referrer-Policy','Permissions-Policy','Content-Security-Policy'])assert.ok(h.includes(name),name)});
