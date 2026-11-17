"""Dashboard : prix de l'immobilier à La Réunion, à partir du mart dbt."""

from pathlib import Path

import altair as alt
import duckdb
import streamlit as st

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "dvf.duckdb"

st.set_page_config(page_title="Immobilier à La Réunion", layout="wide")


@st.cache_data
def charger_mart():
    with duckdb.connect(str(DB_PATH), read_only=True) as con:
        return con.execute("SELECT * FROM mart_prix_m2_commune_annee").df()


# ✏️ Formate un nombre à la française : 4444.7 -> "4 445"
def fr(nombre):
    return f"{nombre:,.0f}".replace(",", " ")


df = charger_mart()

st.title("Prix de l'immobilier à La Réunion")
st.caption("Source : DVF géolocalisées (Etalab), 2021–2025. Ventes simples uniquement, ventes hors marché exclues.")

# --- Filtres (barre latérale) ---
type_local = st.sidebar.radio("Type de bien", ["Appartement", "Maison"])
annees = sorted(df["annee"].unique())
annee = st.sidebar.select_slider("Année", options=annees, value=annees[-1])

filtre = df[(df["type_local"] == type_local) & (df["annee"] == annee)]

# --- Indicateurs clés ---
plus_chere = filtre.loc[filtre["prix_median"].idxmax()]
moins_chere = filtre.loc[filtre["prix_median"].idxmin()]
total_ventes = filtre["nb"].sum()

col1, col2, col3 = st.columns(3)
col1.metric(f"Plus chère : {plus_chere['nom_commune']}", f"{fr(plus_chere['prix_median'])} €/m²")    # ✏️
col2.metric(f"Moins chère : {moins_chere['nom_commune']}", f"{fr(moins_chere['prix_median'])} €/m²")  # ✏️
col3.metric("Ventes analysées", fr(total_ventes))                                                    # ✏️

# --- Classement des communes ---
st.subheader(f"Prix médian au m² par commune : {type_local.lower()}s, {annee}")

graphique = alt.Chart(filtre).mark_bar().encode(
    x=alt.X("prix_median:Q", title="€/m²"),
    y=alt.Y("nom_commune:N", sort="-x", title=None),
    tooltip=[                                                                   # ✏️ titres en français
        alt.Tooltip("nom_commune:N", title="Commune"),
        alt.Tooltip("prix_median:Q", title="Prix médian (€/m²)", format=",.0f"),
        alt.Tooltip("nb:Q", title="Nombre de ventes"),
    ],
)
st.altair_chart(graphique)

# --- Évolution dans le temps ---
st.subheader(f"Évolution du prix médian au m² : {type_local.lower()}s")

toutes_communes = sorted(df["nom_commune"].unique())
communes_choisies = st.multiselect(
    "Communes à comparer",
    options=toutes_communes,
    default=["Saint-Denis", "Saint-Paul", "Saint-Pierre"],
)

evolution = df[
    (df["type_local"] == type_local)
    & (df["nom_commune"].isin(communes_choisies))
]

courbe = alt.Chart(evolution).mark_line(point=True).encode(
    x=alt.X("annee:O", title="Année", axis=alt.Axis(labelAngle=0)),            # ✏️ années à l'horizontale
    y=alt.Y("prix_median:Q", title="€/m²", scale=alt.Scale(zero=False)),       # ✏️ zoom sur les variations
    color=alt.Color("nom_commune:N", title="Commune"),
    tooltip=[                                                                   # ✏️ titres en français
        alt.Tooltip("nom_commune:N", title="Commune"),
        alt.Tooltip("annee:O", title="Année"),
        alt.Tooltip("prix_median:Q", title="Prix médian (€/m²)", format=",.0f"),
        alt.Tooltip("nb:Q", title="Nombre de ventes"),
    ],
)
st.altair_chart(courbe)

# --- Méthodologie ---
with st.expander("Méthodologie et limites"):
    st.markdown("""
**Données** : Données DVF (Demandes de Valeurs Foncières) géolocalisées à La Réunion, fournies par Etalab, couvrant les années 2021 à 2025, recensant les ventes de biens immobiliers déclarées à l'administration fiscale.

**Ventes retenues** : Uniquement les ventes simples de biens immobiliers, qui ne portent que sur un seul logement (appartement ou maison) éventuellement avec ses dépendances (cave, parking). Car dans les données DVF, lorsqu’une vente porte sur plusieurs logements ou locaux, le prix total est répété sur chaque ligne, et on ne peut pas savoir combien vaut chaque bien.

**Ventes exclues** : Les ventes symboliques d'un montant inférieur à 1 000 € sont exclues, les mutations qui ne sont pas des ventes classiques (échanges, adjudications, ventes sur plan (VEFA), ventes de terrain à bâtir), et les ventes à moins de 500 €/m² considérées comme hors marché (ventes de parts, ventes familiales, logements sociaux).

**Fiabilité** : Une commune est considérée comme fiable si elle a enregistré au moins 10 ventes simples pour le type de bien et l'année sélectionnés, ce qui a pour conséquence que certaines communes ne sont pas affichées dans le classement si elles n'ont pas atteint ce seuil.

**Limites** :
- Le prix au m² ne compte que la surface bâtie, pas le terrain. Pour une maison sur un grand terrain, ou en bord de mer, le prix au m² est gonflé. Par exemple, dans le cas d'une des maisons à Saint-Gilles, rue des Sables, un bien de 50 m² vendu 1 500 000 € sur un terrain de 237 m², ce qui fait un prix au m² de 30 000 €/m² bâti.
- L'effet de composition : si, une année, il y a plus de ventes dans les quartiers chers, la médiane monte sans que les prix n'aient réellement augmenté. Les évolutions sont donc à interpréter avec prudence, surtout pour les communes avec peu de ventes.
- En excluant les VEFA, on exclut les logements neufs vendus sur plan, qui sont souvent plus chers que les logements anciens. Cela peut donc sous-estimer le prix médian dans certaines communes où il y a beaucoup de VEFA.
""")