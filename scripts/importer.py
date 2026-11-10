"""Import unique des cinq blogs dans _posts/ avec un front matter homogène.

Sources (à cloner / extraire à côté, chemins en tête de fichier) :
- Transports du Futur : _posts actuels du dépôt (conflits de fusion résolus côté HEAD)
  + articles.csv du dépôt transportsdufutur pour les corps vides
- FabMob : dépôt fabmob/fabmob.io (contenu/articles), filtré sur la liste lue (lu.tsv)
- Bricologie : export WordPress converti en markdown + images
- XD et LinkedIn : textes copiés depuis le projet Claude « blog »

Chaque article reçoit : title, date, source, source_name, original_url, tags,
et redirect_from (ancienne adresse de ce blog) quand elle existe.
Adresse finale : /AAAA/MM/titre/ (voir permalink dans _config.yml).
"""
import csv, glob, html, json, os, re, shutil, sys, unicodedata
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = '/home/claude/ext'
TDF_POSTS = f'{EXT}/blog/_posts'   # copie des _posts d'origine (avant refonte)
TDF_CSV = '/home/claude/gabrielplassat/transportsdufutur/articles.csv'
FABMOB = f'{EXT}/fabmob.io/contenu/articles'
BRICO = '/home/claude/src/brico/articles'
BRICO_IMG = f'{EXT}/brico_img/images'
XD_DIR, LI_DIR = f'{EXT}/xd', f'{EXT}/li'
LU = '/home/claude/work/livre/lu.tsv'

SRC = {'tdf': 'Transports du Futur', 'fabmob': 'Fabrique des Mobilités', 'brico': 'Bricologie & Sérendipité',
       'xd': 'Blog XD (ADEME)', 'linkedin': 'LinkedIn'}


def slugify(s, n=80):
    s = unicodedata.normalize('NFKD', html.unescape(s).lower()).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:n].rstrip('-')


def resolve(s):
    return re.sub(r'<<<<<<< HEAD\n(.*?)=======\n.*?>>>>>>> [0-9a-f]+\n?', r'\1', s, flags=re.S)


def split_fm(s):
    m = re.match(r'﻿?---\n(.*?)\n---\n?(.*)', s, re.S)
    return (m.group(1), m.group(2)) if m else ('', s)


def fmval(fm, k):
    m = re.search(rf'^{k}:\s*(.*)$', fm, re.M)
    if not m:
        return ''
    v = m.group(1).strip()
    if len(v) > 1 and v[0] == v[-1] and v[0] in '"\'':
        v = v[1:-1]
    return v.replace('\\"', '"').replace("''", "'")


def listval(fm, k):
    m = re.search(rf'^{k}:\s*\[(.*?)\]\s*$', fm, re.M)
    if m:
        try:
            return [x for x in json.loads('[' + re.sub(r"'([^']*)'", lambda z: json.dumps(z.group(1)), m.group(1)) + ']') if x]
        except Exception:
            return [x.strip().strip('"\'') for x in m.group(1).split(',') if x.strip().strip('"\'')]
    m = re.search(rf'^{k}:\s*\n((?:[ \t]+-.*\n?)*)', fm + '\n', re.M)
    return [x.strip(' \t-"\'') for x in m.group(1).splitlines() if x.strip(' \t-"\'')] if m else []


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


posts = []

