"""Calcule la carte du blog : thèmes, voisins, ciel, liens, rhizome des tags.

Lit _posts/, écrit assets/data/carte.json et ajoute (ou met à jour) la ligne
`theme:` dans le front matter de chaque article.
À relancer après chaque ajout d'articles (Colab : pip install scikit-learn).
"""
import glob, html, json, os, re
from collections import Counter
import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES = [  # nom, mots d'ancrage pour reconnaître la composante
    ("Énergie, émissions & consommateurs", "émissions carburant consommation énergie énergétique co2 prix"),
    ("Regards en anglais", "the and for that with are will this"),
    ("Données & services numériques", "données data internet connectivité partage assistant"),
    ("Veille & documents", "documents presentations view programme recherche"),
    ("Intelligence collective & innovation", "intelligence collective holoptisme collectif complexe"),
    ("Véhicule sobre & fonctionnalité", "fonctionnalité efficacité économie circulaire véhicule intermédiaires"),
    ("Stratégies numériques", "google uber numérique guerre plateforme tesla"),
    ("Déplacements, vélo & santé", "vélo covoiturage déplacements transport ville santé"),
    ("Communs, écosystèmes & open source", "communs fabrique open source ressources écosystème"),
]
STOP = set("""au aux avec ce ces dans de des du elle en et eux il je la le les leur lui ma mais me même mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses son sur ta te tes toi ton tu un une vos votre vous c d j l à m n s t y été être avoir ont est sont plus aussi comme cette tout tous toutes très bien faire fait peut sans entre deux leurs dont où ainsi alors donc encore car si non ils elles cet celui ceux sera seront peuvent doit avant après depuis lors chaque autre autres quand déjà ici là nbsp http https www com fr html amp strong p br div span style text align justify target blank rel noopener href src img alt class title width height iframe youtube embed frameborder allowfullscreen nan également notamment selon vers ans an aujourd hui fois mieux toute ça sous point part plusieurs exemple article lire voir jusqu site baseurl assets images jpg png""".split())

posts = []
for f in sorted(glob.glob(f'{ROOT}/_posts/*.md')):
    t = open(f, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n', t, re.S); fm, body = m.group(1), t[m.end():]
    g = lambda k: (re.search(rf'^{k}:\s*"?(.*?)"?\s*$', fm, re.M) or [None, ''])[1]
    tags = json.loads(re.search(r'^tags:\s*(\[.*\])\s*$', fm, re.M).group(1)) if re.search(r'^tags:\s*\[', fm, re.M) else []
    b = os.path.basename(f)[:-3]
    txt = html.unescape(re.sub(r'<[^>]+>|\{\{.*?\}\}|\{%.*?%\}', ' ', body))
    txt = re.sub(r'!\[[^\]]*\]\([^)]*\)|\]\([^)]*\)|https?://\S+', ' ', txt)
    txt = re.sub(r'\s+', ' ', re.sub(r'[\[\]#*_>|]', ' ', txt)).strip()
    posts.append(dict(file=f, fm=fm, body=body, t=json.loads('"' + g('title').replace('\\"', '"').replace('"', '\\"') + '"') if g('title') else b,
                      d=b[:10], u=f'/{b[:4]}/{b[5:7]}/{b[11:]}/', s=g('source'), tags=tags, txt=txt, w=len(txt.split()),
                      links=set(re.findall(r'\{\{ site\.baseurl \}\}(/\d{4}/\d\d/[^/"\s)]+/)', body))))
print(len(posts), 'articles')

corpus = [p['t'] + ' ' + p['t'] + ' ' + ' '.join(p['tags']) * 2 + ' ' + p['txt'] for p in posts]
vec = TfidfVectorizer(stop_words=list(STOP), max_df=0.5, min_df=3, sublinear_tf=True,
                      token_pattern=r"(?u)\b[a-zA-Zàâäéèêëîïôöùûüçœ0-9]{3,}\b")
X = vec.fit_transform(corpus); terms = vec.get_feature_names_out(); ti = {w: i for i, w in enumerate(terms)}
nmf = NMF(n_components=len(THEMES), random_state=1, init='nndsvda', max_iter=800)
W = nmf.fit_transform(X); C = nmf.components_
score = np.array([[sum(C[k, ti[w]] for w in anc.split() if w in ti) for k in range(len(THEMES))] for _, anc in THEMES])
r, c = linear_sum_assignment(-score)            # thème j <- composante c[j]
W = W[:, c]; C = C[c]
fam = W.argmax(1)
for j, (n, _) in enumerate(THEMES):
    print(n, '|', ', '.join(terms[np.argsort(-C[j])[:8]]), '|', int((fam == j).sum()))

S = cosine_similarity(X); np.fill_diagonal(S, 0)
emb = TSNE(n_components=2, metric='cosine', perplexity=30, random_state=3, init='random').fit_transform(X.toarray())
lo, hi = np.percentile(emb, 1, 0), np.percentile(emb, 99, 0); emb = np.clip((emb - lo) / (hi - lo), 0, 1)
byu = {p['u']: i for i, p in enumerate(posts)}
out = [[byu[l] for l in p['links'] if l in byu and byu[l] != i] for i, p in enumerate(posts)]
inn = [[] for _ in posts]
for i, o in enumerate(out):
    for j in o:
        inn[j].append(i)

tc = Counter(t for p in posts for t in p['tags']); top = [t for t, _ in tc.most_common(80)]
co = Counter()
for p in posts:
    ts = sorted(set(t for t in p['tags'] if t in top))
    for a in range(len(ts)):
        for b in range(a + 1, len(ts)):
            co[(ts[a], ts[b])] += 1
Wn = W / (W.sum(1, keepdims=True) + 1e-9)
tagfam = {t: int(Wn[[i for i, p in enumerate(posts) if t in p['tags']]].sum(0).argmax()) for t in top}

data = dict(
    themes=[dict(n=n, mots=list(terms[np.argsort(-C[j])[:8]])) for j, (n, _) in enumerate(THEMES)],
    posts=[dict(i=i, t=p['t'], d=p['d'], u=p['u'], s=p['s'], f=int(fam[i]), w=p['w'],
                x=round(float(emb[i, 0]), 4), y=round(float(emb[i, 1]), 4), tags=p['tags'][:6],
                nb=[[int(j), round(float(S[i, j]), 2)] for j in np.argsort(-S[i])[:6]], out=out[i], inn=inn[i])
           for i, p in enumerate(posts)],
    tags=dict(nodes=[dict(id=t, c=tc[t], f=tagfam[t]) for t in top],
              links=[dict(a=a, b=b, c=c) for (a, b), c in co.items() if c >= 4]))
os.makedirs(f'{ROOT}/assets/data', exist_ok=True)
json.dump(data, open(f'{ROOT}/assets/data/carte.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

for i, p in enumerate(posts):   # thème dans le front matter
    th = THEMES[fam[i]][0]
    fm = re.sub(r'^theme:.*\n?', '', p['fm'] + '\n', flags=re.M).rstrip('\n')
    fm = re.sub(r'^(tags:.*)$', lambda m: m.group(1) + f'\ntheme: "{th}"', fm, count=1, flags=re.M)
    if 'theme:' not in fm:
        fm += f'\ntheme: "{th}"'
    open(p['file'], 'w', encoding='utf-8').write('---\n' + fm + '\n---\n' + p['body'])
print('liens internes', sum(len(o) for o in out), '· carte.json', os.path.getsize(f'{ROOT}/assets/data/carte.json') // 1024, 'Ko')
