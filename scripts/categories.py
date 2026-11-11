"""Marque les MétaNotes et les Fictions (ligne `categorie:` du front matter).

MétaNotes : titres contenant « MétaNote » (sauf les articles qui en parlent sans en être une).
Fictions : les fictions numérotées, dont les quatre premières dont le titre ne porte pas
le mot (retrouvées grâce à l'article « Et si la fiction facilitait le passage à l'action ? »).
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAS_METANOTE = {'2013-09-16-partenariat-renault-bollore-incarne-la-mutation'}
FICTIONS_SANS_LE_MOT = {  # numéro : début du nom de fichier
    '1': '2011-07-04-google-mobility-service-et-si-nous-le-faisions-sans-attendre',
    '2': '2011-08-08-lavenir-de-lenergie-dans-les-transports-amazon-energy-service',
    '3': '2013-08-22-les-technologies-de-surveillance',
    '4': '2013-04-26-en-supprimant-quasiment-la-matiere',
}
n = {'metanote': 0, 'fiction': 0}
for f in sorted(glob.glob(f'{ROOT}/_posts/*.md')):
    t = open(f, encoding='utf-8').read(); b = os.path.basename(f)[:-3]
    m = re.match(r'---\n(.*?)\n---\n', t, re.S); fm = m.group(1)
    title = (re.search(r'^title:\s*(.*)$', fm, re.M) or [None, ''])[1]
    cat = None
    if re.search(r'm[ée]ta ?note', title, re.I) and not any(b.startswith(x) for x in PAS_METANOTE):
        cat = 'metanote'
    elif re.search(r'fiction\s*n°\s*\d+', title, re.I) or 'pure fiction' in title.lower() \
            or any(b.startswith(x) for x in FICTIONS_SANS_LE_MOT.values()):
        cat = 'fiction'
    fm2 = re.sub(r'\ncategorie:.*', '', fm)
    if cat:
        fm2 += f'\ncategorie: {cat}'; n[cat] += 1
    if fm2 != fm:
        open(f, 'w', encoding='utf-8').write('---\n' + fm2 + '\n---\n' + t[m.end():])
print(n)
