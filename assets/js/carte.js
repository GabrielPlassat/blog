/* Carte du blog : ciel (constellation), terre (rhizome des tags), temps (chronologie),
   et voisins d'un article. Données : assets/data/carte.json (scripts/carte.py). */
const SRC = {tdf:['Transports du Futur','#2f6fd6'], fabmob:['Fabrique des Mobilités','#1f9d74'],
  brico:['Bricologie','#8b55cc'], xd:['Blog XD','#c7841a'], linkedin:['LinkedIn','#7d8899']};
const COL = ['#c7841a','#7d8899','#2f6fd6','#a8a08f','#8b55cc','#1f9d74','#d6455d','#33a4c4','#b8931a'];
const BASE = window.BASE || '';
let CARTE = null;
async function carte(){ if(!CARTE) CARTE = await (await fetch(BASE + '/assets/data/carte.json')).json(); return CARTE; }
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function tip(){ let t=document.getElementById('ctip'); if(!t){ t=document.createElement('div'); t.id='ctip'; t.className='ctip'; document.body.appendChild(t);} return t; }
function showTip(e, p, D){ const t=tip(); t.innerHTML=`<small>${SRC[p.s][0]} · ${p.d} · ${esc(D.themes[p.f].n)}</small><br>${esc(p.t)}`; t.style.display='block'; t.style.left=Math.min(e.clientX+14, innerWidth-300)+'px'; t.style.top=(e.clientY+14)+'px'; }
function hideTip(){ tip().style.display='none'; }
const go = p => { location.href = BASE + p.u; };
function legend(el, D, mode){
  el.innerHTML = mode==='s'
    ? Object.keys(SRC).map(s=>`<span class="chip"><i style="background:${SRC[s][1]}"></i>${SRC[s][0]} · ${D.posts.filter(p=>p.s===s).length}</span>`).join('')
    : D.themes.map((t,k)=>`<span class="chip" title="${esc(t.mots.join(', '))}"><i style="background:${COL[k]}"></i>${esc(t.n)}</span>`).join('');
}

/* ---------- Ciel ---------- */
async function ciel(sel){
  const D = await carte(), P = D.posts, box = document.querySelector(sel);
  box.innerHTML = `<div class="ctl"><label>De <input type="range" id="c0" min="2009" max="2026" value="2009"> <b id="c0o">2009</b></label>
    <label>à <input type="range" id="c1" min="2009" max="2026" value="2026"> <b id="c1o">2026</b></label>
    <label>Couleur <select id="cm"><option value="f">thèmes</option><option value="s">blogs</option></select></label>
    <label><input type="checkbox" id="cl" checked> liens écrits</label></div>
    <div class="legend" id="cleg"></div><svg viewBox="0 0 1000 640" class="cv"></svg>
    <p class="note">Chaque point est un article ; les articles au vocabulaire proche sont voisins. Survolez pour lire le titre, cliquez pour ouvrir l'article. Molette pour zoomer.</p>`;
  const svg = d3.select(box).select('svg'), g = svg.append('g');
  const X = d=>30+d.x*940, Y = d=>20+d.y*600, R = d=>2.2+Math.sqrt(d.w||300)/18;
  const L = []; P.forEach(p=>p.out.forEach(j=>L.push([p.i,j])));
  const lines = g.append('g').selectAll('line').data(L).join('line').attr('class','clink')
    .attr('x1',d=>X(P[d[0]])).attr('y1',d=>Y(P[d[0]])).attr('x2',d=>X(P[d[1]])).attr('y2',d=>Y(P[d[1]]));
  const halo = g.append('g');
  const dots = g.append('g').selectAll('circle').data(P).join('circle').attr('cx',X).attr('cy',Y).attr('r',R)
    .attr('fill',d=>COL[d.f]).attr('opacity',.85).style('cursor','pointer')
    .on('mouseenter',(e,d)=>{ showTip(e,d,D); halo.selectAll('*').remove();
      d.nb.forEach(([j])=>halo.append('line').attr('class','chalo').attr('x1',X(d)).attr('y1',Y(d)).attr('x2',X(P[j])).attr('y2',Y(P[j]))); })
    .on('mouseleave',()=>{ hideTip(); halo.selectAll('*').remove(); }).on('click',(e,d)=>go(d));
  svg.call(d3.zoom().scaleExtent([1,8]).on('zoom',e=>g.attr('transform',e.transform)));
  const yr=[2009,2026];
  function upd(){ const m=box.querySelector('#cm').value;
    dots.attr('fill',d=>m==='s'?SRC[d.s][1]:COL[d.f]).attr('display',d=>{const y=+d.d.slice(0,4); return y>=yr[0]&&y<=yr[1]?null:'none';});
    lines.attr('display',d=>{ if(!box.querySelector('#cl').checked) return 'none'; const a=+P[d[0]].d.slice(0,4), b=+P[d[1]].d.slice(0,4); return a>=yr[0]&&a<=yr[1]&&b>=yr[0]&&b<=yr[1]?null:'none'; });
    legend(box.querySelector('#cleg'), D, m); }
  ['c0','c1'].forEach((id,k)=>box.querySelector('#'+id).oninput=e=>{ yr[k]=+e.target.value; if(yr[0]>yr[1]) yr[1-k]=yr[k];
    box.querySelector('#c0').value=yr[0]; box.querySelector('#c1').value=yr[1]; box.querySelector('#c0o').textContent=yr[0]; box.querySelector('#c1o').textContent=yr[1]; upd(); });
  box.querySelector('#cm').onchange=upd; box.querySelector('#cl').onchange=upd; upd();
}

