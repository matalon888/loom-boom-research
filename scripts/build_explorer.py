import json, os

payload = open('comments_payload.json', encoding='utf-8').read()

HEAD = r'''<title>Loom Reviews, Unfiltered</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>
:root{
  --paper:#F2F5F6; --card:#FFFFFF; --ink:#101A1F; --ink-soft:#2C3B42; --muted:#5A6B72;
  --rule:#D6E0E3; --rule-soft:#E6EDEF;
  --rec:#C0332A; --rec-wash:#F7E7E4;
  --boom:#0B6F79; --boom-wash:#E0EFF0;
  --warm:#9A6B1F; --warm-wash:#F6EDDC;
  --shadow:0 1px 2px rgba(16,26,31,.05), 0 8px 24px -16px rgba(16,26,31,.22);
  --display:"Familjen Grotesk","Helvetica Neue",Arial,sans-serif;
  --body:"Source Serif 4",Georgia,"Times New Roman",serif;
  --mono:"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --paper:#0C1316; --card:#131E22; --ink:#E7EFF1; --ink-soft:#C3D2D6; --muted:#8DA2A9;
    --rule:#22343A; --rule-soft:#1A2A2F;
    --rec:#F0796A; --rec-wash:#2A1613;
    --boom:#48BFC7; --boom-wash:#0E2A2C;
    --warm:#D9A75A; --warm-wash:#2A2213;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -18px rgba(0,0,0,.8);
  }
}
:root[data-theme="dark"]{
  --paper:#0C1316; --card:#131E22; --ink:#E7EFF1; --ink-soft:#C3D2D6; --muted:#8DA2A9;
  --rule:#22343A; --rule-soft:#1A2A2F;
  --rec:#F0796A; --rec-wash:#2A1613;
  --boom:#48BFC7; --boom-wash:#0E2A2C;
  --warm:#D9A75A; --warm-wash:#2A2213;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 30px -18px rgba(0,0,0,.8);
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
  font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px 90px}

header{padding:52px 0 26px}
.kicker{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--muted);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.dot{width:9px;height:9px;border-radius:50%;background:var(--rec);flex:none;box-shadow:0 0 0 3px var(--rec-wash)}
h1{font-family:var(--display);font-weight:700;font-size:clamp(2.1rem,5.2vw,3.5rem);
  line-height:1;letter-spacing:-.025em;margin:18px 0 0;text-wrap:balance}
.sub{color:var(--ink-soft);max-width:56ch;margin:14px 0 0;font-size:1.04rem}
.sub a{color:var(--boom)}

/* counts */
.counts{display:grid;grid-template-columns:repeat(auto-fit,minmax(128px,1fr));gap:1px;
  background:var(--rule);border:1px solid var(--rule);margin:26px 0 0}
.cnt{background:var(--card);padding:13px 15px}
.cnt .n{font-family:var(--mono);font-weight:600;font-size:1.3rem;display:block;line-height:1.1;
  font-variant-numeric:tabular-nums}
.cnt .l{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--muted);margin-top:5px;display:block}

/* controls */
.controls{position:sticky;top:0;z-index:20;background:var(--paper);
  padding:16px 0 14px;border-bottom:1px solid var(--rule);margin-top:30px}
.searchrow{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
#q{flex:1 1 260px;min-width:0;font-family:var(--body);font-size:1rem;padding:11px 14px;
  background:var(--card);color:var(--ink);border:1px solid var(--rule);outline:none}
#q:focus{border-color:var(--boom);box-shadow:0 0 0 3px var(--boom-wash)}
#q::placeholder{color:var(--muted)}
select{font-family:var(--mono);font-size:12px;padding:11px 12px;background:var(--card);
  color:var(--ink);border:1px solid var(--rule);outline:none}
select:focus{border-color:var(--boom);box-shadow:0 0 0 3px var(--boom-wash)}

.chips{display:flex;gap:7px;flex-wrap:wrap;margin-top:11px}
.chipbtn{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;
  padding:6px 11px;background:transparent;color:var(--muted);border:1px solid var(--rule);
  cursor:pointer;transition:none}
.chipbtn:hover{color:var(--ink);border-color:var(--muted)}
.chipbtn:focus-visible{outline:2px solid var(--boom);outline-offset:2px}
.chipbtn[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.chipbtn .k{opacity:.55;margin-left:6px;font-variant-numeric:tabular-nums}

.status{font-family:var(--mono);font-size:11.5px;color:var(--muted);margin-top:11px;
  font-variant-numeric:tabular-nums;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.status b{color:var(--ink);font-weight:600}
.clear{background:none;border:none;color:var(--boom);font-family:var(--mono);font-size:11.5px;
  cursor:pointer;padding:0;text-decoration:underline}

/* list */
#list{display:flex;flex-direction:column;gap:12px;margin-top:22px}
.row{background:var(--card);border:1px solid var(--rule);padding:15px 17px;box-shadow:var(--shadow)}
.row.neg{border-left:3px solid var(--rec)}
.row.pos{border-left:3px solid var(--boom)}
.row.mid{border-left:3px solid var(--warm)}
.row.none{border-left:3px solid var(--rule)}
.meta{display:flex;gap:9px;align-items:center;flex-wrap:wrap;margin-bottom:8px}
.tag{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  padding:3px 7px;border:1px solid var(--rule);color:var(--muted);white-space:nowrap}
.tag.play,.tag.ios{color:var(--rec);border-color:var(--rec)}
.tag.reddit,.tag.hn{color:var(--warm);border-color:var(--warm)}
.stars{font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:var(--rec)}
.stars.hi{color:var(--boom)}
.stars.mid{color:var(--warm)}
.small{font-family:var(--mono);font-size:10.5px;color:var(--muted);font-variant-numeric:tabular-nums}
.small a{color:var(--boom)}
.txt{font-size:1rem;line-height:1.56;color:var(--ink-soft);white-space:pre-wrap;
  overflow-wrap:anywhere}
.txt mark{background:var(--boom-wash);color:var(--ink);padding:0 2px}
.more{background:none;border:none;color:var(--boom);font-family:var(--mono);font-size:11px;
  cursor:pointer;padding:4px 0 0;text-decoration:underline}

#loadmore{margin:26px auto 0;display:block;font-family:var(--mono);font-size:12px;
  letter-spacing:.1em;text-transform:uppercase;padding:13px 30px;background:var(--card);
  color:var(--ink);border:1px solid var(--rule);cursor:pointer;box-shadow:var(--shadow)}
#loadmore:hover{border-color:var(--ink)}
#loadmore:focus-visible{outline:2px solid var(--boom);outline-offset:2px}
.empty{text-align:center;padding:56px 20px;color:var(--muted);font-family:var(--mono);font-size:12.5px}

footer{margin-top:70px;border-top:2px solid var(--ink);padding-top:20px;
  font-family:var(--mono);font-size:11px;line-height:1.75;color:var(--muted)}
footer b{color:var(--ink-soft);font-weight:500}
footer a{color:var(--boom)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>'''

