"""Nettoie les articles importés de l'ancien export CSV de Transports du Futur.

1. Supprime la « traîne » de l'export (date, adresse, tags collés par des |, publish,
   identifiant, courriel…) restée à la fin de certains articles.
2. Rétablit les liens vidés lors de l'ancienne conversion ([texte]()) en retrouvant
   l'adresse dans le HTML d'origine (articles.csv du dépôt transportsdufutur).
3. Retire les images vides ([![]()]() et ![]()).
Écrit scripts/rapport-nettoyage.csv. À relancer ensuite : scripts/liens.py puis scripts/carte.py.
"""
import csv, glob, html, os, re, unicodedata
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TDF_CSV = '/home/claude/gabrielplassat/transportsdufutur/articles.csv'
TAIL = re.compile(r'\s*"?\s*\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\s*(?:https?://\S+?\.html|/\S+?\.html)[^\n]*(?:publish|draft|private)\d*\S*.*$', re.S)


def nn(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', html.unescape(s).lower()).encode('ascii', 'ignore').decode())


csv.field_size_limit(10 ** 9)
orig = {}
for r in list(csv.reader(open(TDF_CSV, encoding='utf-8-sig'), delimiter=';'))[1:]:
    if len(r) > 2 and len(r[2]) > len(orig.get(nn(r[1])[:60], '')):
        orig[nn(r[1])[:60]] = r[2]

rows, stats = [], Counter()
for f in sorted(glob.glob(f'{ROOT}/_posts/*.md')):
    t = open(f, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n', t, re.S); head, body = t[:m.end()], t[m.end():]
    if not re.search(r'^source: tdf$', m.group(1), re.M):
        continue
    new = body
    # 1. traîne de l'export
    tm = TAIL.search(new)
    if tm and ('gabrielplassat' in tm.group(0) or 'publish' in tm.group(0)):
        rows.append([os.path.basename(f), 'traîne supprimée', tm.group(0).strip()[:120]]); stats['traîne'] += 1
        new = new[:tm.start()].rstrip() + '\n'
    # 2. liens vides
    if re.search(r'\]\(\s*\)', new):
        title = (re.search(r'^title:\s*"?(.*?)"?\s*$', m.group(1), re.M) or [None, ''])[1]
        src = orig.get(nn(title.replace('\\"', '"'))[:60], '')
        anchors = [(nn(re.sub(r'<[^>]+>', '', a)), h) for h, a in
                   re.findall(r'<a\s[^>]*?href=["\']+([^"\']+)["\']+[^>]*>(.*?)</a>', src, re.S)]
        used = set()

        def fix(mo):
            txt = mo.group(1); k = nn(txt)
            for i, (ak, h) in enumerate(anchors):
                if i not in used and k and (ak == k or (len(k) > 3 and len(ak) > 3 and (k in ak or ak in k))):
                    used.add(i); stats['lien rétabli'] += 1
                    rows.append([os.path.basename(f), 'lien rétabli', f'{txt[:40]} -> {h[:80]}'])
                    return f'[{txt}]({h})'
            stats['lien vide retiré'] += 1
            rows.append([os.path.basename(f), 'lien vide retiré (texte gardé)', txt[:60]])
            return txt
        new = re.sub(r'\[!\[[^\]]*\]\(\s*\)\]\(\s*\)', '', new)          # 3. images vides
        new = re.sub(r'!\[[^\]]*\]\(\s*\)', '', new)
        new = re.sub(r'(?<!!)\[([^\[\]]*)\]\(\s*\)', fix, new)
    if new != body:
        open(f, 'w', encoding='utf-8').write(head + new)

with open(f'{ROOT}/scripts/rapport-nettoyage.csv', 'w', encoding='utf-8', newline='') as fo:
    w = csv.writer(fo, delimiter=';'); w.writerow(['article', 'action', 'détail']); w.writerows(rows)
print(dict(stats))
