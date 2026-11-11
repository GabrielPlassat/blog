/**
 * Recherche plein texte côté client (titre, tags, début du texte).
 * Insensible aux accents et aux majuscules ; les titres qui contiennent les mots passent en premier.
 */
(function() {
  'use strict';
  const input = document.getElementById('search-input');
  const box = document.getElementById('search-results');
  if (!input || !box) return;
  const BASE = window.BASE || '';
  let index = null, timer;
  const norm = s => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const esc = s => String(s || '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const load = () => index || (index = fetch(BASE + '/search.json').then(r => r.json()).then(d => d.map(p => ({
    ...p, nt: norm(p.title), nx: norm(p.title + ' ' + (p.tags || []).join(' ') + ' ' + p.content)
  }))));
  input.addEventListener('focus', load);
  input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(run, 250); });

  async function run() {
    const q = input.value.trim();
    if (q.length < 2) { box.innerHTML = ''; box.style.display = 'none'; return; }
    const words = norm(q).split(/\s+/).filter(w => w.length > 1);
    const all = await load();
    const hits = all.filter(p => words.every(w => p.nx.includes(w)))
      .map(p => ({ p, s: words.filter(w => p.nt.includes(w)).length }))
      .sort((a, b) => b.s - a.s || (a.p.date < b.p.date ? 1 : -1));
    box.style.display = 'block';
    if (!hits.length) { box.innerHTML = `<div class="search-no-results"><p>Aucun résultat pour « <strong>${esc(q)}</strong> »</p></div>`; return; }
    box.innerHTML = `<div class="search-results-header"><p>${hits.length} article${hits.length > 1 ? 's' : ''}${hits.length > 30 ? ' — les 30 premiers' : ''}</p></div>
      <div class="search-results-list">${hits.slice(0, 30).map(({ p }) => `
        <article class="search-result"><h3><a href="${p.url}">${mark(p.title, words)}</a></h3>
        <time>${new Date(p.date).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })}</time>
        <p class="excerpt">${mark(p.excerpt, words)}</p></article>`).join('')}</div>`;
  }
  // surligne les mots trouvés, accents compris (« metanote » surligne « MétaNote »)
  function mark(text, words) {
    const t = String(text || ''), n = norm(t); let out = '', i = 0;
    const spans = [];
    words.forEach(w => { let k = n.indexOf(w); while (k >= 0) { spans.push([k, k + w.length]); k = n.indexOf(w, k + w.length); } });
    spans.sort((a, b) => a[0] - b[0]).forEach(([a, b]) => { if (a < i) return; out += esc(t.slice(i, a)) + '<mark>' + esc(t.slice(a, b)) + '</mark>'; i = b; });
    return out + esc(t.slice(i));
  }
  document.addEventListener('click', e => { if (!input.contains(e.target) && !box.contains(e.target)) box.style.display = 'none'; });
  input.addEventListener('focus', () => { if (box.innerHTML) box.style.display = 'block'; });
})();
