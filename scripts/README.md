# Scripts de la refonte (novembre 2026)

Trois scripts Python, à lancer dans l'ordre (Colab ou poste local, `pip install scikit-learn scipy`) :

1. `importer.py` — réunit les cinq blogs dans `_posts/` avec un front matter homogène
   (`title`, `date`, `source`, `source_name`, `original_url`, `tags`, `redirect_from`).
   Les chemins des sources (dépôts clonés, exports) sont en tête du fichier.
2. `liens.py` — revoit chaque article et réécrit ses liens :
   ancienne adresse d'un article du corpus → nouvelle adresse `/AAAA/MM/titre/` ;
   image présente dans `assets/` → adresse locale ;
   ancien site fermé (Typepad, transportsdufutur.ademe.fr, lafabriquedesmobilites.fr) sans article correspondant → copie web.archive.org.
   Le détail est dans `rapport-liens.csv` (une ligne par lien modifié).
3. `nettoyage.py` — retire la « traîne » de l'ancien export CSV (date, adresse, tags collés par des |, courriel…) laissée en bas de certains articles de Transports du Futur, et rétablit les liens vidés lors de l'ancienne conversion en retrouvant leur adresse dans `articles.csv` (détail dans `rapport-nettoyage.csv`). Relancer ensuite `liens.py`.
4. `carte.py` — calcule les neuf thèmes, les voisins de chaque article, la constellation et le rhizome des tags,
   écrit `assets/data/carte.json` et la ligne `theme:` de chaque article.

Pour ajouter un article : créer `_posts/AAAA-MM-JJ-titre.md` avec le même front matter, puis relancer `carte.py`.
