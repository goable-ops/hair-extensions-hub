// Basic UTM helper + fake checkout for demo
function getParam(key){
  let url=new URL(window.location.href);
  return url.searchParams.get(key);
}
function nav(url){
  const u = new URL(url, window.location.origin);
  // carry UTMs across pages
  const params = new URLSearchParams(window.location.search);
  params.forEach((v,k)=>{ if(!u.searchParams.has(k)) u.searchParams.set(k,v); });
  window.location.href = u.toString();
}
// Fake purchase handler (replace with Stripe/Gumroad)
function completePurchase(next='/thankyou.html'){
  // TODO: integrate Stripe Checkout or your processor here
  const orderId = Math.random().toString(36).slice(2,8).toUpperCase();
  nav(next + (next.includes('?')?'&':'?') + 'orderId=' + orderId);
}