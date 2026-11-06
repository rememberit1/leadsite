// Tiny tracker: approximates calls by counting tel: clicks. Real call counts need a call-tracking number.
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="tel:"]');if(!a)return;
try{navigator.sendBeacon('/api/call-click',JSON.stringify({page:location.pathname,ts:Date.now()}))}catch(_){}});
document.querySelectorAll('input[name=page]').forEach(function(i){i.value=location.pathname});
