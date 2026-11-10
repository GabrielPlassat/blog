"""Réécrit, article par article, les liens et images de _posts/.

- lien vers un article du corpus (quelle que soit son ancienne adresse) -> /AAAA/MM/titre/ du nouveau blog
- image ou fichier présent dans assets/ -> adresse locale
- lien vers un ancien site fermé (Typepad, transportsdufutur.ademe.fr, lafabriquedesmobilites.fr)
  sans article correspondant -> copie web.archive.org
- tout le reste est laissé tel quel.
Écrit scripts/rapport-liens.csv (une ligne par lien modifié ; le fichier est remplacé à chaque passage).
Relançable : un lien déjà réécrit n'est plus touché.
"""
import csv, glob, os, re, unicodedata, html
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from urllib.parse import urlparse as _up, unquote


def urlparse(u):
    try:
        return _up(u)
    except ValueError:
        return _up('')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = '{{ site.baseurl }}'
DEAD = ('transportsdufutur.typepad.fr', 'transportsdufutur.ademe.fr', 'lafabriquedesmobilites.fr',
        'www.lafabriquedesmobilites.fr', 'static.typepad.com', 'www.typepad.com', 'typepad.com')
ARCHIVE = 'https://web.archive.org/web/2018/'


def norm(s):
    s = unicodedata.normalize('NFKD', unquote(html.unescape(s)).lower()).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', s)


def fm(text):
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    return m.group(1) if m else ''


def val(f, k):
    m = re.search(rf'^{k}:\s*"?(.*?)"?\s*$', f, re.M)
    return m.group(1) if m else ''


# ---------- index des articles ----------
posts = []
for f in sorted(glob.glob(f'{ROOT}/_posts/*.md')):
    t = open(f, encoding='utf-8').read(); h = fm(t)
    b = os.path.basename(f)[:-3]
    p = dict(file=f, y=b[:4], m=b[5:7], slug=b[11:], src=val(h, 'source'), title=val(h, 'title'),
             orig=val(h, 'original_url'))
    p['url'] = f'/{p["y"]}/{p["m"]}/{p["slug"]}/'
    p['keys'] = {norm(p['slug']), norm(p['title'])}
    if p['orig']:
        tail = urlparse(p['orig']).path.rstrip('/').split('/')[-1]
        p['keys'].add(norm(re.sub(r'\.html?$', '', tail)))
    redir = re.search(r'redirect_from:\s*\n\s*-\s*(\S+)', h)
    if redir:
        p['keys'].add(norm(redir.group(1).rstrip('/').split('/')[-1]))
    posts.append(p)
bykey = defaultdict(list)
for p in posts:
    for k in p['keys']:
        bykey[k].append(p)


def find(slug, y=None, m=None, srcs=None):
    """Retrouve l'article à partir d'un bout d'adresse (slug éventuellement tronqué)."""
    k = norm(re.sub(r'\.html?$', '', slug))
    if len(k) < 6:
        return None
    cands = [p for p in bykey.get(k, []) if not srcs or p['src'] in srcs]
    if not cands:  # slug tronqué (Typepad coupe vers 50 caractères) ou légèrement différent
        pool = [p for p in posts if (not srcs or p['src'] in srcs) and (not y or p['y'] == y)]
        best, score = None, 0
        for p in pool:
            for pk in [x for x in p['keys'] if len(x) >= 10]:
                if len(k) >= 15 and (pk.startswith(k[:40]) or k.startswith(pk[:40])):
                    s = 0.95
                else:
                    s = SequenceMatcher(None, k, pk).ratio()
                if m and p['m'] == m:
                    s += 0.03
                if s > score:
                    best, score = p, s
        return best if score >= 0.86 else None
    if y:
        same = [p for p in cands if p['y'] == y and (not m or p['m'] == m)] or [p for p in cands if p['y'] == y]
        if same:
            return same[0]
    return cands[0]