# ---------- Transports du Futur ----------
csv.field_size_limit(10 ** 9)
def nn(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', html.unescape(s).lower()).encode('ascii', 'ignore').decode())[:60]
csvbody = {}
for r in list(csv.reader(open(TDF_CSV, encoding='utf-8-sig'), delimiter=';'))[1:]:
    if len(r) > 5 and len(r[2]) > len(csvbody.get(nn(r[1]), ('',))[0]):
        csvbody[nn(r[1])] = (r[2], r[5])
seen = {}
for f in sorted(glob.glob(f'{TDF_POSTS}/*.md')):
    s = resolve(open(f, encoding='utf-8', errors='ignore').read().replace('_x000D_', ''))
    fm, body = split_fm(s)
    t = fmval(fm, 'title'); base = os.path.basename(f)
    d = fmval(fm, 'date') or base[:10]
    slug = base[11:-3]
    words = len(re.sub(r'<[^>]+>|\[|\]\([^)]*\)', ' ', body).split())
    c = csvbody.get(nn(t))
    orig = ''
    if c:
        orig = c[1]
        if words < 30 and len(re.sub(r'<[^>]+>', ' ', c[0]).split()) > 40:
            body = c[0]
    p = dict(src='tdf', title=t, date=d, slug=slug, tags=listval(fm, 'tags'), body=body.strip() + '\n',
             original_url=('http://transportsdufutur.ademe.fr' + orig) if orig.startswith('/') else orig,
             redirect=f'/{base[:4]}/{base[5:7]}/{base[8:10]}/{slug}/', file=f)
    k = nn(t)
    if k in seen:   # doublon : on garde le plus long
        if len(p['body']) > len(seen[k]['body']):
            posts.remove(seen[k]); posts.append(p); seen[k] = p
        continue
    seen[k] = p; posts.append(p)

# ---------- liste lue (FabMob, XD, LinkedIn) ----------
lu = [l.rstrip('\n').split('\t') for l in open(LU, encoding='utf-8')][1:]

# ---------- FabMob ----------
for src, slug, date, *_ in lu:
    if src != 'fabmob':
        continue
    y, name = slug.split('_', 1)
    cand = glob.glob(f'{FABMOB}/{y}/{name}.md') or glob.glob(f'{FABMOB}/{y}/*.md')
    cand = [c for c in cand if os.path.basename(c)[:-3] == name] or \
           [c for c in glob.glob(f'{FABMOB}/{y}/*.md') if slugify(os.path.basename(c)[:-3]) == slugify(name)]
    if not cand:
        print('FabMob introuvable', slug); continue
    fm, body = split_fm(open(cand[0], encoding='utf-8').read())
    tags = [re.sub(r'-(fr|en)$', '', t).replace('-', ' ') for t in listval(fm, 'tags')]
    tags = [t for t in tags if t not in ('parole_adherent',)]
    # images relatives -> assets/images/fabmob/AAAA/
    for im in set(re.findall(r'\]\((images/[^)\s]+)', body)):
        srcf = f'{FABMOB}/{y}/{im}'
        if os.path.exists(srcf):
            dst = f'{ROOT}/assets/images/fabmob/{y}/{os.path.basename(im)}'
            os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(srcf, dst)
        body = body.replace('](' + im, '](/assets/images/fabmob/' + y + '/' + os.path.basename(im))
    posts.append(dict(src='fabmob', title=fmval(fm, 'title') or name, date=(fmval(fm, 'date') or date)[:10],
                      slug=slugify(name), tags=tags, body=body.strip() + '\n',
                      original_url='https://fabmob.io/blog/' + name))

# ---------- Bricologie ----------
for f in sorted(glob.glob(f'{BRICO}/*.md')):
    fm, body = split_fm(open(f, encoding='utf-8').read())
    body = re.sub(r'^# .*\n+', '', body.strip())
    def img(m):
        y, mo, name = m.group(1), m.group(2), m.group(3)
        loc = f'{BRICO_IMG}/{y}/{mo}/{name}'
        if os.path.exists(loc):
            dst = f'{ROOT}/assets/images/brico/{y}/{mo}/{name}'
            os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(loc, dst)
            return f'/assets/images/brico/{y}/{mo}/{name}'
        return m.group(0)
    body = re.sub(r'https?://plassat\.(?:wordpress\.com|files\.wordpress\.com)/(?:wp-content/uploads/)?(\d{4})/(\d\d)/([^?\s)"]+)(?:\?[^)\s"]*)?', img, body)
    posts.append(dict(src='brico', title=fmval(fm, 'title'), date=fmval(fm, 'date')[:10], slug=os.path.basename(f)[11:-3],
                      tags=listval(fm, 'tags'), body=body + '\n', original_url=fmval(fm, 'url')))

# ---------- XD et LinkedIn ----------
# Articles LinkedIn qui republient un billet de Transports du Futur : pas de doublon,
# on signale la republication sur le billet d'origine.
LI_DUP = {"2017 Le programme Apollo par Baidu": "lindustrie-automobile-europeenne",
          "2016 MétaNote N°24, l'avenir du voyage": "metanote-lavenir-voyage",
          "2016 metanote 14 futur de l'auto": "lavenir-de-lautomobile",
          "2016 constructeurs vos plateformes brulent": "constructeurs-vos-plateformes-brulent"}
for src, slug, date, *_ in lu:
    if src not in ('xd', 'linkedin'):
        continue
    if src == 'linkedin' and slug in LI_DUP:
        for p in posts:
            if p['src'] == 'tdf' and p['slug'] == LI_DUP[slug]:
                p['also'] = 'LinkedIn'
        continue
    d = XD_DIR if src == 'xd' else LI_DIR
    fs = glob.glob(f'{d}/{slugify(slug)}.md')
    if not fs:
        print('texte manquant', src, slug); continue
    fm, body = split_fm(open(fs[0], encoding='utf-8').read())
    title = fmval(fm, 'title')
    if not title:
        m = re.search(r'^#\s+(.+)$', body, re.M)
        title = re.sub(r'[*_]', '', m.group(1)).strip() if m else slug
        body = body[m.end():] if m else body
    body = re.sub(r'^\s*·\s.*$', '', body, flags=re.M)
    tags = listval(fm, 'tags')
    if not tags and fmval(fm, 'tags'):
        tags = [x.strip() for x in fmval(fm, 'tags').split(',') if x.strip()]
    posts.append(dict(src=src, title=title, date=date, slug=slugify(slug if src == 'xd' else title),
                      tags=tags, body=body.strip() + '\n',
                      original_url=fmval(fm, 'source') or fmval(fm, 'original_url')))

# ---------- écriture ----------
out = f'{ROOT}/_posts'
for f in glob.glob(f'{out}/*.md'):
    os.remove(f)
used = Counter()
for p in sorted(posts, key=lambda p: p['date']):
    key = (p['date'][:7], p['slug'])
    used[key] += 1
    if used[key] > 1:
        p['slug'] += f'-{used[key]}'
    lines = ['---', 'layout: post', f'title: {yaml_str(p["title"])}', f'date: {p["date"][:10]}',
             f'source: {p["src"]}', f'source_name: {yaml_str(SRC[p["src"]])}']
    if p.get('original_url'):
        lines.append(f'original_url: {yaml_str(p["original_url"])}')
    lines.append('tags: ' + json.dumps([t for t in p['tags'] if t], ensure_ascii=False))
    if p.get('also'):
        lines.append(f'aussi_sur: {yaml_str(p["also"])}')
    if p.get('redirect'):
        lines += ['redirect_from:', f'  - {p["redirect"]}']
    lines.append('---')
    open(f'{out}/{p["date"][:10]}-{p["slug"]}.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n\n' + p['body'])
print(Counter(p['src'] for p in posts), len(posts))