BODY = r'''<div class="wrap">
<header>
  <div class="kicker"><span class="dot"></span> Raw corpus &middot; Loom teardown &middot; collected 19 Aug 2026</div>
  <h1>Loom Reviews,<br>Unfiltered</h1>
  <p class="sub">Every user comment behind <a href="./">the teardown</a> &mdash; 1,795 of them, from four sources, unedited. Search it, filter it, read what people actually wrote.</p>

  <div class="counts">
    <div class="cnt"><span class="n">660</span><span class="l">Google Play</span></div>
    <div class="cnt"><span class="n">620</span><span class="l">App Store</span></div>
    <div class="cnt"><span class="n">207</span><span class="l">Reddit</span></div>
    <div class="cnt"><span class="n">308</span><span class="l">Hacker News</span></div>
    <div class="cnt"><span class="n">1,795</span><span class="l">Total</span></div>
  </div>
</header>

<div class="controls">
  <div class="searchrow">
    <input id="q" type="search" placeholder="Search all 1,795 comments — try &ldquo;upload&rdquo;, &ldquo;5 minute&rdquo;, &ldquo;download&rdquo;, &ldquo;log in&rdquo;&hellip;" autocomplete="off" spellcheck="false">
    <select id="sort" aria-label="Sort order">
      <option value="up">Most upvoted</option>
      <option value="long">Longest</option>
      <option value="new">Newest</option>
      <option value="short">Shortest</option>
    </select>
  </div>
  <div class="chips" id="srcchips" role="group" aria-label="Filter by source"></div>
  <div class="chips" id="ratechips" role="group" aria-label="Filter by rating"></div>
  <div class="status">
    <span id="count"></span>
    <button class="clear" id="clear" type="button">Reset filters</button>
  </div>
</div>

<div id="list"></div>
<button id="loadmore" type="button" hidden>Load more</button>

<footer>
  <b>Sources:</b> Google Play <span>com.loom.android</span> &middot; Apple App Store id 1474480829, 20 storefronts &middot; Reddit, 40 subreddits &middot; Hacker News via Algolia<br>
  <b>Filtering:</b> Reddit and HN rows are limited to comments where Loom-the-product is genuinely the subject; link-only mentions removed. App-store rows are verbatim, deduplicated.<br>
  <b>Note:</b> written reviews skew negative on both app stores &mdash; people type when they are angry. Read this as the shape of complaints among complainers.<br>
  <b>Full report:</b> <a href="./">The Loom Complaint Ledger</a> &middot; <b>Data &amp; scripts:</b> <a href="https://github.com/matalon888/loom-boom-research">github.com/matalon888/loom-boom-research</a>
</footer>
</div>

<script id="data" type="application/json">__PAYLOAD__</script>
<script>
(function(){
  var DATA = JSON.parse(document.getElementById('data').textContent);
  var SRC_LABEL = {play:'Google Play', ios:'App Store', reddit:'Reddit', hn:'Hacker News'};
  var state = {q:'', src:'all', rate:'all', sort:'up', shown:0};
  var PAGE = 50;
  var list = document.getElementById('list');
  var loadmore = document.getElementById('loadmore');
  var countEl = document.getElementById('count');

  // ---- build filter chips with real counts
  function makeChips(host, defs, key){
    host.innerHTML = '';
    defs.forEach(function(d){
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'chipbtn';
      b.setAttribute('aria-pressed', state[key] === d.v ? 'true' : 'false');
      b.dataset.v = d.v;
      b.innerHTML = d.label + '<span class="k">' + d.n.toLocaleString() + '</span>';
      b.addEventListener('click', function(){
        state[key] = d.v; state.shown = 0;
        Array.prototype.forEach.call(host.children, function(c){
          c.setAttribute('aria-pressed', c.dataset.v === d.v ? 'true' : 'false');
        });
        render();
      });
      host.appendChild(b);
    });
  }
  function nSrc(v){ return v === 'all' ? DATA.length : DATA.filter(function(x){return x.s===v;}).length; }
  function nRate(v){
    if(v==='all') return DATA.length;
    if(v==='neg') return DATA.filter(function(x){return x.r && x.r<=2;}).length;
    if(v==='mid') return DATA.filter(function(x){return x.r===3;}).length;
    if(v==='pos') return DATA.filter(function(x){return x.r && x.r>=4;}).length;
    return DATA.filter(function(x){return !x.r;}).length;
  }
  makeChips(document.getElementById('srcchips'), [
    {v:'all', label:'All sources', n:nSrc('all')},
    {v:'play', label:'Google Play', n:nSrc('play')},
    {v:'ios', label:'App Store', n:nSrc('ios')},
    {v:'reddit', label:'Reddit', n:nSrc('reddit')},
    {v:'hn', label:'Hacker News', n:nSrc('hn')}
  ], 'src');
  makeChips(document.getElementById('ratechips'), [
    {v:'all', label:'Any rating', n:nRate('all')},
    {v:'neg', label:'1–2 star', n:nRate('neg')},
    {v:'mid', label:'3 star', n:nRate('mid')},
    {v:'pos', label:'4–5 star', n:nRate('pos')},
    {v:'na', label:'Unrated (forums)', n:nRate('na')}
  ], 'rate');

  // ---- filtering
  function filtered(){
    var q = state.q.toLowerCase().trim();
    var out = DATA.filter(function(x){
      if(state.src !== 'all' && x.s !== state.src) return false;
      if(state.rate === 'neg' && !(x.r && x.r <= 2)) return false;
      if(state.rate === 'mid' && x.r !== 3) return false;
      if(state.rate === 'pos' && !(x.r && x.r >= 4)) return false;
      if(state.rate === 'na' && x.r) return false;
      if(q && x.c.toLowerCase().indexOf(q) === -1 && (x.g||'').toLowerCase().indexOf(q) === -1) return false;
      return true;
    });
    if(state.sort === 'up')    out.sort(function(a,b){ return (b.u||0)-(a.u||0) || b.c.length-a.c.length; });
    if(state.sort === 'long')  out.sort(function(a,b){ return b.c.length-a.c.length; });
    if(state.sort === 'short') out.sort(function(a,b){ return a.c.length-b.c.length; });
    if(state.sort === 'new')   out.sort(function(a,b){ return (b.d||'').localeCompare(a.d||''); });
    return out;
  }

  function esc(s){ return s.replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

  function highlight(s, q){
    if(!q) return esc(s);
    var out = '', i = 0, low = s.toLowerCase(), lq = q.toLowerCase();
    while(true){
      var j = low.indexOf(lq, i);
      if(j === -1){ out += esc(s.slice(i)); break; }
      out += esc(s.slice(i, j)) + '<mark>' + esc(s.slice(j, j+q.length)) + '</mark>';
      i = j + q.length;
    }
    return out;
  }

  function starRow(r){
    if(!r) return '';
    var cls = r <= 2 ? '' : (r === 3 ? ' mid' : ' hi');
    return '<span class="stars'+cls+'">' + '★'.repeat(r) + '☆'.repeat(5-r) + '</span>';
  }

  function rowHTML(x, q){
    var band = !x.r ? 'none' : (x.r <= 2 ? 'neg' : (x.r === 3 ? 'mid' : 'pos'));
    var bits = [];
    bits.push('<span class="tag '+x.s+'">'+SRC_LABEL[x.s]+'</span>');
    if(x.r) bits.push(starRow(x.r));
    if(x.g) bits.push('<span class="small">'+(x.s==='reddit' ? 'r/'+esc(x.g) : esc(x.g).toUpperCase())+'</span>');
    if(x.d) bits.push('<span class="small">'+esc(x.d)+'</span>');
    if(x.u) bits.push('<span class="small">↑ '+x.u+'</span>');
    if(x.l) bits.push('<span class="small"><a href="'+esc(x.l)+'" target="_blank" rel="noopener">source ↗</a></span>');

    var long = x.c.length > 620;
    var body = long ? x.c.slice(0, 620) + '…' : x.c;
    return '<article class="row '+band+'">' +
             '<div class="meta">'+bits.join('')+'</div>' +
             '<div class="txt" data-full="'+esc(x.c)+'">'+highlight(body, q)+'</div>' +
             (long ? '<button class="more" type="button">Show full comment</button>' : '') +
           '</article>';
  }

  var current = [];
  function render(){
    current = filtered();
    state.shown = 0;
    list.innerHTML = '';
    if(!current.length){
      list.innerHTML = '<div class="empty">No comments match that. Try a shorter search term.</div>';
      loadmore.hidden = true;
      countEl.innerHTML = '<b>0</b> of ' + DATA.length.toLocaleString() + ' comments';
      return;
    }
    append();
  }

  function append(){
    var q = state.q.trim();
    var slice = current.slice(state.shown, state.shown + PAGE);
    var frag = document.createElement('div');
    frag.innerHTML = slice.map(function(x){ return rowHTML(x, q); }).join('');
    while(frag.firstChild) list.appendChild(frag.firstChild);
    state.shown += slice.length;
    loadmore.hidden = state.shown >= current.length;
    loadmore.textContent = 'Load ' + Math.min(PAGE, current.length - state.shown) + ' more';
    countEl.innerHTML = 'Showing <b>' + state.shown.toLocaleString() + '</b> of <b>' +
      current.length.toLocaleString() + '</b> matching · ' + DATA.length.toLocaleString() + ' collected';
  }

  loadmore.addEventListener('click', append);

  list.addEventListener('click', function(e){
    var btn = e.target.closest('.more');
    if(!btn) return;
    var txt = btn.previousElementSibling;
    txt.innerHTML = highlight(txt.dataset.full, state.q.trim());
    btn.remove();
  });

  var t;
  document.getElementById('q').addEventListener('input', function(e){
    clearTimeout(t);
    var v = e.target.value;
    t = setTimeout(function(){ state.q = v; render(); }, 160);
  });
  document.getElementById('sort').addEventListener('change', function(e){
    state.sort = e.target.value; render();
  });
  document.getElementById('clear').addEventListener('click', function(){
    state.q = ''; state.src = 'all'; state.rate = 'all'; state.sort = 'up';
    document.getElementById('q').value = '';
    document.getElementById('sort').value = 'up';
    Array.prototype.forEach.call(document.querySelectorAll('.chipbtn'), function(c){
      c.setAttribute('aria-pressed', c.dataset.v === 'all' ? 'true' : 'false');
    });
    render();
  });

  render();
})();
</script>'''

body = BODY.replace('__PAYLOAD__', payload)
os.makedirs('out', exist_ok=True)

# artifact version (no html/head/body wrapper)
open('out/comments.html', 'w', encoding='utf-8').write(HEAD + '\n' + body + '\n')

# standalone version for GitHub Pages
full = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="description" content="All 1,795 raw Loom user comments from the Google Play Store, Apple App Store, Reddit and Hacker News — searchable and filterable.">\n'
        + HEAD + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
open('/Users/danielmatalon/loom-boom-research/docs/comments.html', 'w', encoding='utf-8').write(full)
print('artifact KB', round(os.path.getsize('out/comments.html')/1024))
print('pages KB', round(os.path.getsize('/Users/danielmatalon/loom-boom-research/docs/comments.html')/1024))
