# Immobilier à La Réunion : analyse des données DVF

Analyse des ventes immobilières à La Réunion (département 974) à partir des données publiques **DVF** (Demandes de valeurs foncières), sur les années 2021 à 2025.

Le projet suit un parcours d'apprentissage du data engineering : téléchargement automatisé et idempotent des données, exploration avec pandas, puis passage à une base analytique avec DuckDB et SQL.

## Premiers résultats

Prix médian au m² des ventes « simples » (un seul bien vendu, ventes hors marché exclues) :

| Année | Appartements | Maisons |
|------:|-------------:|--------:|
| 2021  | ≈ 2 300 €/m² | ≈ 2 540 €/m² |
| 2025  | ≈ 2 860 €/m² | ≈ 2 830 €/m² |

- Les appartements ont pris environ **+24 %** en 4 ans. Les maisons, environ **+12 %**, avec un plateau depuis 2023.
- Les communes les plus chères sont sur la côte Ouest : **Saint-Paul** (≈ 5 100 €/m² pour les appartements en 2024), Saint-Leu et L'Étang-Salé.

## Les données

- **Source** : [DVF géolocalisées](https://files.data.gouv.fr/geo-dvf/), publiées par Etalab sur data.gouv.fr (licence Ouverte).
- **Contenu** : toutes les ventes enregistrées par les notaires, avec prix, date, adresse, surfaces et type de bien.
- **Disponibilité** : data.gouv.fr ne garde que les 5 dernières années (2021 à 2025 à ce jour).

Les données ne sont pas versionnées dans ce dépôt (`data/` est dans le `.gitignore`). Le script `scripts/download_dvf.py` les récupère.

### Pièges connus de DVF

- **Une vente occupe plusieurs lignes** : chaque lot, cave ou parcelle a sa propre ligne, et toutes répètent le prix total. Il faut raisonner par `id_mutation`, sinon une moyenne naïve est fausse (2,66 M€ au lieu de 273 000 € en 2024).
- **Ventes hors marché** : prix symboliques à 1 € ou à quelques centaines d'euros le m². Elles sont repérées par un seuil de 500 €/m².
- **Ventes en bloc** : un seul prix pour un immeuble entier (jusqu'à plus de 3 000 lignes pour une seule vente).
- **Le prix au m² inclut le terrain** pour les maisons, ce qui gonfle les valeurs dans les zones où le foncier est cher, comme Saint-Gilles.

## Structure du projet

```
reunion-immobilier-data/
├── data/                      # non versionné
│   ├── raw/                   # fichiers 974_{annee}.csv.gz téléchargés
│   └── dvf.duckdb             # base DuckDB créée par le notebook 2
├── notebooks/
│   ├── 01_exploration_dvf.ipynb   # exploration pandas de l'année 2024
│   └── 02_duckdb.ipynb            # 5 années dans DuckDB, requêtes SQL, évolution des prix
├── scripts/
│   └── download_dvf.py        # téléchargement des données (idempotent)
└── requirements.txt
```

## Installation

Prérequis : Python 3.11 ou plus récent.

```bash
git clone https://github.com/assadakh/reunion-immobilier-data.git
cd reunion-immobilier-data

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

## Utilisation

1. **Télécharger les données**

   ```bash
   python scripts/download_dvf.py
   ```

   Le script est **idempotent** : les fichiers déjà présents ne sont pas retéléchargés, on peut donc le relancer sans risque.

2. **Lancer les notebooks** dans l'ordre, avec le kernel du `.venv` :

   ```bash
   jupyter notebook notebooks/
   ```

   - `01_exploration_dvf.ipynb` : structure du fichier, pièges DVF, prix médian au m² par commune.
   - `02_duckdb.ipynb` : chargement des 5 années dans DuckDB, réécriture du filtrage en SQL (CTE), vérification contre pandas, évolution des prix.

## Outils

Python, pandas, DuckDB, SQL, Jupyter, matplotlib.

## Pistes pour la suite

- Prendre en compte la surface du terrain pour les maisons.
- Passer le filtrage dans un script réutilisable plutôt que dans les notebooks.
- Cartographier les prix avec les coordonnées GPS fournies par DVF.
