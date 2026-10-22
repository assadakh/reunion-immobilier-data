-- Vérifie que toutes les lignes du mart ont nb >= 10.
SELECT annee, nom_commune, type_local, nb
FROM {{ ref('mart_prix_m2_commune_annee') }}
WHERE nb < 10