// Build only customer-facing assets. Configure Pages to run this script and deploy public-dist after a staged test.
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),out=path.join(root,'public-dist');
const pages=['index.html','consultation.html','booking.html','price-calculator.html','guides.html','hair-extension-cost-moreton-bay.html','weft-extension-maintenance.html','choosing-weft-hair-extensions.html','privacy.html','service-terms.html','accessibility.html'];
const assets=new Set(['static/favicon.svg','static/campaign.js']);
const include=p=>{const src=path.resolve(root,p),dst=path.resolve(out,p);if(!src.startsWith(root+path.sep)||!dst.startsWith(out+path.sep))throw Error('Invalid asset path');if(!fs.statSync(src).isFile())throw Error('Missing asset: '+p);fs.mkdirSync(path.dirname(dst),{recursive:true});fs.copyFileSync(src,dst)};
if(fs.existsSync(out))throw Error('Build output already exists. Use a fresh checkout or remove only public-dist explicitly.');
fs.mkdirSync(out);
const mode=process.env.BIZDR_BUILD_MODE||'preview';
if(!['preview','production'].includes(mode))throw Error('Invalid build mode');
for(const p of [...pages,...(mode==='preview'?['calendar-demo.html']:[])]){const source=fs.readFileSync(path.join(root,p),'utf8');for(const m of source.matchAll(/\/static\/[A-Za-z0-9%_.,()\-/]+(?:\.[A-Za-z0-9]+)?/g)){let rel=decodeURIComponent(m[0].slice(1));if(rel.includes('..'))throw Error('Invalid asset path');assets.add(rel)}include(p);}
for(const p of assets)include(p);
include('_headers');include('_redirects');include('robots.txt');include('sitemap.xml');
if(mode==='production')throw Error('Production build intentionally blocked pending owner approval and final noindex/terms review.');
console.log('Preview output created from allowlisted pages and referenced assets. Private code and internal files excluded.');