/* ---------- Terre (rhizome des tags) ---------- */
async function terre(sel){
  const D = await carte(), P = D.posts, box = document.querySelector(sel);
  box.innerHTML = `<div class="legend" id="tleg"></div><svg viewBox="0 0 1000 640" class="cv"></svg>
    <p class="note">Les tags les plus utilisés, reliés quand ils apparaissent ensemble dans plusieurs articles. Cliquez un tag pour voir ses articles.</p><div id="tlist" class="tlist"></div>`;
  legend(box.querySelector('#tleg'), D, 'f');
  const nodes = D.tags.nodes.map(d=>({...d})), links = D.tags.links.filter(l=>l.c>=18).map(l=>({source:l.a,target:l.b,c:l.c}));
  const svg = d3.select(box).select('svg'), g = svg.append('g'), r = d=>3+Math.sqrt(d.c)*1.2;
  const ln = g.append('g').selectAll('line').data(links).join('line').attr('class','clink').attr('stroke-width',d=>Math.min(4,d.c/12));
  const nd = g.append('g').selectAll('g').data(nodes).join('g').style('cursor','pointer').on('click',(e,d)=>pick(d.id));
  nd.append('circle').attr('r',r).attr('fill',d=>COL[d.f]).attr('opacity',.85);
  nd.append('text').attr('dy',d=>-r(d)-3).attr('text-anchor','middle').attr('class','tlab').text(d=>d.id);
  d3.forceSimulation(nodes).force('link',d3.forceLink(links).id(d=>d.id).distance(90).strength(.15))
    .force('charge',d3.forceManyBody().strength(-520)).force('center',d3.forceCenter(500,320))
    .force('collide',d3.forceCollide(d=>r(d)+22)).force('x',d3.forceX(500).strength(.04)).force('y',d3.forceY(320).strength(.06))
    .on('tick',()=>{ nodes.forEach(d=>{d.x=Math.max(20,Math.min(980,d.x)); d.y=Math.max(20,Math.min(625,d.y));});
      ln.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y); nd.attr('transform',d=>`translate(${d.x},${d.y})`); });
  svg.call(d3.zoom().scaleExtent([.6,5]).on('zoom',e=>g.attr('transform',e.transform)));
  function pick(t){ const nb=new Set([t]); links.forEach(l=>{ if(l.source.id===t||l.target.id===t){nb.add(l.source.id);nb.add(l.target.id);} });
    nd.attr('opacity',d=>nb.has(d.id)?1:.15); const list=P.filter(p=>p.tags.includes(t)).sort((a,b)=>a.d<b.d?1:-1);
    box.querySelector('#tlist').innerHTML=`<h3>${esc(t)} · ${list.length} articles</h3><ul class="plist">${list.map(li).join('')}</ul>`; }
}
const li = p => `<li><i style="background:${SRC[p.s][1]}" title="${SRC[p.s][0]}"></i><span class="pd">${p.d.slice(0,7)}</span><a href="${BASE}${p.u}">${esc(p.t)}</a></li>`;

