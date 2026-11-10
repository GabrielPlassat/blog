---
layout: post
title: "La Robustesse est la Nouvelle Vitesse"
date: 2025-11-28
source: xd
source_name: "Blog XD (ADEME)"
original_url: "https://xd.ademe.fr/blog/la-robustesse-est-la-nouvelle-vitesse"
tags: ["robuste", "stress test", "système", "multi échelle"]
theme: "Énergie, émissions & consommateurs"
---

*Vers des Programmes Territoriaux de Stress Test*

L’eXtrême Défi Mobilité (XD) cherche à redéfinir la performance des Véhicules Électriques Légers Intermédiaires (**VELIs**). Il ne s’agit plus de concevoir des machines ultra-performantes, caractérisées par la puissance et la vitesse. A l’inverse, il s’agit de constituer les briques d’un système de mobilité radicalement robuste. La robustesse, loin d’être un luxe, devient un critère essentiel pour réduire nos dépendances et faire face aux nombreuses incertitudes énergétiques et d’approvisionnement actuelles et à venir.

### Pourquoi la Robustesse est Indispensable

La robustesse est la clé de la pérennité et de l’accessibilité de ces véhicules. Elle garantit notamment une mobilité qui dépend moins des chaînes logistiques mondialisées et du prix des énergies. Quand la vitesse moyenne des automobiles ne dépasse pas 20 km/h et la puissance maxi n’est jamais utilisée mais payée à chaque mètre parcouru, il devient nécessaire de revenir sur les principales caractéristiques de nos objets roulants.

La robustesse découle d’abord d’une **sobriété** de conception, du réduction du nombre de pièces (faible masse), associée à la **réduction des performances** (faible vitesse, faible énergie cinétique). La lenteur apparente des vélis, en tout cas leur faible vitesse maxi, est un signe de robustesse qui engendre de nombreux effets positifs. Ce choix diminue les contraintes mécaniques, l’usure et la quantité de matière nécessaire à la fabrication et cela ouvre à l’utilisation d’autres matériaux et procédés. Cela impacte également les risques pour les autres avec des véhicules à faible énergie cinétique en comparaison avec l’automobile ou encore l'endommagement des routes. La situation actuelle est ironique puisque ce sont les véhicules à faible énergie cinétique qui sont aujourd’hui limités en vitesse maxi et puissance par les réglementations et pas les véhicules les plus lourds, puissants et rapides, donc dangereux pour les autres.