def resolve(u, self_src):
    """Retourne (nouvelle_url, type) ou (None, None) si on ne touche pas."""
    if u.startswith(BASE) or u.startswith('#') or u.startswith('mailto:'):
        return None, None
    pu = urlparse(u); host = pu.netloc.lower().replace('www.', ''); path = unquote(pu.path)
    # images et fichiers locaux
    if path.startswith('/assets/') and (not host or 'transportsdufutur' in host):
        if host and not os.path.exists(ROOT + unquote(path)):
            return ARCHIVE + u, 'archive'
        return BASE + path, 'image'
    if 'lafabriquedesmobilites.fr' in host and 'wp-content/uploads' in path:
        y = re.search(r'uploads/(20\d\d)/', path)
        loc = f'/assets/images/fabmob/{y.group(1)}/{os.path.basename(path)}' if y else ''
        if loc and os.path.exists(ROOT + loc):
            return BASE + loc, 'image'
    if 'wp-content/uploads' in path and (not host or 'transportsdufutur' in host):
        rest = re.sub(r'^.*?wp-content/uploads/(?:sites/\d+/)?', '', path)
        if os.path.exists(f'{ROOT}/assets/images/{rest}'):
            return f'{BASE}/assets/images/{rest}', 'image'
        return ARCHIVE + 'http://transportsdufutur.ademe.fr' + path, 'archive'
    # pages d'accueil des anciens sites
    if path in ('', '/'):
        if 'lafabriquedesmobilites.fr' == host:
            return 'https://fabmob.io', 'accueil'
        if host in ('transportsdufutur.typepad.fr', 'transportsdufutur.ademe.fr'):
            return BASE + '/', 'accueil'
    # articles
    m = re.search(r'/(20\d\d)/(\d\d)/(?:\d\d/)?([^/]+?)(?:\.html?)?/?$', path)
    p = None
    if host in ('transportsdufutur.typepad.fr', 'transportsdufutur.ademe.fr', 'gabrielplassat.github.io', '') and m:
        p = find(m.group(3), m.group(1), m.group(2), {'tdf'})
    elif host in ('lafabriquedesmobilites.fr', 'fabmob.io') and re.search(r'/(articles|blog|[a-z-]+)/', path):
        p = find(path.rstrip('/').split('/')[-1], srcs={'fabmob'})
    elif host == 'plassat.wordpress.com' and m:
        p = find(m.group(3), m.group(1), m.group(2), {'brico'})
    elif host == 'xd.ademe.fr' and '/blog/' in path:
        p = find(path.rstrip('/').split('/')[-1])
    elif host == 'linkedin.com' and '/pulse/' in path:
        tail = re.sub(r'-gabriel-plassat.*$', '', path.rstrip('/').split('/')[-1])
        p = find(tail)
    if p:
        return BASE + p['url'], 'interne'
    if host in DEAD or (not host and m and self_src == 'tdf'):
        full = u if host else 'http://transportsdufutur.ademe.fr' + u
        return ARCHIVE + full, 'archive'
    return None, None


LINK = re.compile(r'(\]\(\s*<?|(?:href|src)=["\'])([^"\'\s)<>]+)')
rows = []; stats = Counter(); per_file = Counter()
for p in posts:
    t = open(p['file'], encoding='utf-8').read()
    mo0 = re.match(r'---\n.*?\n---\n', t, re.S); head, body = t[:mo0.end()], t[mo0.end():]

    def sub(mo):
        u = mo.group(2)
        new, kind = resolve(u, p['src'])
        if new and new != u:
            stats[kind] += 1; per_file[os.path.basename(p['file'])] += 1
            rows.append([os.path.basename(p['file']), kind, u, new])
            return mo.group(1) + new
        return mo.group(0)

    nb = LINK.sub(sub, body)
    if nb != body:
        open(p['file'], 'w', encoding='utf-8').write(head + nb)

with open(f'{ROOT}/scripts/rapport-liens.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=';'); w.writerow(['article', 'type', 'ancien lien', 'nouveau lien']); w.writerows(rows)
print(dict(stats), 'articles modifiés :', len(per_file))
