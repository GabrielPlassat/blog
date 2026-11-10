"""Corrige les mises en gras cassées par un espace collé aux ** (« **texte ** » ou « ** texte** »).

Dans chaque paragraphe, les ** sont appariés dans l'ordre (ouvrant, fermant, ouvrant…).
L'espace placé juste après un ** ouvrant ou juste avant un ** fermant est déplacé à l'extérieur ;
un gras vide (« ** ** ») est supprimé. Les paragraphes qui ont un nombre impair de ** sont
laissés tels quels et signalés. Détail : scripts/rapport-gras.csv.
"""
import csv, glob, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WS = ' \t '
rows, stats = [], Counter()


def fix_par(par, name):
    parts = par.split('**')
    if len(parts) < 3:
        return par
    if len(parts) % 2 == 0:      # nombre impair de ** : on ne touche pas
        stats['paragraphe impair (signalé)'] += 1
        rows.append([name, 'nombre impair de ** (à vérifier)', par.strip()[:120]])
        return par
    out = [parts[0]]
    for i in range(1, len(parts), 2):
        inner, after = parts[i], parts[i + 1]
        if not inner.strip(WS + '\n'):          # gras vide
            if inner:
                stats['gras vide supprimé'] += 1
            out.append(' ' if inner else '')
            out.append(after)
            continue
        lead = inner[:len(inner) - len(inner.lstrip(WS))]
        trail = inner[len(inner.rstrip(WS)):]
        if lead or trail:
            stats['gras réparé'] += 1
            rows.append([name, 'gras réparé', ('**' + inner + '**').strip()[:100]])
        before = out[-1]
        if lead and before and not before[-1:].isspace():
            out[-1] = before + ' '
        out.append('**' + inner.strip(WS) + '**')
        out.append((' ' if trail and after and not after[:1].isspace() and after[:1] not in '.,;:!?)»' else '') + after)
    return ''.join(out)


for f in sorted(glob.glob(f'{ROOT}/_posts/*.md')):
    t = open(f, encoding='utf-8').read()
    m = re.match(r'---\n.*?\n---\n', t, re.S); head, body = t[:m.end()], t[m.end():]
    body = re.sub(r'^[ \t\u00a0]*\*{4,}[ \t\u00a0]*$', '', body, flags=re.M)   # lignes d'étoiles seules
    body = re.sub(r'\*{6,}', '', body)
    pars = re.split(r'(\n\s*\n)', body)
    new = ''.join(fix_par(p, os.path.basename(f)) if i % 2 == 0 else p for i, p in enumerate(pars))
    if new != body:
        stats['articles modifiés'] += 1
        open(f, 'w', encoding='utf-8').write(head + new)

with open(f'{ROOT}/scripts/rapport-gras.csv', 'w', encoding='utf-8', newline='') as fo:
    w = csv.writer(fo, delimiter=';'); w.writerow(['article', 'action', 'extrait']); w.writerows(rows)
print(dict(stats))
