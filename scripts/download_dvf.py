"""Télécharge les fichiers DVF de La Réunion (974) dans data/raw/.

Source : DVF géolocalisées (Etalab), https://files.data.gouv.fr/geo-dvf/
Lancer depuis n'importe où :  python scripts/download_dvf.py
"""

import urllib.error
import urllib.request
from pathlib import Path

URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/{annee}/departements/974.csv.gz"
ANNEES = range(2020, 2025)  # 2020 à 2024 (la borne de fin est exclue)

# Dossier data/raw/ à la racine du projet, quel que soit l'endroit d'où on lance le script
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def telecharger(annee):
    destination = RAW_DIR / f"974_{annee}.csv.gz"

    # Idempotence : si le fichier est déjà là, on ne refait rien
    if destination.exists():
        print(f"{annee} : déjà présent, on passe")
        return

    url = URL.format(annee=annee)
    temporaire = destination.with_suffix(".tmp")

    try:
        # On télécharge d'abord dans un fichier temporaire...
        urllib.request.urlretrieve(url, temporaire)
    except urllib.error.HTTPError as e:
        temporaire.unlink(missing_ok=True)
        print(f"{annee} : indisponible (erreur {e.code})")
        return

    # ...puis on le renomme : un téléchargement coupé ne laisse pas de faux fichier « déjà présent »
    temporaire.rename(destination)
    taille_ko = destination.stat().st_size / 1024
    print(f"{annee} : téléchargé ({taille_ko:.0f} Ko)")


if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for annee in ANNEES:
        telecharger(annee)
