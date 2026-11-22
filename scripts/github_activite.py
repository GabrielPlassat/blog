#!/usr/bin/env python3
"""Récupère l'activité GitHub publique et l'écrit dans _data/github.json.

Lancé par le workflow de publication, juste avant la construction Jekyll.
L'onglet « L'atelier » (atelier.md, via _includes/github.html) lit ce
fichier. Si GitHub ne répond pas, le fichier est écrit vide et la page
affiche un simple lien vers GitHub : la publication n'est jamais bloquée.

Réglages dans _config.yml, rubrique `github` :
  utilisateur : compte GitHub à afficher
  nombre      : nombre de projets montrés (0 = tous)
  exclure     : dépôts à ne pas montrer (ex. le blog lui-même)
"""
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.request

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "_data" / "github.json"
SEMAINES = 12


def lire_reglages():
    """Lecture minimale de la rubrique `github:` de _config.yml (sans dépendance)."""
    reglages = {"utilisateur": "GabrielPlassat", "nombre": 6, "exclure": []}
    lignes = (RACINE / "_config.yml").read_text(encoding="utf-8").splitlines()
    dedans, cle_liste = False, None
    for ligne in lignes:
        if ligne.startswith("github:"):
            dedans = True
            continue
        if dedans and ligne and not ligne.startswith(" "):
            break
        if not dedans or not ligne.strip() or ligne.strip().startswith("#"):
            continue
        brut = ligne.strip()
        if brut.startswith("- ") and cle_liste:
            reglages[cle_liste].append(brut[2:].strip().strip('"\''))
            continue
        cle, _, valeur = brut.partition(":")
        cle, valeur = cle.strip(), valeur.strip().strip('"\'')
        if valeur == "":
            cle_liste = cle
            reglages[cle] = []
        else:
            cle_liste = None
            reglages[cle] = int(valeur) if valeur.isdigit() else valeur
    return reglages


def appel(chemin):
    requete = urllib.request.Request(
        "https://api.github.com/" + chemin,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "blog-transports-du-futur"},
    )
    jeton = os.environ.get("GITHUB_TOKEN")
    if jeton:
        requete.add_header("Authorization", "Bearer " + jeton)
    with urllib.request.urlopen(requete, timeout=20) as reponse:
        return json.load(reponse)


def date(texte):
    return dt.datetime.fromisoformat(texte.replace("Z", "+00:00"))


def construire(depots, evenements, reglages, maintenant):
    exclure = {e.lower() for e in reglages.get("exclure", [])}
    gardes = [
        d for d in depots
        if not d.get("fork") and not d.get("archived") and not d.get("private")
        and d["name"].lower() not in exclure
    ]
    gardes.sort(key=lambda d: d.get("pushed_at") or "", reverse=True)

    il_y_a_30j = maintenant - dt.timedelta(days=30)
    actifs_30j = sum(1 for d in gardes if d.get("pushed_at") and date(d["pushed_at"]) >= il_y_a_30j)

    # Commits par semaine sur les 12 dernières semaines (événements publics « push »)
    debut = maintenant - dt.timedelta(weeks=SEMAINES)
    semaines = [0] * SEMAINES
    for ev in evenements:
        if ev.get("type") != "PushEvent":
            continue
        if ev.get("repo", {}).get("name", "").split("/")[-1].lower() in exclure:
            continue
        quand = date(ev["created_at"])
        if quand < debut:
            continue
        indice = min(SEMAINES - 1, int((quand - debut).days // 7))
        charge = ev.get("payload", {})
        semaines[indice] += charge.get("size") or charge.get("distinct_size") or 1
    pic = max(semaines) or 1

    projets = []
    nombre = int(reglages.get("nombre", 0)) or len(gardes)
    for d in gardes[:nombre]:
        projets.append({
            "nom": d["name"],
            "description": d.get("description") or "",
            "url": d["html_url"],
            "demo": d.get("homepage") or "",
            "langage": d.get("language") or "",
            "maj": (d.get("pushed_at") or "")[:10],
            "etoiles": d.get("stargazers_count", 0),
        })

    return {
        "utilisateur": reglages["utilisateur"],
        "profil": "https://github.com/" + reglages["utilisateur"],
        "genere": maintenant.strftime("%Y-%m-%d"),
        "nb_depots": len(gardes),
        "actifs_30j": actifs_30j,
        "commits_12s": sum(semaines),
        "semaines": [{"n": n, "h": round(100 * n / pic)} for n in semaines],
        "projets": projets,
    }


def main():
    reglages = lire_reglages()
    SORTIE.parent.mkdir(exist_ok=True)
    utilisateur = reglages["utilisateur"]
    try:
        depots = appel(f"users/{utilisateur}/repos?per_page=100&sort=pushed&type=owner")
        try:
            evenements = appel(f"users/{utilisateur}/events/public?per_page=100")
        except Exception:
            evenements = []
        donnees = construire(depots, evenements, reglages, dt.datetime.now(dt.timezone.utc))
    except Exception as erreur:  # GitHub injoignable : on publie sans l'encart
        print(f"Activité GitHub indisponible ({erreur}) : encart masqué.", file=sys.stderr)
        donnees = {}
    SORTIE.write_text(json.dumps(donnees, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{SORTIE.relative_to(RACINE)} : {len(donnees.get('projets', []))} projets.")


if __name__ == "__main__":
    main()
