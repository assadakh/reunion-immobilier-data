"""Lance le pipeline complet : téléchargement -> chargement -> transformations dbt + tests."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DBT_DIR = ROOT / "dvf_dbt"

ETAPES = [
    # étape Extract (téléchargement des fichiers DVF), lancée depuis ROOT
    ("Extract",   [sys.executable, "scripts/download_dvf.py"], ROOT),
    # étape Load (chargement des fichiers DVF dans la base de données), lancée depuis ROOT
    ("Load",   [sys.executable, "scripts/load_row.py"], ROOT),
    # étape Transform (transformation des données avec dbt), lancée depuis DBT_DIR
    ("Transform", ["dbt", "build"], DBT_DIR),
]

if __name__ == "__main__":
    for nom, commande, dossier in ETAPES:
        print(f"\n=== {nom} ===")
        subprocess.run(commande, cwd=dossier, check=True)
    print("\nPipeline terminé avec succès")