SELECT
    annee,
    nom_commune,
    type_local,
    MEDIAN(prix_m2) AS prix_median,
    COUNT(*)        AS nb
FROM {{ ref('int_ventes_simples') }}
WHERE NOT hors_marche
  AND type_local IN ('Appartement', 'Maison')
GROUP BY annee, nom_commune, type_local
HAVING COUNT(*) >= 10