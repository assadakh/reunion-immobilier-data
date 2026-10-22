-- Le mart doit avoir une seule ligne par (année, commune, type)
SELECT annee, nom_commune, type_local, COUNT(*) AS nb_lignes
FROM {{ ref('mart_prix_m2_commune_annee') }}
GROUP BY annee, nom_commune, type_local
HAVING COUNT(*) > 1