# 🚀 Transports du Futur - Blog Jekyll

Blog personnel réunissant vingt ans d'écrits sur les mobilités, les communs et les véhicules intermédiaires (2009-2026) : Transports du Futur, la Fabrique des Mobilités, Bricologie & Sérendipité, le blog de l'eXtrême Défi et LinkedIn.

Cinq entrées : **Thèmes**, **Derniers articles**, **le ciel** (constellation des articles), **la terre** (rhizome des tags), **le temps** (chronologie). Les scripts de la refonte sont décrits dans `scripts/README.md`.

## 📊 Statistiques

- **1 121 articles** publiés (978 Transports du Futur, 92 FabMob, 24 XD, 21 Bricologie, 6 LinkedIn)
- **261 tags** thématiques
- **Période** : 2009-2026
- **Auteur** : Gabriel Plassat

## ✨ Fonctionnalités

- ✅ **Recherche full-text** dans tous les articles
- ✅ **Navigation par tags** avec nuage interactif
- ✅ **Timeline chronologique** des articles
- ✅ **Archives complètes** par année et mois
- ✅ **Design minimaliste** style Medium
- ✅ **SEO optimisé** avec Jekyll
- ✅ **Responsive** mobile-first

## 🚀 Déploiement sur GitHub Pages

### 1. Créer un repository GitHub

```bash
# Depuis votre ordinateur local
git init
git add .
git commit -m "Initial commit - 998 articles"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
git push -u origin main
```

### 2. Activer GitHub Pages

1. Aller sur votre repository GitHub
2. **Settings** > **Pages**
3. Source : **Deploy from a branch**
4. Branch : **main** / folder : **/ (root)**
5. Cliquer sur **Save**

### 3. Configurer l'URL

Éditer `_config.yml` :

```yaml
# Si hébergé sur username.github.io
baseurl: ""
url: "https://VOTRE_USERNAME.github.io"

# Si hébergé sur username.github.io/nom-repo
baseurl: "/nom-repo"
url: "https://VOTRE_USERNAME.github.io"
```

## 🖥️ Développement local

### Installation

```bash
# Installer Ruby et Jekyll (si pas déjà fait)
gem install bundler jekyll

# Installer les dépendances
bundle install
```

### Lancer le serveur local

```bash
bundle exec jekyll serve

# Ou avec live reload
bundle exec jekyll serve --livereload

# Le site sera disponible sur http://localhost:4000
```

## 📁 Structure du projet

```
.
├── _config.yml           # Configuration Jekyll
├── _posts/              # 998 articles (format: YYYY-MM-DD-slug.md)
├── assets/
│   ├── css/
│   │   └── style.scss   # CSS principal
│   └── js/
│       └── search.js    # Moteur de recherche
├── index.html           # Page d'accueil
├── archives.html        # Archives complètes
├── tags.html            # Page des tags
├── search.json          # Index de recherche
├── Gemfile              # Dépendances Ruby
└── README.md            # Ce fichier
```

## 🎨 Personnalisation

### Modifier les couleurs

Éditer `assets/css/style.scss` :

```scss
:root {
  --primary: #007bff;        // Couleur principale
  --primary-dark: #0056b3;   // Couleur foncée
  --text: #212529;           // Couleur du texte
  --text-muted: #6c757d;     // Texte secondaire
  // ...
}
```

### Ajouter des pages

Créer un fichier `.md` ou `.html` avec le front matter :

```yaml
---
layout: page
title: Ma page
permalink: /ma-page/
---

Contenu de la page...
```

### Modifier le thème

Le thème actuel est basé sur Minima. Pour changer :

1. Éditer `_config.yml`
2. Modifier `theme:` ou `remote_theme:`
3. Adapter les layouts et styles

## 📝 Ajouter un nouvel article

Créer un fichier dans `_posts/` :

```markdown
---
layout: post
title: "Mon titre"
date: 2024-02-16 10:00:00 +0100
categories: []
tags: [mobilité, innovation]
---

Contenu de l'article...
```

## 🔍 Recherche

La recherche fonctionne côté client via JavaScript :
- Index JSON généré automatiquement (`search.json`)
- Recherche full-text dans titres, contenus et tags
- Résultats instantanés avec surlignage

## 📸 Images

### Images actuelles

Les images sont référencées dans les articles avec des chemins comme :
```
/wp-content/uploads/sites/6/old/...
```

### Ajouter les images

1. Télécharger `tdf-export-media.zip`
2. Extraire dans le dossier `assets/images/`
3. Mettre à jour les chemins dans les articles si nécessaire

Ou utiliser un script de remplacement :

```bash
# Remplacer les anciens chemins
find _posts -type f -name "*.md" -exec sed -i 's|/wp-content/uploads/sites/6/old/|/assets/images/|g' {} \;
```

## 🌐 Domaine personnalisé (optionnel)

Pour utiliser votre propre domaine :

1. Créer un fichier `CNAME` à la racine :
```
blog.votredomaine.com
```

2. Configurer les DNS chez votre registrar :
```
Type: CNAME
Name: blog
Value: VOTRE_USERNAME.github.io
```

3. Activer HTTPS dans Settings > Pages

## 🔗 Liens utiles

- [Documentation Jekyll](https://jekyllrb.com/docs/)
- [GitHub Pages](https://docs.github.com/pages)
- [Thème Minima](https://github.com/jekyll/minima)
- [Markdown Guide](https://www.markdownguide.org/)

## 📄 Licence

Articles : © Gabriel Plassat  
Code : MIT License

## 🤝 Contribution

Ce blog est personnel mais les suggestions sont bienvenues :
- Ouvrir une issue pour signaler un problème
- Proposer des améliorations via PR

---

**Créé avec** ❤️ **et Jekyll** • 998 articles • 2009-2024
