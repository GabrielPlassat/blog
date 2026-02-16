# 🚀 Guide de Démarrage Rapide

## Option 1 : Déploiement GitHub Pages (Recommandé)

### Étape 1 : Créer un compte GitHub
Si vous n'en avez pas déjà un, allez sur [github.com](https://github.com) et créez un compte gratuit.

### Étape 2 : Créer un nouveau repository

1. Cliquez sur le `+` en haut à droite > "New repository"
2. Nom du repository : `transports-du-futur` (ou autre nom)
3. Cochez "Public"
4. NE PAS cocher "Initialize with README"
5. Cliquez sur "Create repository"

### Étape 3 : Uploader les fichiers

**Option A : Via l'interface web (plus simple)**
1. Sur la page de votre nouveau repo, cliquez sur "uploading an existing file"
2. Glissez-déposez TOUS les fichiers du dossier `blog-jekyll`
3. Écrivez un message de commit : "Import blog initial"
4. Cliquez sur "Commit changes"

**Option B : Via Git (si vous êtes à l'aise avec la ligne de commande)**
```bash
cd blog-jekyll
git init
git add .
git commit -m "Import blog initial"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/transports-du-futur.git
git push -u origin main
```

### Étape 4 : Activer GitHub Pages

1. Dans votre repo, allez dans **Settings** (roue dentée)
2. Dans le menu de gauche, cliquez sur **Pages**
3. Source : sélectionnez **Deploy from a branch**
4. Branch : sélectionnez **main** et **/ (root)**
5. Cliquez sur **Save**
6. ⏳ Attendez 2-3 minutes

### Étape 5 : Configurer l'URL

Votre site sera disponible sur :
- `https://VOTRE_USERNAME.github.io/transports-du-futur/`

Si ce n'est pas votre site, éditez le fichier `_config.yml` :

```yaml
baseurl: "/transports-du-futur"
url: "https://VOTRE_USERNAME.github.io"
```

Puis commit et push ces changements.

### Étape 6 : C'est en ligne ! 🎉

Visitez votre site sur l'URL indiquée dans Settings > Pages.

---

## Option 2 : Test en local (optionnel)

### Prérequis
- Ruby 2.5+ installé
- Bundler installé

### Installation

```bash
cd blog-jekyll

# Installer les dépendances
bundle install

# Lancer le serveur
bundle exec jekyll serve

# Ouvrir http://localhost:4000
```

---

## 🎨 Personnalisation de base

### Modifier le titre et la description

Éditez `_config.yml` :

```yaml
title: "Votre Titre"
description: "Votre description"
author:
  name: "Votre Nom"
  email: "votre@email.com"
```

### Changer les couleurs

Éditez `assets/css/style.scss` :

```scss
:root {
  --primary: #007bff;      /* Votre couleur principale */
  --primary-dark: #0056b3; /* Version foncée */
}
```

### Ajouter des images

1. Créez un dossier `assets/images/`
2. Copiez vos images dedans
3. Dans les articles, référencez : `![Description](/assets/images/mon-image.jpg)`

---

## 🔧 Dépannage

### Le site ne s'affiche pas
- Vérifiez que GitHub Actions a bien terminé (onglet "Actions")
- Attendez 5 minutes après le premier deploy
- Vérifiez que `baseurl` dans `_config.yml` correspond au nom de votre repo

### Les styles ne s'appliquent pas
- Vérifiez le `baseurl` dans `_config.yml`
- Forcez le refresh avec Ctrl+F5

### La recherche ne fonctionne pas
- Vérifiez que `search.json` est bien présent à la racine
- Ouvrez la console du navigateur (F12) pour voir les erreurs

---

## 📬 Support

Si vous rencontrez des problèmes :
1. Vérifiez les [issues GitHub](https://github.com/VOTRE_REPO/issues)
2. Consultez la [documentation Jekyll](https://jekyllrb.com/docs/)
3. Contactez gabriel.plassat@ademe.fr

---

## 🎓 Ressources

- [GitHub Pages Documentation](https://docs.github.com/pages)
- [Jekyll Documentation](https://jekyllrb.com/)
- [Markdown Guide](https://www.markdownguide.org/)
- [YAML Syntax](https://yaml.org/)

---

**Bonne publication ! 📚**