De plus, la robustesse est renforcée par une **autonomie énergétique** partielle sur plusieurs véhicules. L’intégration de sources d’énergie variées, comme les **panneaux photovoltaïques** ou les **pédaliers générateurs**, permet aux VELIs d’assurer une alimentation hors réseau face aux ruptures. Olivier Hamant insiste sur l’opposition Robustesse / Performance (voir notamment ce [wiki](https://larobustesse.org/?FacetteRessource), ce [podcast](https://www.radiofrance.fr/franceinter/podcasts/zoom-zoom-zen/zoom-zoom-zen-du-jeudi-05-decembre-2024-4079917) et cette [publication](https://journals.openedition.org/edso/31966)).

### Comment Atteindre la Robustesse dans la Conception ?

La robustesse est intégrée au véhicule par un ensemble de choix de conception radicaux, privilégiant la simplicité, la réparabilité et la circularité à plusieurs niveaux.

**Organisation de la Robustesse sur les Véhicules :**

- **Conception Circulaire et Réparable :** L’accent est mis sur l’**éco-conception pour la réparation** et le **reconditionnement** des pièces. L’utilisation de matériaux comme l’acier ou l’aluminium, mais aussi le bois et les fibres naturelles, faciles à réparer localement, est favorisée. Sur certains projets, l’assemblage par **rivetage** remplace la soudure pour des réparations simplifiées. Les véhicules sont, pour la plupart, **ouverts**, c’est à dire que tous les composants sont visibles simplifiant l’auto-diagnostic et les premiers entretiens du quotidien.
- **Modularité et Interopérabilité :** Pour améliorer la maintenance, des **interfaces standardisées** entre les composants critiques (batteries, châssis, siège, chassis) sont mises en œuvre. Cette standardisation permet d’échanger rapidement des modules, y compris la batterie. Cela apporte également une interdépendance entre les véhicules (et donc les entreprises) et une forme de redondance puisqu’une réparation pourra être effectuée avec un autre véhicule avec le même composant et outillage.
- **Liberté Technologique et Logiciels Libres :** La robustesse numérique est assurée par l’utilisation de **logiciels ouverts** pour le contrôle du véhicule comme proposé par [OwnTech](https://wikixd.fabmob.io/wiki/OwnDrive) et la gestion des batteries (**BMS**). Cette approche garantit la liberté de maintenance et l’évolution du véhicule, comme avec le **BMS Open Source** développé par l’équipe du **HPULHV** et plus récemment un **pédalier générateur** en cours de mise en open source par OuiCycle.
- **Exemples Concrets :** Des projets comme le **Vhéliotech** intègrent directement des **panneaux solaires**. D’autres, comme l’**E-nvy One**, utilisent des **fusibles mécaniques** et des raccords imprimés en 3D pour un remplacement facile des tubes du châssis en cas de choc. L’association **Vadzaih** publie en open source des technologies visant à alléger avec un chassis en bois ou encore une [solution aérodynamique auto-gonflante](https://wikixd.fabmob.io/wiki/GFG201).

### Tester et Intégrer la Robustesse aux différentes échelles

La robustesse est à travailler en collectif. Sa validation en situation réelle est cruciale. Elle pourrait être menée à travers un **Programme Territorial de Stress Test (PTST-VELI)**, organisé en deux phases complémentaires : le travail sur les véhicules, puis l’intégration territoriale.

#### Phase 1 : Le Travail sur les Véhicules

Une flotte de VELIs est soumise à des missions critiques dans des conditions extrêmes réelles ou simulées pour mesurer leurs limites, s’améliorer et “donner à voir” :

- **Stress Énergétique (Off-Grid) :** Les véhicules doivent achever plusieurs missions en rechargeant le moins souvent les batteries et en n’utilisant que les sources alternatives (solaire, pédalage), simulant une panne réseau généralisée. Utiliser des outils d’évaluation (comme le [mobilitywidget](https://www.mobilitywidgets.com/extreme-defi/embed) de l’eXtrême Défi) pour calculer les itinéraires et les consommations d’énergie associées pour différents types de VELIs et ainsi valider les données de performance énergétique.
- **Stress d’Approvisionnement :** Les équipes simulent la défaillance d’un composant critique. L’évaluation se concentre sur le **MTTR (Mean Time To Repair)** et la capacité à réparer avec des outils et des pièces facilement disponibles. Simulation de Pénurie de Pièces : Tester la capacité des ateliers distribués à usiner des matériaux ou réemployer des composants locaux en cas de rupture d’approvisionnement des pièces critiques. Diagnostic de Panne par l’Utilisateur : S’assurer que les utilisateurs peuvent facilement comprendre le fonctionnement du véhicule, identifier les composants et réaliser un diagnostic simple et rapide pour l’entretien et la réparation par soi-même ou par la communauté proche.
- **Stress Physique :** Des tests mesurent la **stabilité en virage** après un choc simulé ou la résistance structurelle à l’usage intensif, en vérifiant la bonne tenue des assemblages.
- Et des idées de "**fluctuations**" sur le [wiki](https://larobustesse.org/?FluctuationS)

#### Phase 2 : Le Déploiement Territorial et la Mobilisation des Compétences

Utilisant des vélis ayant réussis les stress tests, un territoire pilote motivé pourrait devenir le laboratoire où la robustesse d’un “Système Véli” local est testée.

**Identification des Acteurs et des Usages**

Les VELIs sont mis entre les mains de professionnels dont l’activité est jugée critique comme par exemple :

- **Agents de la collectivité :** Pour les missions d’entretien, de voirie ou de logistique inter-sites.
- **Artisans et TPE/PME :** Pour la logistique du dernier kilomètre en zone dense ou rurale.
- **Aides à domicile et professionnels de santé :** Pour les visites, nécessitant une fiabilité maximale.
- **Autres volontaires :** à définir avec le territoire

**Compétences et Moyens Matériels Locaux**

Le programme s’appuie alors sur la capacité du territoire à fonctionner puis à s’auto-réparer. Les tests pourraient viser à identifier :

- **Compétences Locales :** Les garagistes indépendants, les ateliers vélos, les Fab Labs, les centres de formation professionnelle et les écoles, les services techniques des collectivités et d’autres acteurs motivés sont mobilisés pour réparer et reconditionner les véhicules. Ces structures possèdent déjà les compétences et savoir faire en mécanique générale, électricité basse tension et soudure (pour l’acier/alu).
- **Reconditionnement des Composants :** Un effort particulier est fait pour évaluer la capacité locale à **reconditionner les vélis**, certains composants, en utilisant l’approche Open Source (comme celle du BMS et du pédalier).
- **Moyens Matériels Existants :** L’inventaire des outils de production locaux (imprimantes 3D, découpe laser, machines-outils standard) est dressé pour valider la fabrication de pièces de rechange critiques.
- Identification des **dépendances** à des tiers en dehors du territoire pour constituer des réseaux étendus de collaboration, d’échanges et de services.

### Les Livrables du programme Territorial de Stress Test

Les résultats d’un tel programme pourront alimenter une boucle d’amélioration continue basée sur la **coopération**. Le savoir est mis à disposition de tous :

- Les **Fiches de Robustesse** et les solutions de design éprouvées pour les véhicules, le système et les acteurs impliqués dans la production et la maintenance sont documentées sur le **Wiki XD** sous **licence libre**.
- Un **Design Guide pour la Robustesse** est créé, formalisant les meilleures pratiques pour la prochaine génération de VELIs, garantissant ainsi que ces véhicules ne sont pas seulement l’avenir de la mobilité, mais des solutions robustes, fabriquées et maintenues avec les ressources des territoires, avec des dépendances identifiées et maîtrisées.
- Les **Acteurs des territoires** jouant un rôle dans l’entretien, la réparation, la maintenance créant un réseau de dépendance en proximité. Ce réseau pourrait déjà avoir conscience de sa valeur, ses capacités d’actions, puis se former et inviter de nouvelles personnes à le rejoindre. Un tel réseau transcende les frontières de la formation, l’éducation et des métiers, ou encore du professionnel et du personnel, pour devenir pleinement acteur dans la transformation des filières industrielles, des territoires et des modes de vies.

Ce plan, qui lie intimement la conception (sobriété, réparabilité) et l’expérimentation (tests de résistance aux crises et aux usages intensifs), permettrait de consolider un écosystème robuste comprenant notamment des VELIs, en ne cherchant pas la performance maximale, pour construire progressivement des solutions beaucoup plus robustes aux crises à venir.