/* ---------- Temps (chronologie) ---------- */
async function temps(sel){
  const D = await carte(), P = D.posts, box = document.querySelector(sel);
  box.innerHTML = `<div class="ctl"><label>Couleur <select id="tm"><option value="f">thèmes</option><option value="s">blogs</option></select></label></div>
    <div class="legend" id="mleg"></div><svg class="cv"></svg><p class="note">Un carré par article, dans l'ordre de publication, une ligne par année.</p>`;
  const svg = d3.select(box).select('svg'), s=8, gap=2, per=100, left=70; let yy=8; const pos=[];
  for(let y=2009;y<=2026;y++){ const list=P.filter(p=>+p.d.slice(0,4)===y).sort((a,b)=>a.d<b.d?-1:1), rows=Math.max(1,Math.ceil(list.length/per));
    svg.append('text').attr('x',0).attr('y',yy+s).attr('class','tlab').text(y);
    svg.append('text').attr('x',left-8).attr('y',yy+s).attr('text-anchor','end').attr('class','tlab muted').text(list.length||'');
    list.forEach((p,i)=>pos.push({p,x:left+(i%per)*(s+gap),y:yy+Math.floor(i/per)*(s+gap)})); yy+=rows*(s+gap)+8; }
  svg.attr('viewBox',`0 0 1080 ${yy}`);
  const sq = svg.append('g').selectAll('rect').data(pos).join('rect').attr('x',d=>d.x).attr('y',d=>d.y).attr('width',s).attr('height',s).attr('rx',1.5)
    .style('cursor','pointer').on('mousemove',(e,d)=>showTip(e,d.p,D)).on('mouseleave',hideTip).on('click',(e,d)=>go(d.p));
  const upd=()=>{ const m=box.querySelector('#tm').value; sq.attr('fill',d=>m==='s'?SRC[d.p.s][1]:COL[d.p.f]); legend(box.querySelector('#mleg'),D,m); };
  box.querySelector('#tm').onchange=upd; upd();
}

/* ---------- Voisins d'un article ---------- */
async function voisins(sel, url){
  const D = await carte(), P = D.posts, p = P.find(q=>q.u===url), box=document.querySelector(sel); if(!p||!box) return;
  const blk=(h,ids)=>ids.length?`<h3>${h}</h3><ul class="plist">${ids.map(j=>li(P[j])).join('')}</ul>`:'';
  box.innerHTML = blk('Voisins par le texte', p.nb.map(x=>x[0])) + blk('Cet article cite', p.out) + blk(`Cité par (${p.inn.length})`, p.inn.slice(0,12));
}

/* Styles minimaux des vues, au cas où la feuille de style du thème ne serait pas chargée */
(function(){ if(document.getElementById('carte-css')) return; const s=document.createElement('style'); s.id='carte-css'; s.textContent=`
.vue .ctl{display:flex;flex-wrap:wrap;gap:14px;align-items:center;font-size:.9em;margin-bottom:8px}
.legend{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 10px}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:.78em;padding:3px 9px;border:1px solid #dee2e6;border-radius:14px;background:#fff}
.chip i{width:9px;height:9px;border-radius:50%;display:inline-block}
.cv{width:100%;height:auto;background:#fbfaf7;border:1px solid #dee2e6;border-radius:8px}
.clink{stroke:#b9b5ab;stroke-opacity:.35}.chalo{stroke:#d6455d;stroke-width:1.4}
.tlab{font-size:10px;fill:#444;pointer-events:none}.tlab.muted{fill:#999}
.note{font-size:.85em;color:#6c757d}
.ctip{position:fixed;display:none;max-width:280px;background:#222;color:#fff;padding:7px 10px;border-radius:6px;font-size:13px;line-height:1.35;pointer-events:none;z-index:99}
.ctip small{color:#bbb}
.plist{list-style:none;margin:0;padding:0}
.plist li{display:flex;gap:10px;align-items:baseline;padding:6px 0;border-bottom:1px solid #dee2e6;font-size:.92em}
.plist li i{flex:none;width:9px;height:9px;border-radius:50%;display:inline-block}
.pd{flex:none;color:#6c757d;font-family:ui-monospace,monospace;font-size:.85em;min-width:4.5em}`; document.head.appendChild(s); })();
